---
title: "Software Development is an Endurance Sport"
date: 2024-12-06
medium_url: "https://medium.com/@mckornfield/software-development-is-an-endurance-sport-2e07c983aa59"
---

Good software is well worn

![Photo by Sopan Shewale on Unsplash](/img/software-development-is-an-endurance-sport/0_BjYXpfrlcB8xoWBT.jpg)

*Photo by [Sopan Shewale](https://unsplash.com/@sopanshewale?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### “If You Haven’t Tried It, Assume It’s Broken”

[Bad software is untested. Good software is well tested](https://sre.google/sre-book/testing-reliability/).

Testing can be manual, automated, or something weirdly in between. But testing is an exercise in *endurance*, not in speed. Does the code hold up under conditions it’s supposed to

The best software I’ve used is software that is far removed from the person who wrote it.

This isn’t a pitch for quality engineering, or any amount of manual bubble wrap (though they can certainly help), but a pitch for the fact that good software is put through the ringer. What I mean by “removed” is that the software can stand alone, and it stands multiple tests:

- The tests of limits
- The tests of usage
- The tests of time

All of these things lead to the fact that good software, and therefore software development that’s worth a damn, is an endurance sport.

### Limits — “Man’s Gotta Know His Limitations”

After Dirty Harry/ Clint Eastwood beats the bad guy in the second Dirty Harry film, [he utters this line](https://www.youtube.com/watch?v=CG2cux_6Rcw). Knowing limits is a key part of being a good piece of software.

All software has limits. It will run with only so many times before breaking down, or with such an input size before breaking.

Good software doesn’t throw something like a [buffer overflow error](https://en.wikipedia.org/wiki/Buffer_overflow) and throw its hands up. It knows what the limitations are and is prepared for them. That preparation might just be failing in a more graceful way, or better yet, refusing to accept input or load that will break the system.

A good piece of software knows that it can’t process your request, and doesn’t simply try and crash. It knows (and ideally enforces) its limitations.

Endurance athletes know that they can go another mile, or that they can’t. To push farther they realize it takes effort, but that they can’t just miraculously run farther or faster without putting in the effort. They’re defined by their limits, and their ability to push them.

### Usage — Well Used Software Provides Good Feedback Loops

If only a handful of people use a piece of software, the feedback loops can be difficult to tease out. A small number of people have opinions that may or may not give useful information on what is going right and what is going wrong with a piece of software.

But as usage of a piece of software takes off, you can rely on bigger usage patterns (what functions/pages/systems are hot and which are not) as well as get enough of a quorum to know when there are true issues in your system.

Usage can be manual (yay users) or automated (CI, canaries, synthetic tests). Either way, both pieces of usage give signals on whether or not things are working. Usage with validated measurement is the gold standard of a software system (e.g., tests that pass/fail, alerts that fire when things go wrong for users).

Running a few miles a week is nice, but to train up for a marathon, you’re running basically that full marathon spread out over the week, every week, for months. More ideally, you’re measuring the time it takes and trying to bring that down.

Every measured step is a vote for the faster runner, just like every line of code executed (and measured) is a vote for a better piece of software.

### Time — “Old Software is Good Software”

[Adam Tornhill has an interesting book](https://www.amazon.com/Software-Design-X-Rays-Technical-Behavioral/dp/1680502727) on strategies for how to fix tech debt, but he also calls out a really interesting phenomena for software. The phenomena is: old software is good.

How does he come to this conclusion? The answer boils down to the three ages of software, which are:

- New
- “Middle Aged”
- Old

To zoom out, software is a set of instructions for a machine. The best software is a set of instructions that knows its limits and usage, it has no need to change. If the limits and usage are constantly changing, the software will be new or “middle aged”.

New software is full of bugs (we don’t know its limits, and we don’t know its usage patterns), which get hammered out as more changes to the system are introduced to stabilize it.

Eventually, the software reaches a “good state”; it does what it needs to and the set of changes are minor or maintenance-level. This software is considered “old.”

What about “middle aged” software? The reason I’ve quoted it is it’s not exactly middle aged, rather this is software that might be old, but has bits of newer code injected into it. It has the worst of both worlds, it’s both buggy (like new software) and it’s hard to understand for developers (one of the downsides of software being “old”).

Slapping something together in a hackathon is nifty, but spending hours debugging and improving a few lines of code is the brick and mortar of a good software system; it’s the time put in at the trick.

To take the analogy to an athlete: endurance is a measure of the time you put into growing your vascular system and muscles.

The other side of usage is time; the minutes, hours, and days spent moving your body build not just a muscle, but they wear a groove in who you are. You know your limits and you have these layers and layers of usage that have built you into an athlete.

An old endurance athlete might not be as fast as someone who’s brand new, but they will be more consistent and reliable, which is ultimately what you want from an athlete (and a piece of software).

### Summary

Software development is an endurance sport.

Knowing and pushing the software’s limits, through increased usage and time spent improving it produces a software system that is definitionally “good.”
