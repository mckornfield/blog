---
title: "The Last Mile in a Software Solution is the Longest"
subtitle: "Last-minute integrations take longer than a minute to do"
date: 2023-06-15
medium_url: "https://medium.com/@mckornfield/the-last-mile-in-a-software-solution-is-the-longest-4d196f9c598b"
---

![Photo by Mark Chan on Unsplash (or kilometer)](/img/the-last-mile-in-a-software-solution-is-the-longest/0_hjMXDs94IOM3srhJ.jpg)

*Photo by [Mark Chan](https://unsplash.com/@markcjn?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (or kilometer)*

## No Size Fits All

One of the most striking things I’ve found in my short software career (&lt;10 years) is that software projects, be they internal tools, or customer-facing applications or solutions, are notoriously hard to estimate.

There have been many things written about this estimation dilemma, including why Agile will save us all (haha) or why Waterfall is bad (sure, but who’s arguing that it’s good?).

From my perspective, there’s a lie that permeates this industry, which is that you can shift left on *new* software solutions.

This means testing, iterating, and finding problems earlier in a development cycle. Getting things ironed out before they hit a production phase.

I think this holds true very well for established projects and systems because the set of capabilities is known and defined. The main issue I take is that *new* solutions present *new* problems. Shifting things left can be an impossible task, or even worse, the *appearance* of being 80–90% there, when you are in fact not even 50% of the way there.

What causes people to think they’re almost done with a project when they aren’t even close? I think it’s the problem of *the last mile*.

## The Last Mile

Consider you are driving down a road you have never driven down before. Your GPS will tell you that one mile remains, and based on your current speed, you should arrive within a few minutes.

You turn a corner and… *there’s no road*. You screech to a halt, because what lies before you is not a dirt path, or a gravel road, or even a cut through, but a full forest, with trees and underbrush, something your car can’t simply drive through.

You have reached the last mile, but it is truly brand new territory, untouched by humankind before it. You look more intently at the GPS and notice that the road line *does* stop, and that there’s a blue dot placed a mile ahead of you.

In this last mile, there are two approaches you can take:

1. Cut through the forest and make your way on foot
2. Circle back and see if another path will take you closer

Both will add plenty of time and both are analogous to a software development project.

You will hit many rough integration points, but the roughest is generally the last one, as you get into completely new territory. Backtracking generally means stepping back and seeing if there’s a better solution that you’ve gone down, but oftentimes that just leaves you back where you started, with more time wasted.

What are some of the things that contribute to this disparity between all the other miles and the last mile? Let’s start with —

## Frameworks, Shrameworks

A lot of stake is put into the choices of technologies and frameworks that are made as part of a software solution.

In my experience, it doesn’t really matter: you can choose the highest performing language and still produce a garbage system, or choose something slow like Python or Javascript and put out something that’s blazing fast.

There are a lot of choices to make when building a system, and making those choices can *feel* like forward progress. However, these choices are ones that can actually make the last mile even longer, later on.

Consider that you want to build a website that processes payments, and you want it to be super fast, so you use something like webassembly. You get up to speed and make a snappy, super fast site. But when it comes to the payments piece, you look around and realize there are not really any good connectors for Paypal/Stripe, etc. that work with the framework/language, you chose. You can now decide to:

1. Cut through the forest (write your own PCI-compliant thing? Oh no)
2. Backtrack (try to use your framework as much as possible while searching for something off the shelf)

A framework and/or an explicit technology choice is a necessary evil in software: you don’t want to have to define your own server protocol, or web framework if you can help it. But all technologies come with their own warts, and usually, the biggest warts show up when you’re in that last mile.

It can be something like the framework doesn’t work with certain file formats well, or performs very poorly under load that you never tested with before, but the last mile will really test the mettle of the frameworks you chose.

Oftentimes delaying these sorts of decisions is the right way to go, using simpler or more basic setups until “we need a framework” is the answer to a problem you have.

Instead of starting with PostgreSQL or DynamoDB, just start with flat files or SQLite. Change when you start to get a sense of what’s going well, and what’s not.

As Bob Martin says in *Clean Architecture:*

> Decisions about the details can be delayed and deferred for as long as possible during the life of the software.

This delay won’t necessarily make the last mile any easier, but it will definitely be less abrupt, and require less circling back.

Beyond frameworks and technologies, there’s an even heavier weight that a project can be forced to deal with —

## Proprietary Software -> Hard to Integrate

A real blindside that can appear in the last mile is the integration between a more “standard” (i.e. Open Source) solution and a proprietary solution.

As an example: you might be tasked with integrating a set of relational databases, so you set off on your database connector journey. Then in the last mile, you’re told that the database you need to integrate with doesn’t support a relational setup, and requires a different format to load data. And it’s proprietary.

In my experience, proprietary things are not generally better than their Open Source equivalents. The primary reason is that no one has written a good client to share with the community, because, well the system is proprietary. So proprietary software begets other proprietary, private solutions.

This makes the last mile especially dangerous. You’re not talking about a lush forest, now it’s a swamp, full of gators and quicksand. Your last mile has become the *final* mile that you will march down to integrate with some proprietary system, that is both hard to test against (they don’t have easily testable trial versions of propietary things? shocker!) and hard to validate (how do we know it works? we go to the one UI we have access to).

If someone mentions a proprietary system as necessary to a project, getting any sort of idea on how to talk with it is a good way to spread the hell of the last mile along your journey.

But my advice: avoid proprietary things at all costs, or treat them as black boxes if you can. Having to integrate with them can be the most painful part of any software job. Given that you *have* to integrate with these systems, make sure you can find someone with domain expertise, and get them to help you, so you aren’t working crazy hours trying to get something working.

So what can you do in the face of tough tech choices and proprietary systems?

## The Importance of Leaving Room for Hooks/Plugins

One possible savior of the last mile problem is oftentimes moving the end destination closer (shifting left?!). Accomplishing this is usually done with: “Please insert the code you need to do the last bit here.” So you shift your end to the left but shift the other’s ends a bit farther to the right.

This can come in the form of hooks or plugins, which are at the consumer’s discretion to create, but also don’t create these abrupt dead-end paths.

Instead, you’ll see a rough transition to many small paths, each written by people who came before and may or may not have had similar problems to you.

A lot of times the best answer is no answer. You don’t know if the last mile that you’re traveling down is the same last mile another consumer or developer might need to go down. Leaving some options, or the ability to add in your own option, is oftentimes the right answer.

But know that you haven’t “solved” the last mile problem, you’ve merely shifted responsibility elsewhere, hopefully to a person who’s better set to take the baton and run that last mile.

## Summary

Software projects attempt to shift left on net new solutions, which leads to a last mile fallacy (i.e. the work is mostly done when it is just beginning).

People use frameworks or technology choices to say that they’re saving time, but that’s not necessarily the case. Delaying these decisions can be more beneficial in how we decide to do things.

Proprietary systems can be nightmarish to integrate with: seek help on how to do so early, and consider getting any form of communicating with that system the most important thing to prioritize early on.

Leave room for others to solve the last mile problem for you, reducing the work you have to do, but increasing the opportunities for people to get some value out of the system you have created with different last miles.

Thanks for reading!
