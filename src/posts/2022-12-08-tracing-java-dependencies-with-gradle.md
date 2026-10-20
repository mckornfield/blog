---
title: "Tracing Java Dependencies with Gradle"
subtitle: "Ever wonder why a library ends up in your Production JAR?"
date: 2022-12-08
medium_url: "https://medium.com/@mckornfield/tracing-java-dependencies-with-gradle-98dd93f8e973"
---

Ever wonder why a library ends up in your Production JAR?

![Photo by Anna Dziubinska on Unsplash](/img/tracing-java-dependencies-with-gradle/0_9mOrlMU8ee6j7Ig-.jpg)

*Photo by [Anna Dziubinska](https://unsplash.com/@annadziubinska?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Gradle has some [pretty awesome docs](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html) when it comes to using the tool to debug the origin of dependencies, but I thought I’d take you through an open source project as an example.

Many people I’ve worked with were always curious why a CVE showed up for a library they hadn’t heard of, and it’s good to know how to quickly see where a dependency comes from.

### Where do we begin?

`./gradlew dependencies` ?

WRONG!

The Gradle docs will let you know that just shows the root project dependencies, which, for most projects there’s some sort of multi-project setup going on.

Let’s walk through the [spring-framework](https://github.com/spring-projects/spring-framework) repo and see where some dependencies come from. Feel free to clone the OSS repo and follow along.

(Note: running `./gradlew dependencies` returns something for this project and many others, but it isn’t very useful)

### Let’s start over

Before we can list dependencies, we need a project to do it on! How do we get the list of projects?

`./gradlew -q projects` ?

Yes!

Running that in the spring-framework repo gives us:

```java
Root project 'spring' - Spring Framework
+--- Project ':framework-bom' - Spring Framework (Bill of Materials)
+--- Project ':framework-docs' - Spring Framework Docs
+--- Project ':framework-platform'
+--- Project ':integration-tests' - Spring Integration Tests
+--- Project ':spring-aop' - Spring AOP
+--- Project ':spring-aspects' - Spring Aspects
+--- Project ':spring-beans' - Spring Beans
+--- Project ':spring-context' - Spring Context
+--- Project ':spring-context-indexer' - Spring Context Indexer
+--- Project ':spring-context-support' - Spring Context Support
+--- Project ':spring-core' - Spring Core
+--- Project ':spring-core-test' - Spring Core Test
+--- Project ':spring-expression' - Spring Expression Language (SpEL)
+--- Project ':spring-instrument' - Spring Instrument
+--- Project ':spring-jcl' - Spring Commons Logging Bridge
+--- Project ':spring-jdbc' - Spring JDBC
+--- Project ':spring-jms' - Spring JMS
+--- Project ':spring-messaging' - Spring Messaging
+--- Project ':spring-orm' - Spring Object/Relational Mapping
+--- Project ':spring-oxm' - Spring Object/XML Marshalling
+--- Project ':spring-r2dbc' - Spring R2DBC
+--- Project ':spring-test' - Spring TestContext Framework
+--- Project ':spring-tx' - Spring Transaction
+--- Project ':spring-web' - Spring Web
+--- Project ':spring-webflux' - Spring WebFlux
+--- Project ':spring-webmvc' - Spring Web MVC
\--- Project ':spring-websocket' - Spring WebSocket
```

OK great… What now?

How about we list off the dependencies in `spring-core` , that sounds like a fun one?

`./gradlew -q :spring-core:dependencies`

*terminal flies by*

What was that? 2356 lines of text? OK let’s try…

`./gradlew -q :spring-core:dependencies | less`

Now at least we can scroll through. You’ll see various sections `compileClasspath` that map well to this [diagram](https://docs.gradle.org/current/userguide/img/java-main-configurations.png) and this [diagram](https://docs.gradle.org/current/userguide/img/java-test-configurations.png) in the [Gradle docs](https://docs.gradle.org/current/userguide/java_plugin.html#sec:java_plugin_and_dependency_management). But essentially you have a bunch of trees to look through.

You could write this output to a file and grep for them, maybe if you were searching for `jackson-databind` because of its many [CVEs](https://www.cvedetails.com/vulnerability-list/vendor_id-15866/product_id-42991/Fasterxml-Jackson-databind.html) you could do

```ruby
./gradlew -q :spring-core:dependencies > deps.txt
grep -C5 jackson-databind deps.txt
```

And you might get some… semi useful output.

```lua
     |         |    \--- org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.3 (c)
     |         +--- org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.6.21 -> 1.7.20 (*)
     |         \--- org.jetbrains.kotlin:kotlin-stdlib-common:1.6.21 -> 1.7.20
     +--- org.jsoup:jsoup:1.14.3
     +--- com.fasterxml.jackson.module:jackson-module-kotlin:2.12.7
     |    +--- com.fasterxml.jackson.core:jackson-databind:2.12.7
     |    |    +--- com.fasterxml.jackson.core:jackson-annotations:2.12.7
     |    |    |    \--- com.fasterxml.jackson:jackson-bom:2.12.7
     |    |    |         +--- com.fasterxml.jackson.core:jackson-annotations:2.12.7 (c)
     |    |    |         +--- com.fasterxml.jackson.core:jackson-databind:2.12.7 (c)
     |    |    |         +--- com.fasterxml.jackson.module:jackson-module-kotlin:2.12.7 (c)
     |    |    |         \--- com.fasterxml.jackson.core:jackson-core:2.12.7 (c)
     |    |    +--- com.fasterxml.jackson.core:jackson-core:2.12.7
     |    |    |    \--- com.fasterxml.jackson:jackson-bom:2.12.7 (*)
     |    |    \--- com.fasterxml.jackson:jackson-bom:2.12.7 (*)
```

But a lot of times the dependency type that the tree is under is cut off. And scrolling sucks. There’s got to be a better output format yeah?

### Build Scans?

Build scans are great. They go away after a while usually but if you navigate to the [right tab](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html#sec:identifying_reason_dependency_selection) on a scan you can see the sort of information we’ll be able to demonstrate with the CLI here in a sec. Basically the inverted tree, showing the path to the build scan.

### Dependency Insight — The Big Brain Approach

Further on in the Gradle Docs you’ll see `dependencyInsight`

😇👼*Angelic Chorus*🐠😇

This tool is the best… well almost the best. The thing it *doesn’t* do is tell you the configuration; you have to pass that in!

Fortunately there are really only four that matter in most cases, `compileClasspath` , `runtimeClasspath` ,`testCompileClasspath` , and `testRuntimeClasspath` .

Quick refresher on dependency formats, for example, this

`com.fasterxml.jackson.core:jackson-databind:2.12.7` is

`group:artifact:version`

Which is how we’re able to resolve the dependency from an artifact store like [Maven Central](https://search.maven.org/).

The dependency is a partial match on the `group:artifact:version` , so we’re just going to throw in `databind`for our search.

I went through the four configurations above but no databind…

```ruby
for configuration in compileClasspath runtimeClassPath testCompileClasspath testRuntimeClasspath; do
 ./gradlew -q :spring-core:dependencyInsight --configuration $configuration \
     --dependency 'databind'
done
```

Turns out I was wrong! It was in some of those “bizarre” configurations.

We can just go through them all! Doing some yucky parsing on the `./gradlew -q :spring-core:dependencies` command we can get our configurations.

(We throw out the (n) dependencies, and just grab their names by finding all the text after empty newlines).

```ruby
configurations=$(./gradlew -q :spring-core:dependencies | grep -A1 '^$' | \
    grep -v "\-\-" | grep -v \(n\) | \
    grep -v '^$' | cut -d" " -f1 | grep -v '(')
for configuration in $configurations; do
 echo "== $configuration ==" # Useful for the successful cases so we know the config
 ./gradlew -q :spring-core:dependencyInsight --configuration $configuration \
     --dependency 'databind'
done
```

We’ll get some empties, like the four horseman I expected an answer from… But heck yeah we got some databind!

```sql
== dokkaHtmlPartialPlugin ==
com.fasterxml.jackson.core:jackson-databind:2.12.7 (by constraint)
  Variant runtimeElements:
    | Attribute Name                 | Provided     | Requested    |
    |--------------------------------|--------------|--------------|
    | org.gradle.category            | library      |              |
    | org.gradle.dependency.bundling | external     |              |
    | org.gradle.libraryelements     | jar          |              |
    | org.gradle.status              | release      |              |
    | org.gradle.usage               | java-runtime | java-runtime |

com.fasterxml.jackson.core:jackson-databind:2.12.7
+--- com.fasterxml.jackson:jackson-bom:2.12.7
|    +--- com.fasterxml.jackson.core:jackson-databind:2.12.7 (*)
|    +--- com.fasterxml.jackson.core:jackson-annotations:2.12.7
|    |    +--- com.fasterxml.jackson.core:jackson-databind:2.12.7 (*)
|    |    +--- com.fasterxml.jackson:jackson-bom:2.12.7 (*)
|    |    \--- com.fasterxml.jackson.module:jackson-module-kotlin:2.12.7
|    |         +--- org.jetbrains.dokka:dokka-base:1.7.20
|    |         |    \--- dokkaHtmlPartialPlugin
|    |         \--- com.fasterxml.jackson:jackson-bom:2.12.7 (*)
|    +--- com.fasterxml.jackson.core:jackson-core:2.12.7
|    |    +--- com.fasterxml.jackson.core:jackson-databind:2.12.7 (*)
|    |    \--- com.fasterxml.jackson:jackson-bom:2.12.7 (*)
|    \--- com.fasterxml.jackson.module:jackson-module-kotlin:2.12.7 (*)
\--- com.fasterxml.jackson.module:jackson-module-kotlin:2.12.7 (*)
```

This `dokka` thing… it’s a [documentation tool](https://github.com/Kotlin/dokka) 😆.

Guess the spring framework is safe then :)

### Wrapping up

`./gradlew dependencies` -> useless

`./gradlew :project-name:dependencies` -> more useful

`./gradlew :project-name:dependencyInsight --configuration $configuration --dependency depname` -> most useful

Some silly grep with dependencyInsight -> most useful++

Build Scan -> Also good 👍

Thanks for reading!
