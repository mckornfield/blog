---
title: "Explain Like I’m Five: SDKs"
subtitle: "What is an SDK (Software Development Kit?)"
date: 2022-11-28
medium_url: "https://medium.com/@mckornfield/explain-like-im-five-sdks-d44c7f5526eb"
---

![Photo by Josh Olalde on Unsplash](/img/explain-like-im-five-sdks/0_ltY6iApg51iDJlqm.jpg)

*Photo by [Josh Olalde](https://unsplash.com/@josholalde?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

## What is an SDK (Software Development Kit?)

Software is all about building blocks. You typically don’t try to implement things like sorting etc. from scratch when you go to solve a problem. You either using something built into the language (the “standard library”) or you pull down some code that someone else wrote (“third party library”).

Imagine you’re building a house. Would it make sense to try and build every single thing from scratch (like trees and raw ore?!), or maybe buy some precut lumber, some pipes, and follow someone’s “how to build a house” tutorial on YouTube?

These standard and 3rd party libraries are analogous to the prebuilt pieces you would use to assemble your house. You *could* build a house from scratch, but it would probably resemble a shack/ not be up to any sort of code that a home inspector would pass.

Now, let’s up the ante. Instead of a third party library or a standard library, what if you wanted some way to build homes that just involved customizing a few bits and pieces. Essentially most of the house would already have been built, but you could decide where to put it, what sort of furnishings it had, etc. This might sound like a fantasy to you, but [Sears actually sold these sorts of homes](http://www.searsarchives.com/homes/index.htm), back when they were a thing (RIP Sears). You’d essentially buy a “Modern Home” and have all of the pieces shipped to you. And then it was up to you to make something.

SDKs, or Software Development Kits, are essentially the Sears Modern Homes of the software world. They come with all sorts of goodies for how to talk to existing systems, so that you can build software way faster than if you had to build your house from pre-assembled parts, but still figure out how to do the “architecting” of a house. Your job with SDKs is just to plug in what specific behavior/ features you want into a predefined ecosystem.

To see it another way, if we were building with Legos, you might think of standard libraries and third party libraries as prebuilt structures you could reuse, like a wing or a wheel, but you might think of an SDK as a whole set of prebuilt or mostly built structures; a whole ecosystem of Lego buildings that you could fit together as you want or sprinkle a little bit of your own creativity into to make something new.

Let’s step away from these analogies and consider some of the more popular SDKs.

## Examples of SDKs

### Mobile SDKs

The most popular SDKs in terms of usage by developers are probably the Android and iOS SDKs. When it comes to building an application, Alphabet/Google and Apple are very incentivized to make it easy for developers to make new applications (partly because it drives the sales of their physical phones, but also because they take a [~30% cut](https://www.theverge.com/21445923/platform-fees-apps-games-business-marketplace-apple-google)). To make things easier, they offer SDKs to do so.

The Android SDK is a bit more open sourced, in that you can develop on any device (Mac/Windows/Linux) using a development tool called [**Android Studio**](https://developer.android.com/studio)**.** Android Studio itself is an IDE that You can also develop using other tools, but Android Studio is the main way developers interact with the Android SDK. What does the SDK give you? The ability to compile, publish, run and test Android applications with very little of your own code. All you need to define is what your app *looks like* and *does*.

The biggest departure for the iOS SDK is that it is more closed source, in that the only legitimate way to develop iOS applications is using a (yeah you can probably guess) Mac computer. Developing on Windows and Linux machines is not allowed, unless you do something tricky with a VM to run MacOS (which is like saying “you can develop on any machine you want, as long as it can run MacOS”). The iOS SDK is primarily interacted with via [XCode](https://developer.apple.com/xcode/https://developer.apple.com/xcode/), a Mac only IDE that parallels Android Studio, though there are [alternatives](https://www.jetbrains.com/objc/).

But what both of these SDKs have in common is that they make it possible for developers to quickly create and release apps to a marketplace that millions of folks can access. Without tools like this being available to developers, we wouldn’t have the mobile app ecosystem that we do today.

### IntelliJ Plugin SDK

As part of the Mobile SDKs we mentioned IDEs, or Integrated Development Environments, essentially places that developers write code (like VSCode, or for this example, IntelliJ). IntelliJ is probably the most widely used Java IDE, eclipsing *Eclipse*, the IDE that formerly held the mantle of “most widely used Java IDE.” All the places I’ve worked that do Java development end up using IntelliJ.

What is interesting about it is that not only is it a powerful Java IDE, but it is pretty well extensible. You can write your own [plugins](https://plugins.jetbrains.com/docs/intellij/welcome.html) to make it easier for developers to read/write/compile/run/test their code. You could add support for a [different software language](https://plugins.jetbrains.com/plugin/1347-scala), change the syntax highlighting to [use rainbows](https://plugins.jetbrains.com/plugin/10080-rainbow-brackets) to help with readability, or any other thing you can think of that you’d like your IDE to do ([maybe a different progress bar](https://plugins.jetbrains.com/plugin/8575-nyan-progress-bar)?). Just like mobile apps, these plugins have a marketplace you can push to and download apps from, all with the help of the SDK.

## Specialty SDKs, \_DKs

### JDK -> Java Development Kit

I mentioned Java as part of the IntelliJ Plugin SDK, but Java is a relatively complex ecosystem. There’s support for the Java Virtual Machine (JVM) on every machine type it can run on (Mac/Windows/Linux), there’s all sorts of different versions and slightly different tuning you can give to the JVM, and of course, there’s stupid licensing issues (yay Oracle). All of this leads to the fact that developing Java means choosing [a version and a kind](https://whichjdk.com/) of the *JDK*, the Java Development Kit. Amazon has their own, Oracle owns the “proprietary” one, and there’s an open source version (OpenJDK and now Adoptium).

What is important to note is that the later versions have newer language features that might not be present in older versions. And you might not be able to ship or build software with the closed sourced versions without getting into financial trouble. But if you ever do Java development, you’ll have to have one of these JDKs installed and configured on your development machine. Most of the time the open source solution will be the right choice, but read up on what the others are and why they exist if you’re interested.

### CDKs -> Cloud Development Kit

The last specialty SDK is one that allows you integrate with a cloud provider. Instead of something more low level like an application that folks can download, or what version/ type of Java people are running, this SDK is for how you provision and control cloud resources.

The most famous example of this is probably the [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html). They have support for the most common languages, but doing something like creating an s3 bucket looks like so:

```python
bucket = s3.Bucket("MyBucket", bucket_name="my-bucket", versioned=True,
            website_redirect=s3.RedirectTarget(host_name="aws.amazon.com"))
```

Granted, there are alternatives to these CDKs, like using something like Terraform (which is written with [jsonnet](https://jsonnet.org/), blegh), but even [Terraform has a CDK](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-build) so you can write code in a language of your (limited) choice instead of the standard (blegh) way you’d write Terraform.

In closing; SDKs are the prebuilt interfaces and tools that you can use to make applications and systems quickly with as little code as possible.

Thanks for reading!
