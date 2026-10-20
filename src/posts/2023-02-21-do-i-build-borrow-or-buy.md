---
title: "Do I Build, Borrow, or Buy"
subtitle: "Every software developer’s dilemma, and when each option makes sense"
date: 2023-02-21
medium_url: "https://medium.com/@mckornfield/do-i-build-borrow-or-buy-d74b42ce3e62"
---

Every software developer’s dilemma, and when each option makes sense

![Photo by Jon Tyson on Unsplash](/img/do-i-build-borrow-or-buy/0_2aE1iLAFG5X1ZSs8.jpg)

*Photo by [Jon Tyson](https://unsplash.com/@jontyson?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

## The Software World is Full of Hidden Tradeoffs

Every day, millions of people make decisions based on weighing positives and negatives.

Tradeoffs are inevitable in all actions we take, but the physical world mostly does a good job of showcasing the tradeoffs to you.

The virtual world is not so kind.

Costs can be temporally separated from the value; so you think you made a good trade in the moment or in the short term, but in the long term you create an even higher cost/ more heartache than alternatives might.

Let’s see reasons for or against why you might…

## Build

People like to build things. Creativity is part of what makes us human. This might be the single best argument for building; it aligns with what we as a species naturally want to do (besides destroy, which is also pretty human).

When you build something you feel *ownership*. You want to protect and preserve the thing that you built. You’re *invested.*

Another very good reason to build is because you *can’t* borrow or buy it.

You have expertise above or beyond others, or there is too much context specific information for what you’re trying to build, that borrowing or buying is just going to be an exercise of shoving a square peg into a round hole.

Lastly, when it comes to software, what you build yourself should be the main way you give value that other folks cannot. That is to say what you build should be *novel,* or at least a *novel approach* to a known problem.

A novel approach might also be something that is unsolved (i.e. no one has built anything quite like it), in which case you should build, but be careful, since you’ll more be building by necessity than by choice.

An example of building would be: if you’re Snapchat, you build a platform for people to exchange photos and videos. That’s why people use you.

To summarize, you should build because:

- You are naturally creative and want to build
- You’ll feel more invested/ want to own the result more
- You’re capable of building something better
- You’re making something novel, even if it’s novel by manner of degree

## Borrow

As context: so much of the software world is built on “open source” source software.

The type of free that characterizes open source is “free as in speech,” or “libre.” This is software that you are [*allowed* to borrow](https://www.apache.org/licenses/LICENSE-2.0) (or “use”) any way you like, with the ability to modify it if you need to.

The value of borrowing these software packages is that someone or some group of people acted as experts to design a solution.

These people can also maintain the system for you (or you can contribute back any changes). This offloads some maintenance to experts.

Vulnerabilities are a double edge sword for these open source solutions, as they are usually patched frequently, but heavily used packages (e.g. [log4j](https://en.wikipedia.org/wiki/Log4Shell)) can become targets for attackers.

You can install the open source package as part of your new software solution (i.e. a dependency for what you *build*). They are the pre-made tools that you use to make headway in the software world, without reinventing the wheel 30 times.

A word of caution about open source solutions: they are not all created equal. Seeing how recently maintained, how well patched (they *too* can depend on OS solutions) and how many issues exist are good proxies for the quality of an OS product.

An example of borrowing would be: you use the OpenSSL library to handle TLS certificate verification/exchanges. Cryptography is not only hard to get right, but dangerous to get wrong.

To summarize, you should borrow/use OS when:

- You want to use what experts have built in the open, and at low/ no cost
- You want to offload maintenance of a part of your solution to a community, with the option to give back
- You want to use a system that transparently deals with vulnerabilities/exploits
- A well maintained and useful solution exists

## Buy

The main disadvantages to building and borrowing are on the accountability side of the house.

When you **build**, *you* and your team are accountable. You must maintain the product you built and probably no one else will help you (unless you transition it to be open sourced, which is a whole different ballgame).

When you **borrow**, a more nebulous group of developers are accountable (“a community”), but ultimately you and your team are still responsible for issues that affect your software and customers directly, regardless of its ultimate source.

**Buying** is where you make the ultimate tradeoff: I am willing to pay someone to manage as much of this (sub)system as possible, so that I can spend my time *building* something useful, and still *borrowing* in cases where there is a good open source alternative.

You buy because you’ve weighed the maintenance burden of the other options against the added cost of paying for a solution.

Buying can seem like the tougher tradeoff, because the maintenance costs of the other two answers are nebulous/ farther off, AND because spending money isn’t always *money* *well spent*.

But if you come across a good product that costs money, it’s worth assessing how much money it would cost if you *didn’t* invest in it.

So much of the downside in building or borrowing is where the accountability and maintenance burdens fall (on you and your team), and how that presents an opportunity cost: **The time you spend *maintaining* a system you built or borrowed is time you *cannot spend* building something new.**

Your time and your organization’s time is finite, so where you provide value is where you should spend your time building, and where you *don’t* provide value is where you should be borrowing or buying.

An example of buying that is commonplace in the software world: server maintenance. Public cloud providers like AWS, Azure, GCP are the best examples of buying in the software industry. Few people want to build a complex software solution AND maintain the servers that power it.

You buy because you:

- Have found a product better than one you can build yourself or borrow
- You want to shift the maintenance burden completely onto the vendor you buy from
- You want to spend as much of your time building something of value, and as little of it as possible in maintenance mode

### In Summary

I thought it might be a bit tongue and cheek to summarize this as a set of if statements, so here we go:

```go
 if weAreTheExperts() &&
  itFeedsOurCreativeDrive() &&
  weWantToBeMoreInvested() &&
  weAreMakingSomethingNew() {
  Build()
 } else if aGoodOpenSourceVersionExists() &&
  weWantToOffloadSomeMaintenance() &&
  goodPatchingExistsForIssues() {
  Borrow()
 } else if aGoodPaidSolutionExists() &&
  theMaintenanceTradeoffBeatsCost() &&
  youWantToMaximizeBuildingElsewhere() {
  Buy()
 } else {
  BuildCarefully() // Out of options!
 }
```
