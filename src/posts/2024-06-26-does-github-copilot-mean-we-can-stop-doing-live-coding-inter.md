---
title: "Does GitHub Copilot Mean We Can Stop Doing Live Coding Interviews?"
subtitle: "Or that we need them more than ever?"
date: 2024-06-26
medium_url: "https://medium.com/@mckornfield/does-github-copilot-mean-we-can-stop-doing-live-coding-interviews-aca3424352be"
---

Or that we need them more than ever?

![Photo by Christina @ wocintechchat.com on Unsplash](/img/does-github-copilot-mean-we-can-stop-doing-live-coding-inter/0_mYKiSk1MQ7cNDfiG.jpg)

*Photo by [Christina @ wocintechchat.com](https://unsplash.com/@wocintechchat?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Coding interviews are a touchy subject in the software industry. They are surely game-able like any test, where enough studying and repetition can set you apart from others. (If it weren’t game-able, why would books like [this](https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850) or sites like L[eetCode](https://leetcode.com/) be so successful?)

On the other hand, if people don’t have the mechanical ability to write code (without copy pasting from StackOverflow), you might question if they’ll be able to do the job.

That being said, with the [advent of tools](https://github.com/features/copilot) that can churn out code based on a prompt or other reference, we might ask ourselves:

- Why do we do these different types of coding interviews?
- What’s good (and bad) about them?
- How Copilot or ChatGPT make these interviews more (or less) relevant

### Take Home Interview Dilemma

If you want to replicate the experience of what it’s like to write code, a take home is probably more accurate (you have focused time, without someone staring at your face or over your shoulder, to write out a solution).

That being said, take home interviews mean you have to make your own time, and are less a conversation and more of a homework assignment.

Some people knock these things out of the park, and other people don’t make/have the time. I’ve seen plenty of variety in take home coding submissions, but the reality is, these days you have the internet, Stack Overflow and Github Copilot at your behest, along with IDEs and all sorts of coding tools to give it your best shot.

Even a total noob could paste a prompt into ChatGPT and get something semi workable for a take home problem. The dilemma is then, how do I turn this into an effective filter, without saying “please don’t use all these cool tools to ace your take home problem.”

Well —

### “F — k it, we’ll do it live!”

Live coding interviews are one way around all these tools. Especially if you explicitly ban them and say “[please code into this Google doc](https://www.reddit.com/r/csMajors/comments/9rdx94/tips_for_coding_interviews_through_google_doc/).” But they present their own problems.

The worst interviews I’ve given have been live coding interviews. In my brief stint at Walmart Labs, I gave a coding interview that amounted to a [taxi cab geometry problem](https://en.wikipedia.org/wiki/Taxicab_geometry#:~:text=Taxicab%20geometry%20or%20Manhattan%20geometry,the%20taxicab%20distance%2C%20Manhattan%20distance). The details weren’t important, what *was* important is that I was in a room with someone, for 45 minutes, who refused to write a single line of code. I let this person use paper, or my laptop with an IDE pulled up, but nada. Just hemming, hah-ing and lots of thinking.

This has happened to me only handful of times, but I don’t know what causes it. Nerves? Inability?

Either way, it’s an easy interview decision ❌ but leaves you thinking there’s something going wrong with the process.

I’ve also done interviews that went *better* but still a lot of nerves and anxiety showed through, meaning the candidate didn’t really get off on the right foot, and it was hard for me to give them the benefit of the doubt with such a shaky performance.

The main problem with live coding is that it is very unlike the job itself. You are not forced to code in front of a senior person, who diligently notes all the things you’re doing with “mhmm”s and “uhuh”s. Usually you have conversations and go on and work on things on your own, or consult the internet/ use one of the Copilot tools mentioned (I’ll get to those shortly).

The reality is, live coding interviews are more like exhibition sports matches than interviews. You throw a problem at someone and see how they do within a short amount of time. I think they’re valuable (and I think the choice of a realistic problem is important), but they definitely prefer folks who do well under time pressure, which not everyone does, and people benefit heavily from practicing live coding interviews as well as practicing the problems (i.e. they’re game-able).

So are these live interviews/ exhibition matches worth still having on their own? Or are they not representative at all? Let’s ask ourselves —

### How Good are these Copilot Tools?

Very.

These days, if you’re a software engineer and you come across a construct/problem you haven’t seen before, you might consult/use a copiloting tool (ChatGPT is still free and Github Copilot is only $10 a month), something that you *definitely* wouldn’t want to allow in a coding interview.

Why *definitely?* Well, in my experience, these tools can solve coding interview problems like 🫰.

Below is me pasting [this leetcode question](https://leetcode.com/problems/minimum-number-of-k-consecutive-bit-flips/description/?envType=daily-question&envId=2024-06-24) into Github Copilot and getting the answer in under 10 seconds.

![The only problem was the missing `self` as the first arg, for the LeetCode submission](/img/does-github-copilot-mean-we-can-stop-doing-live-coding-inter/1_3saATZZfeiNdt1SXqowLxQ.png.png)

*The only problem was the missing `self` as the first arg, for the LeetCode submission*

![Submitting and passing with one minor tweak in leetcode](/img/does-github-copilot-mean-we-can-stop-doing-live-coding-inter/1_Tif-SMN5LXTqP6eF7R394A.png.png)

*Submitting and passing with one minor tweak in leetcode*

I’d heard of this bit flipping problem before, but never attempted it myself. I’m sure in an interview I’d struggle for a bit, then ask some questions. Maybe I’d do OK, but it wouldn’t be like using an LLM.

Copilot just spits out a 99% correct answer in a few seconds.

Interviewers be damned!

If you’re going to allow tools like this in an interview, you’re now asking “how good is this person at prompting ChatGPT”, not “how good are they at writing software?”

I’m not convinced the two are separable, and maybe it won’t matter in the immediate future, but…

I think the best engineers will be ones that use the tools available to them best they can, not who “craft beautiful software straight from their brains.” That being said, simply using a tool well is not all that goes into being a software engineer.

### Do We Need Better Filters?

Here are a list (in no particular order) of the things I think we need to consider that aren’t simply borne out by reviewing AI or human generated code, but that we can use to filter folks out in the interview process by digging a bit deeper.

These work regardless of the format, but require extra time to sort through.

**Understanding**

A huge part of the interview process, at least for me, is the demonstration of “understanding.” This is a loaded term, but it can amount to:

- Do you understand the code you wrote, or is it copy paste/ memorized/ ChatGPT
- Do you understand how your code scales (or doesn’t) in terms of memory, operations, CPU or GPU usage?
- Do you understand the tradeoffs between the way you wrote it and alternatives?

So much of software engineering isn’t the mechanics of writing code, but understanding why it’s good (or bad). These coding challenges or takehome problems aren’t explicit in the fact that what we should be searching for is *understanding*, not raw coding talent.

**Maintenance**

The best software I have ever seen ends up looking incredibly ugly under the hood (it handles all sorts of edge cases, or has hooks for handling them). But that software is *tested*, not just in some BDD/TDD way (automated tests are great), but it has been used by people and it works. And when it doesn’t work, then we know something about *why* and *when,* and can make the changes to make it work.

Designing coding questions around how you would maintain a system lets the engineer speak, instead of the coding robot.

**Tradeoffs**

Partly spoken about in the understanding section, but what we’re really looking for when any piece of code is written, is what tradeoffs does it have?

- Does it run faster, but use more memory?
- Does it run slower, but use fewer resources?
- How does it scale up with a higher file size/ request count?
- Do you add multiple threads/processes to handle requests? How do you handle concurrency?

All additional complexities come with tradeoffs. Being able to articulate when tradeoffs are worth their cost is something every engineer should be able to say

**Documenting**

Documentation is a sore spot in the software industry. Agile infamously says “Working software over comprehensive documentation”, though in my experience, this can mean “no docs YOLO.”

Documenting the why, the how, is critical to being part of a team, as well as creating a useful product. No product is as walk up useable as Google.com, so being concise and descriptive goes a long way.

### In Conclusion… Interviewing Stinks, But It’s Probably Not Going Anywhere

Interviewing is not a fun process. I’d rather have a magic eight ball I could shake that told me whether or not someone was a good fit (or vice versa, make my interviewer just shake an eight ball at me).

Without the paranormal powers of an eight-ball, we’re reliant on minutes or hours of a person’s time to judge if they’re worth many dollars of investment and hours of investment to become a productive employee.

I don’t think we can dispense with some form of “please code me a blah”, but maybe we can try to rely on filters like understanding someone’s code, seeing what maintenance and tradeoffs would come from it, and how they’d document the usage and other non functional requirements around it. At least these sorts of things are more reflective of a software engineer, instead of a coding robot.

I’d love to see, in a few years time, us giving coding interviews where Copilot tools are part of the process (i.e. how do you use them, and how do you respond to what they produce). But we’d have to change our filters out before we swap over to Copilot assisted interviews, which involves the hardest type of change: procedure.

Thanks for reading!
