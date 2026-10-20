---
title: "The Death of the Entry Level Developer"
date: 2025-02-25
medium_url: "https://medium.com/@mckornfield/the-death-of-the-entry-level-developer-747523fec47b"
---

Algorithms and data structures aren’t going to cut it

![Photo by Joy Real on Unsplash](/img/the-death-of-the-entry-level-developer/0_mZ_Qy-vONJmwcVRw.jpg)

*Photo by [Joy Real](https://unsplash.com/@joyreal328?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### The AI driven hiring freeze

I’ve worked at a startup for over two years, and the number of entry level developers/interns we’ve hired is:

**0**

All of the engineers we’ve hired have been developers for at least 3 years, if not 5–10 years or more. At the mid-size company I used to work, and at companies across the industry, there have been plenty of layoffs. I don’t know the exact drop in “entry level developer” postings, but here they are overall compared with regular postings on indeed.

![Software postings in blue, all other postings in green (Source FRED )](/img/the-death-of-the-entry-level-developer/1_y2u7abutK4972HeZM4cx0w.png.png)

*Software postings in blue, all other postings in green (Source [FRED](https://fred.stlouisfed.org/graph/?g=1b7Xw))*

I’d say there is the obvious cause of layoffs implied by this graph: overhiring during COVID being corrected for afterwards. But I think the more “cultural” factor driving this plunge in open job postings is NVIDIA’s favorite two letters. (Hint: it’s in the section title)

There exists the (possibly true) assumption that AI can code well enough that we can just make the senior staff more productive instead of hiring more junior staff.

It’s like how, 200 years ago, 90% of people in the USA farmed. Now it’s less around ~1%, and they farm more effectively than the super agrarian societies of the past. The reason?

![Photo by Dietmar Reichle on Unsplash](/img/the-death-of-the-entry-level-developer/0_iugka-Z2Aw0NZqio.jpg)

*Photo by [Dietmar Reichle](https://unsplash.com/@dietmarreichle?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Arguably that one guy is doing the work of tens or hundreds of people, but one could argue that he’s *better* than the equivalent number of people, for this specific crop, because there isn’t the need to communicate.

### The Mythical Man Month and Communication Woes

When you hire and staff a software engineering team, productivity doesn’t shoot to the moon. The more engineers you tack onto a project, the effort [that’s spent communicating grows at a faster rate than productivity](https://www.smashingmagazine.com/2020/01/mythical-man-month/#:~:text=The%20contention%20in%20the%20Mythical,that%27s%206%20lines%20of%20communication.). This in concert with a set of factors (time to ramp up, differing skillsets, differing communication styles) means that you take a hit initially when you add developers to a team.

Add onto this the reality that a developer who has their first full time job has probably not coded on a “true team.” This means that even if they had internships or jobs before, they were most likely off to the side, and not privy to the work of the senior developers. This means that on top of learning how to gel with the team, the junior developers have to “learn the ropes.”

### What Does it Mean to “Learn the Ropes”?

Basically, everything not covered in significant detail in a Computer Science/Engineering major. A short list might look like the following

- A complicated git workflow (merges and rebases)
- A complicated CI/ release pipeline
- Containerized environments (lambdas, Kubernetes)
- Architectural review and planning
- Reviewing/editing other people’s code (code archaeology)

The thing all of these have in common is that

1. A senior engineer knows them
2. A junior engineer (most likely) does not

Unfortunately the add of a junior engineer is often in the future, and their immediate add is generally another brain to churn out code.

Which brings us back to the tractor metaphor

### AI: The Tractor of Software Development

The analogy is probably a bit tenuous, but the reason that a farmer now is 100x more productive than a farmer 200 years ago is because of millions of dollars worth of equipment they can buy/rent/lease to tend to their fields. Instead of coordinating an army of farmhands to pick crops or work sickles, the farmer hops onto his sophisticated piece of farm equipment and goes.

For a senior developer, there oftentimes is the understanding of “what” and “why” things need to be built, but the “how” is something that can involve consulting documentation, testing things out or searching Stackoverflow.

An LLM with decent coding chops can turn this how into a simple answer: “ask Copilot/Claude/ChatGPT.”

A farmer who is riding his tractor knows what (the crops he can farm with the tractor) and the why ($$$), just as a senior developer knows the what (this ticket/project that he’s been put on) and the why (hopefully $$$).

The problem is that the how pre 2022 would have been “get some more developers on it.” Artificial brains just weren’t good enough for the “how.”

But now they are.

### The Arrogance of Thought Work

For most of AI’s existence, it was assumed that the first thing that would be replaced would be *manual labor.* Turns out you can replace *some* of it with tractors and assembly line robots, but moving in a dynamic 3D space without breaking things is a pretty tough problem in robotics.

Turns out that, given all of GitHub, StackOverflow and Reddit, you can create a pretty darn good LLM that can produce working code. Given more compute and time, you can produce an LLM that not only produces code, but explains why code *doesn’t work.*

Recently I was fighting Google’s `bazel` build system and simply handed Claude my errors and `BUILD` files. Claude didn’t solve the answer, but it helped get me on the path to the “how.” What would have been a [rubber-duck exercise](https://en.wikipedia.org/wiki/Rubber_duck_debugging) became a few back and forths with a chatbot.

I don’t pretend like I’m a super genius (I am definitely not), and I in fact believe that a ton of what any thought worker does can be replaced by a sufficiently advanced system. Lawyer, doctor, coder, we’re all just producing thoughts, either written or spoken.

If the machines aren’t there already, they will be very soon. Sucks to be a junior developer now… or does it?

When one door closes, another opens.

### The Birth of the AI-powered Developer

When I’ve used any of the AI assisted coding tools, I think the tractor analogy is relevant once again. I can’t just throw Claude at our internal repository, with a JIRA ticket and some git credentials and tell him to “go ham.”

Claude or its equivalents can produce decent code and guide me around, even teach me how to use the tools given enough time, but Claude doesn’t necessarily have the “why” or the “what”.

If you want to get hired in the “AI can do it” economy, the best way is to build something with AI and figure out what it *can’t* do. The short version of what it can’t do: solve human problems beyond the chat interface.

Find problems in your own life or in someone else’s and use AI (assistant or as a backend) + software to solve it.

Use it as your ally, not as your enemy, and go from “junior developer” to “AI-powered developer.” The world doesn’t need more big tech company junior developers, it needs more “army of one” disruptors, using the best coding assistant tools ever conceived.

Thanks for reading!
