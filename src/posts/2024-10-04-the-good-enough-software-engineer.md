---
title: "The Good Enough Software Engineer"
date: 2024-10-04
medium_url: "https://medium.com/@mckornfield/the-good-enough-software-engineer-abd32fa6622c"
---

Don’t waste time on things that no one uses, or wants to use

![Photo by Ralf Knüfer on Unsplash (Those poor, unwanted boats)](/img/the-good-enough-software-engineer/0_yLLsvT_R7Yz36689.jpg)

*Photo by [Ralf Knüfer](https://unsplash.com/@textstation?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (Those poor, unwanted boats)*

In my limited time working in software , I’ve realized that taking a step back is usually more useful than coding up an algorithm. These days you can just use [ChatGPT or Claude for those algorithm problems](https://hackernoon.com/testing-llms-on-solving-leetcode-problems), so people who work with software should be used for something more, right?

One thing that we as people (currently) have over these LLMs are our value judgments, i.e. that someone will use the code we‘re writing, and that the code is *good enough* to accomplish whatever it is the person will use it for.

In other words: “we’re doing something of value, and it’s *good enough*”.

Let’s look at some ways failing to step back can go wrong.

### Don’t Build the Metaverse

Let’s blow things up to the business level and put down the keyboard for a minute. Let’s take Mark Zuckerburg’s white whale, [the Metaverse](https://www.bbc.com/news/technology-66913551).

What problem does the Metaverse solve? What customers does it draw in? How good is good enough?

The answer to these questions, from my perspective, is:

¯\\_(ツ)\_/¯

But the market has spoken so far.

[The Metaverse has cost Meta billions of dollars](https://www.businessinsider.com/charts-meta-metaverse-spending-losses-reality-labs-vr-mark-zuckerberg-2022-10) to make, creating an operating loss of $30 billion dollars.

Now let’s zoom back in to the day to day: Rule #1 of being a *Good Enough* Software Engineer is: “Don’t build a thing that no one wants to use”.

It’s really the first rule of anything, but I think this is more of an insidious problem in Software Engineering.

Let me explain.

### Understand that Most Software is Unwanted

Every moment of every day, someone is writing a terrible software program.

Whoever’s writing it might be learning, or just not very good. I’ve been guilty of this many times, probably even in the last 24 hours. I’ve written terrible code, and I’m not proud of it.

It can be copy pasted from the internet, taken from an LLM, or straight out of documentation/ a textbook.

But low quality is not the arbiter of whether or not something is *wanted*.

By default, ***no*** *software is wanted*.

No one wants Windows 11. Or Mac OS X. Or anything up or down the stack. These aren’t inherently good things, like a hamburger, or a hotel on the beach. These are complicated sets of instructions that power machines to do complex tasks.

Time travel to 1800 and give someone a Windows installation guide; they’ll assume you’re nuts. No one wants these software packages on their own.

What people *do* want is something the software can provide, a concrete joy or advantage from their software. People want to listen to music. Or read the news. Or write and communicate. These are things that software can enable, *and* are things people want.

But the software ecosystem is vast and full of dead ends. Millions of lines of code have been written that aren’t used or wanted by anyone, because they power obsolete systems, or because they represent crummy products that *don’t* meet people’s needs or wants.

It’s hard when buried under design documents, Agile processes, JIRA tickets, and a decent paying job to be introspective. But you’ll find over time that building something that no one wants isn’t good for you, your career, or your company.

*Most software is unwanted*, so before writing a single line, stop and think “Would anyone want this? Would I even want this?”

If the answer is no, then it’s time to use the engineering side of your brain to figure out why you’re writing something that *you* don’t even want. And how to change it to be something at least you want.

That could be done by:

1. Changing the requirements; maybe it’s something specific about what you’re building that makes it unwanted
2. Focusing on quality over quantity; reduce the number of things the software does so that it can do fewer things better
3. Not doing it: going back to Rule #1, don’t build an unwanted thing that you can’t mutate into something wanted

Sometimes you build things just to learn, as I talked about in the beginning of this section. The want there is generally speaking *to learn*. That is probably the best reason to build something no one else will want.

Rule #2: Understand most software is unwanted; your job is to build something good enough that someone, starting often with yourself, would want to use.

### Good Software Meets a Need

If someone has a problem, and there’s an app, or an API, or a SaaS product that meets the need, and does so with little friction (for a “fair” price), you’ve entered the realm of *meeting a need*.

A ton of software serves to solve individual problems people have even *within* the software community, like [build tools](https://www.gnu.org/software/make/manual/html_node/Introduction.html) or [IDEs](https://www.jetbrains.com/ides/).

If you have a project, or a ticket to work on something, make sure that what you’re working on meets a need. The minute it doesn’t meet a need that someone has (including yourself), you should consider doing something else.

If you think of the most successful software implementations, you might think of Google (free, near instant search) or Facebook (free socializing online) or Netflix (a sea of instantly available content).

The needs that they met came first, and then all the [crappy ads and tracking came later](https://doctorow.medium.com/the-specific-process-by-which-google-enshittified-its-search-1ffd3b02d205) so these companies could become profitable monopolies…

But that’s a different story, the important takeaway is the meeting the need part, i.e.,

Rule #3: The need should determine what program you build, not the other way around.

### Being Good Enough: Avoid Bikesheds

A common term you’ll hear in software development is “bike shedding”. The origin of this is something more physical, namely focusing on what [color a bikeshed is instead of something more pressing (like operating a nuclear plant)](https://en.wikipedia.org/wiki/Law_of_triviality).

The most important part of the “enough” piece of “good enough” is drawing lines. Accepting that your program can’t do everything, *won’t* do anything other than what it takes to meet a need.

Another bikeshedding analogy I’ve heard is from a Chinese proverb: 画蛇添足 (draw snake, add feet). The tl;dr version of [the story](https://zhiminzhan.medium.com/chinese-idiom-stories-for-software-professionals-24-to-draw-a-snake-with-feet-%E7%94%BB%E8%9B%87%E6%B7%BB%E8%B6%B3-19272c5e2b47) is: a person is tasked with drawing a snake, finishes, and decides to keep drawing by adding feet. But the important point is that snake don’t have feet; by adding to the drawing, he made things worse.

In programming this can take many forms, but the best examples of bikeshedding I’ve seen:

1. Adding lots of slow/non functional tests to a feature (of questionable value)
2. Spending lots of toil to maintain (and create more) fragile tests
3. Building out frameworks before you have even *two* separate uses of it

Conversely, I’ve seen these programs not meet a need and be highly unusable, maybe because of time spent on the bikeshed, but mostly because people ignored this rule:

Rule #4: Stop and go no further when you’ve written something good enough. Avoid working on building out the bikeshed while other things languish.

### Summary

The rules to being a good enough software engineer

1. Don’t build a thing no one wants to use.
2. Understand that all things are unwanted by default; if you’re building something that even you don’t want to use, see what you can change or see rule #1
3. The need should drive what you build, not the other way around
4. Don’t add any more to a program that is good enough
