---
title: "It Must Work"
subtitle: "The only meaningful manifesto in software"
date: 2025-10-31
medium_url: "https://medium.com/@mckornfield/it-must-work-c1766bac3e14"
---

![Photo by Clint McKoy on Unsplash](/img/it-must-work/0_daBZ4LCU9SwmNIRk.jpg)

*Photo by [Clint McKoy](https://unsplash.com/@clintmckoy?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Enough with the Pedantry

I’ve worked a small number of places, but there are quite a few fights and discussions I’ve seen take place that end up being *pedantic.* If you haven’t heard the word, pedantry is:

> being excessively concerned with minor details and rules or with displaying academic learning.

A lot of times, in software, details matter…

But I have seen arguments about **end user experience**,

or **the preferred way** to use something might be,

or **what’s an acceptable size** for a package to download,

and then it turns out that, at the end of the pipeline of all these discussions isn’t a pot of gold at the end of a rainbow, but a confusing, practically non-functional piece of software that has been argued into existence.

Instead of arguing over what we were going to build, down to some level of detail that you need a microscope to see, we could have spent that time building *something*, realizing it was terrible, and trying again.

Pedantry is the enemy of a decent software feedback loop.

### What Matters

People who use software want it to *WORK FOR THEM*. How long they’re willing to wait is a function of *what* they’re waiting for, but if at the end of some long release cycle, or some fun installation process, they don’t even get something useful, the software and all the pedantry it was wrapped up in, isn’t worth s — t.

Let’s remember —

### The Agile Manifesto’s Second Bullet

From the agile manifesto:

- Individuals and interactions over processes and tools
- **Working software** over comprehensive documentation
- Customer collaboration over contract negotiation
- Responding to change over following a plan

What does “working software” mean? It doesn’t mean software that adds two numbers (boom `return 1+1` ).

It means “software that solves a problem.”

That doesn’t mean software that has been through 300 RFCs, or software that has a nice “QA pass” label on it, or 50,000 JIRA tickets and 100,000s of lines of Python.

That means a person can install the software *somewhere* and use it to solve *a real problem*. Is the path of RFCs, tickets, QA passes and code writing not the final path?

### The Top Software Companies Produce Working Software

Let’s take an example, Netflix.

[An excellent writeup](https://newsletter.pragmaticengineer.com/p/what-is-good-software-architecture?utm_campaign=email-half-post&r=1lafn4&utm_source=substack&utm_medium=email) of his time at Netflix by Matthew Hawthorne details what made Netflix successful during his time there: producing working software and a flexible architecture.

People use Netflix to watch content. It, like similar content distribution platforms such as Spotify, is among the best at it. My understanding from Matthew’s article and some of [ThePrimeagen’s explanations of his time](https://www.youtube.com/watch?v=AVnJB7xN-MU) there, is that the company has a strong emphasis on *working software*.

Process and pedantry are low on the totem pole. If you look at the Mag7/Mag10, or any top software company in the world, they might have all sorts of [internal processes and ossification](https://mckornfield.medium.com/victims-of-our-own-success-dd3729dd599f), but they made it to where they were because of working software.

Let’s not pretend it’s for any other reason.

### Your Job as a Person is to Do Something that Works

Let’s take some random examples:

- If farmers plant bad crops enough times, we all starve to death.
- If people build houses that fall over, we’ll all die in our sleep.
- If power plants fail, people freeze to death.
- If planes crash, no one flies.

I could go on and on, but *all jobs are about doing things correctly.*

### Automate or Delete

The worst parts of software companies I’ve observed are:

- Any document that resembles a TPS reports
- Fears about perception by your peers/manager
- Various fiefdoms that defend their turf at all costs.

People outside of your business couldn’t care less about what your internal processes are, but they *do care if your software works.* And works means handling all sorts of setups, scenarios, failures, fallbacks, etc. Getting software to work in all these scenarios is *hard*, but it is our job.

And anything that a company foists on its employees that distracts from creating *working software* is at the company’s peril.

My job, and every developer’s job, is to make something *that works* and when it doesn’t, *to fix it*.

Everything not in service of that should be automated or deleted.

Software’s one commandment: *It must work.*

Thanks for reading!
