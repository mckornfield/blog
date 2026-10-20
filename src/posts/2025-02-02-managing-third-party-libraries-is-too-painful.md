---
title: "Managing Third Party Libraries is Too Painful"
subtitle: "And weakly languages are the worst offenders"
date: 2025-02-02
medium_url: "https://medium.com/@mckornfield/managing-third-party-libraries-is-too-painful-5fe54f193b22"
---

And weakly languages are the worst offenders

![Photo by 愚木混株 cdd20 on Unsplash](/img/managing-third-party-libraries-is-too-painful/0_d8OWWB3UCND1lGKa.jpg)

*Photo by [愚木混株 cdd20](https://unsplash.com/@cdd20?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Getting Started in Software can be Painful

A friend of mine recently was trying to port a project he’d been working on from .NET to Typescript, and wanted to use [tauri](https://v2.tauri.app/) to do so. He used the docs and Claude/Gemini/ChatGPT to assist him on the move, but kept running into walls.

I got him set up after messing with his setup for a bit (reinstalling `nvm` and a handful of other packages, as well as following an upgrade guide to get the sample app working), but he had spent days fighting the setup and getting nowhere.

After all of this he made a really good point:

> I don’t want to get held hostage by all these random packages conflicting, especially if I have to do some sort of upgrade down the line and hit the same wall.

This is a pretty gruesome problem in software development. It comes down to —

### Package Management, in General, is Hard

Though some languages are much better at this than others.

Golang seems to have a pretty solid way to manage dependencies, even though my early experience with it was that it was sort of bunk (this was before `go.mod` , i.e., before 2018). Basically it can pull all the various versions and load whatever is needed into the binary at runtime.

But it and Java are the only two languages I’ve found that have pretty solid support for handling versions of the same dependency (Java has a more elaborate way to handle conflicts, with [shaded jars](https://stackoverflow.com/a/49811665)).

On the opposite end of the spectrum are my favorite languages, Python and Javascript/Typescript. I like them because Python is great for quickly working out a solution (scripting king), while Javascript is the language of the browser, but can also run on a server via Node.

They also have the most frustrating package management structures.

Both of these languages are structurally typed/weakly typed, meaning there’s no “compilation” step (technically Typescript introduces one, but ultimately packages can be Javascript OR Typescript).

This leads to not only confusion but just makes third party dependency management *painful*. Weak typing means that errors that would normally be compilation errors become *runtime* errors, which means “your app no worky.”

But before hammering these weakly typed languages, it bears repeating that all these other languages can have their flaws when it comes to package management. Let’s start with —

### Exhibit A: Log4Shell and similar CVEs

![Log4shell ruining the holidays — Source](/img/managing-third-party-libraries-is-too-painful/0_9prlESrWzLr5-yTV.jpeg.jpg)

*Log4shell ruining the holidays — [Source](https://blog.devgenius.io/log4shell-as-explained-by-metaphor-and-memes-38de224a2eb7)*

Back in 2021, there was a pretty nasty vulnerability, [discovered by Minecraft users](https://www.npr.org/2021/12/10/1063278227/minecraft-software-flaw), in the `log4j` Java package.

In Java, log4j is one of the most ubiquitous libraries; if you didn’t use it directly, chances are you depended on a project that DID use log4j. It’s nothing more than a fancy printing tool, a logging library.

Upgrading it where I worked was pretty painful, as we either forced dependencies (i.e. possibly breaking dependencies that relied on older versions), or we went and upgraded a cavalcade of dependencies across our stack of Java projects.

After all of this, there was still some weirdness where Amazon was placing a “hotpatch” jar file to protect against this exploit, but this broke one of our other dependencies that was confused why a jar file kept appearing and disappearing, corrupting the boot up of one of our apps.

This is all to say: what a crappy month December 2021 was for any decent size Java shop, all for a *logging library.*

### Exhibit B: The Javascript Ecosystem

There are numerous examples of the JS ecosystem being turned upside down because of a problem with a software package.

It’s to the point of being stupid, like one developer pulling `left-pad` and [breaking all sorts of packages that depended on it](https://www.theregister.com/2016/03/23/npm_left_pad_chaos/), or this developer [pushing a version of the library with files deleted](https://www.bleepingcomputer.com/news/security/big-sabotage-famous-npm-package-deletes-files-to-protest-ukraine-war/) to protest the Ukraine war.

There’s basically [one meme](https://xkcd.com/2347/) that explains it all, which is that a sufficiently sprawling set of Javascript dependencies looks like a jenga tower.

![Photo by Valery Fedotov on Unsplash](/img/managing-third-party-libraries-is-too-painful/0_UY0NPUI-aKJ-M_O9.jpg)

*Photo by [Valery Fedotov](https://unsplash.com/@imlst?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

To the point made earlier, a lot of folks can be held hostage by simply relying on npm as is, and not doing what larger companies do, essentially hosting their own mirror of things and vetting packages in a more rigorous way than simply downloading the latest patch version.

If you’ve ever looked at `package.json` file, they can look like the following ([from the npm docs](https://docs.npmjs.com/about-semantic-versioning)):

```json
"dependencies": {
  "my_dep": "^1.0.0",
  "another_dep": "~2.2.0"
}
```

That caret (`^`) means any minor release, and the tilde (`~` ) means any patch release, so if you rerun the lock command, you will just get the “latest and greatest” along those release lines. That’s good until, well, someone doesn’t properly follow semver and releases an incompatible change that your weakly typed language won’t catch (darn), or worse, a [compromised version of the package is pushed](https://www.aquasec.com/blog/npm-supply-chain-attack/).

Javascript dependencies are a wild west, but in my most recent experience, the worst set of dependencies are

### Exhibit C: Python ML Libraries

I won’t belabor the point, Python package management is already bad. Python is always weakly typed; you can use type hints but they aren’t necessarily enforced, especially with dependencies.

This gets us into a state where conflicts can be problematic (and only manifest at runtime) just like in Javascript, but one of Javascript’s saving graces is that it just has to run within the browser or Node runtime.

As Python has become the *lingua franca* of the ML revolution, we’re tasked with interacting with a set of devices that we’ve all come to know very well since their crypto days: GPUs.

This means many, many GB of NVIDIA drivers installed, making sure the ones included with `pytorch` or `tensorflow` work, but even worse, the libraries built on top of these have byzantine install patterns, requiring an expert in jenga to arrange a functional Python installation.

Python’s version differences and packages being tied to those versions (e.g. `my-package-1.0.0-cp39…` ) is another point of irritation layered on top of the madness that is ML library package management.

I’ve gotten many of these things to work after a time, and have seen my coworkers go down very manual paths to get installations and versions properly set up, but, it just shouldn’t be that hard to use the GPU, should it?

### The Plaintiff Rests

I can’t honestly argue that we should just ditch 3rd party dependencies. So much of what makes software development possible is that every company is not rediscovering how to build things from the ground up, and creating all of their own sets of problems.

But the madness of logging libraries that can be exploited, Javascript dependencies that can become a hostage crisis, and the amount of blood, sweat and tears that goes into getting these ML libraries to work to me seems, well, stupid.

The software world should be accessible for people to get started, without creating enormous amounts of busy work or opening up companies to attacks for the pleasure of a logging library or some padding.

I can only hope that the dependency management of the future is less of, well… a 🗑️🔥.

Otherwise we might well have to reinvent the wheel at every company, startup and solopreneurship to avoid being held hostage.
