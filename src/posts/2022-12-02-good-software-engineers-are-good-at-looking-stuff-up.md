---
title: "Good Software Engineers are Good at Looking Stuff Up"
date: 2022-12-02
medium_url: "https://medium.com/@mckornfield/good-software-engineers-are-good-at-looking-stuff-up-52a60b238d00"
---

If you’re not using Google, you’re wasting people’s time.

![Photo by sarah b on Unsplash](/img/good-software-engineers-are-good-at-looking-stuff-up/0_t_goF7EkvywJGDMJ.jpg)

*Photo by [sarah b](https://unsplash.com/@sixthcitysarah?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Some differences between academia and the industry

There are many disparities between academic software development and “real” (industry) software development. A short list of things you only do in the industry:

- You work with other people for most things, not just some token group projects
- You write tests (gasp)
- You (most likely) commit code to a source repository instead of just having random files on your machine
- You do things in “the cloud,” not the comp sci departments’ bizarre VM setup

But the biggest disparity I’ve found is that folks within academia (and not just computer science departments) are really against looking up the answer.

- *Your code must be original.*
- *If you submit someone else’s code, the council of honor will get on your a$$*
- *Using another student’s code is NOT ALLOWED.*

But that’s bologna. People in the real world don’t write everything from scratch. People are not graded in real life because they memorize facts, they get paid to solve problems.

### “An Exercise”

Let’s give an example of how you might solve a problem as a software engineering student.

Your teacher gives you a prompt, let’s say, generate a PDF from some data. They tell you exactly what language to use, what format it needs to be in, how to submit it, what tests it should pass, and of course, NO CHEATING. They give you a “library” that does some PDF things, but it’s old and junky and some grad student wrote it.

So you dig around for a while on this code, and maybe after hours of toil, and some begging at office hours (but definitely not talking to your classmates if you don’t want HONOR COUNCIL JUSTICE), you submit some code.

Amazing, you just solved the same problem that 50+ other people have done with a bunch of tight constraints.

Imagine a more contrived scenario, where you have to write some pseudocode on a test. If you wrote good psuedocode, congrats! You proved you can memorize how to write something that doesn’t really do… anything. I mean it is *psuedocode.* Sure it might demonstrate some level of understanding, but software engineering is about *solving problems*, not demonstrating understanding.

This is not to be disparaging to academia, but there is really a… gap between how solve problems in academia and how you solve problems in the industry.

The real world is a lot messier.

You’re going to get a very narrow or very wide set of constraints based on where you work, but no one is going to tell you “no cheating.” In fact, there will probably be the opposite problem.

You’ll have no idea what’s going on and you’re going to have to look EVERYTHING up. Let’s say you’re given the same prompt, but now you have to use customer data to generate a PDF. And that data has to be encrypted, the PDFs can be redownloaded, etc. Some questions to start might include:

- Which third party library should I use? (Search around on GitHub, PYPI, StackOverflow, MavenCentral).
- Does someone already have a snippet for how to do this I can use as a reference (in the company, outside of the company?)
- How do I do this random thing in Python/another language? (Just use StackOverflow or the docs PLEASE)
- What database/object store should I use?
- What’s the right security model for something like this?

The closest problem you run into for “no cheating” is licensing, which is a pain in the software world. There are tons of different licenses and ones that sound the same (like [GPL v1 vs v2](https://en.wikipedia.org/wiki/GNU_General_Public_License#Version_1), woof). But also there’s tons of Apache 2.0 goodies that you can use as a business and not get in trouble, so yay that.

### So many choices: what do I do now?

In this world of choice paralysis and licensing, what makes a good engineer?

Someone who can look up a “good enough” answer quickly and get something working.

Someone who hits their hammers with nails and puts their flooring down with rubber mallets.

And when they don’t know something, they ask someone they work with or they Google it. Then they find the right hammer or mallet they need for the situation.

The best developers I’ve seen admit within a few seconds/minutes that they have no idea what’s going on, then spend their time researching (ahem, Googling) solutions, trying things out, and rinsing and repeating. Eventually they become the people everyone else goes to for help, because searching for useful information is a skill you have to grow.

They won’t send you a paragraph or an essay if you ask for help, they’ll just shoot a link at you. (“Oh how do I convert this PDF into an image?” “What about this [StackOverflow post](https://stackoverflow.com/a/61833151/10061484)?”)

You really can’t fit all of the information in your brain for how to work with software systems. There’s too dang much out there.

People don’t get hired because they know how to code algorithms from memory (OK well some companies do hire people this way, but it’s BS), or how to use a library without reading its docs.

Software Engineers get hired to solve problems. If you don’t know something, great, you can look it up. This industry is about solving problems without breaking the law (yay licensing), but everything else is on the table. Your grade is whether or not customers use what you make. And the time you spend not looking things up and doing mental gymnastics is time your competitors are racing past you with the help of all the developers on the web.

Don’t know the answer? Or where to start? IDK Google it or something.
