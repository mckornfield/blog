---
title: "New Developers, Here’s What You Should Know to Get Ahead"
subtitle: "In the time of layoffs, the better developer wins"
date: 2023-05-03
medium_url: "https://medium.com/@mckornfield/new-developers-heres-what-you-should-know-to-get-ahead-1498a2cf59c0"
---

In the time of layoffs, the better developer wins

![Photo by Mahmud Ahsan on Unsplash](/img/new-developers-heres-what-you-should-know-to-get-ahead/0_94XTl3NWrbVRzTQs.jpg)

*Photo by [Mahmud Ahsan](https://unsplash.com/@mahmudahsan?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

10 years ago I was in school studying physics. I was decent enough with a computer, but software development was a foreign concept to me. I took some Computer Science courses but they were very boring to me (to be fair, not the world’s best professor taught them).

Because I took a path through physics, then consulting, and then learning on the job as a Product Engineer, my path was [rocky and self-paved](https://mckornfield.medium.com/a-few-ways-to-become-a-software-developer-b0677f140caf).

That being said, I learned from some great people at Appian and Walmart on how to be a good software developer, and I don’t know that I would have gotten all of that from a Comp Sci degree. I thought I’d try to boil down what I think makes a great developer down into the people side and the technical side.

## The People Side

Developers don’t have to talk to people, right? You just sit in a chair at home (or in the office!) and keep an IDE open and clack away on a mechanical keyboard, don’t you?

Some do this, and some do it pretty well. Unfortunately I think a big part of getting ahead is getting out of the code and into the product and people side of things. You’re an easy person to lay off if your primary contribution is “writes code that works (hopefully).”

So yes, having technical skills is important (and I’ll get to *what* you should know in a sec), but let’s not forget these just as important things.

### Having Good Rapport with Your Teammates

Depending on where you work, your team could be a bunch of other developers, or other roles, like User Experience, Product Owners, Quality Engineers and Agile Coaches.

These other people should like you, or at the very least, tolerate you. That means you show a genuine interest in what they’re doing, and if you disagree with them, you do it respectfully (i.e. “I understand what you’re saying” vs. “No, you’re wrong.”) You’re on a team, you know what that means? You win together or you lose together. You don’t win if you find a way to outsmart your Product Owner.

This means being helpful and being generous with your time. I think focusing and doing heads down work is important, but leaving time to grow closer with your teammates is *more important*. After all, they’re the people that communicate to your manager “oh yeah, Matt’s awesome to work with”, vs. “Matt really needs to work on his communication skills.”

“Matt really needs to work on his communication skills,” is teammate speak for “Matt is a sociopath who needs to learn how to talk to people without being a jerk.”

Don’t be that person everyone hates. Be the person everyone relies on.

### Being Customer Focused

This term makes me want to gag. I wrote it because it’s an industry standard, or even corporate standard thing.

I think a better term might be “Know How the Hell People Use What You Create.”

“Knowing How the Hell People Use What You Create” means a lot. In fact it might be *the most important thing* in software development. Because if people *don’t use* what you create, then you *won’t have a job*.

Some companies are very big, so this means working with Customer Success/On Call people closely to know if things are going well or bad with the software you’re writing. Maybe you create products used internally, so your stakeholders are people at the company. Maybe you’re a startup with just you as the developer or a small team, in which case you should know how people are using the things you create since you’re in a sink or swim state.

There are some technical answers (Google analytics track the hell out of everyone!) but I think the best answers are “talk to somebody who either used the software or works with someone who did.” Know what the major pain points and blockers are to using what you make and squash or work around them ASAP.

Great software is software that solves real problems that real people have, not something you can put on a VC slide deck. And you only know about real people’s problems by understanding what they’re doing with your product.

### Developer Experience

If you work with other developers (i.e. you’re not in a startup where you’re the only dev), you’ll notice developers can do lots of things differently.

- Some will have strange rituals to get their builds to work.
- Some think every line of code should be unit tested
- Some of them think unit tests are a waste of time, only integration or system tests will work
- Some code in vim and emacs like a boss
- Some won’t look at the code unless it’s open in IntelliJ (i.e. they won’t even look on GitHub)

Developer Experience is varied but a core thing that binds developers together is that they are generally:

- Lazy
- Impatient

i.e. Developers don’t want to do a bunch of manual clicky stuff and they don’t want to wait forever. They want to run commands and feel like they’re super fast and amazing (god complex?).

When you work in a codebase with other developers, understanding what you have in common with folks is a key part of being productive and not getting into turf wars.

Troll 1: “We should be using black to autoformat”

Troll 2: “No! Only autopep8!”

These are battles you’ll have to fight at some level, but remember that more important than being right, developer experience is about understanding *what works* and *what doesn’t*. A lot of times, it’s context specific.

Unit testing is pretty standard, but unit testing everything is masochistic. Forcing everyone to use the same IDE is a good idea for a larger organization, but for a smaller one, it probably doesn’t matter as much.

Sometimes tech debt matters a lot, other times, it’s just a way to appear busy but doesn’t serve the organization or other developers much to address it. Tech debt != bad code. Tech debt is the sludge that makes working hard or impossible, and is worth getting rid of.

PS: Everyone should use black for python formatting, it’s the best. Screw what Troll 2 says.

## The Technical Side

I could write a whole other article about what to be good at technically speaking, but I think there are also much better resources online. But I do remember there were a lot of things that new college hires had basically zero understanding of, CompSci or not, so here’s my short-list.

### The Terminal and the Filesystem

If you don’t know how to use the terminal, practice practice practice. Read something like [this on the commands that exist](https://github.com/jlevy/the-art-of-command-line) for the terminal.

Or play some [games online](https://overthewire.org/wargames/bandit/) that show you how to use the terminal.

Learn how to use a terminal based text editor like vim (type “vimtutor” in the terminal) or emacs (apparently you read this [old wiki](https://www.emacswiki.org/emacs/LearningEmacs)? it has a [vimtutor sorta thing too](https://wiki.termux.com/wiki/Emacstutor)) or even nano (IDK anything about nano other than compsci 101 PTSD).

You’ll use IDEs and Cloud computing and all these fancy things, but the terminal and the filesystem are still basically the backbone of it all.

### “Git” Gud

Git is going to be your bread and butter for most software companies. I haven’t worked somewhere yet that *hasn’t* used git (although sometimes stuff was in subversion, which is always in a state of being migrated to git).

[Learn git branching](https://learngitbranching.js.org/) is kinda fun, but my advice is: don’t use visual git commands from IDEs or the GitHub app. Just read [git’s docs](https://git-scm.com/docs/gittutorial) (which are very good and thorough) and practice using it in a personal GitHub project. Know how to rebase and merge, and keep your commit history clean.

### Running and Working with Containerized Environments

I was in a bar in 2015, a consultant that new basically nothing. This guy from another tech company was telling me how containers were so awesome and were going to change everything. I was like… you’re right but IDK what a container is. He said it was like a VM, but smaller.

That’s… basically it. A VM, but smaller.

This is a big one that I think is still pretty lacking in University education (why is everything still on VMs dawg?). Since 2010, Docker has been the word on everyone’s lips, and its equivalents (containerd, whatever openshift uses). If you don’t know what Docker and/or containers are, [Docker has solid docs](https://docs.docker.com/get-started/), and you should just download it and run some containers. Start a project that uses something containerized, deployed in ECS or Lambda or something.

Why do containers matter?

Kubernetes -> Containers

Serverless -> Containers (even if you don’t use a container to run it, it’s how it works basically)

Cross platform development -> Containers

Heck, GitHub’s codespaces run in a container. This webpage probably was served out of a container.

Containers containers containers containers. You should know about containers!

### Software Testing; Unit/Integration and Beyond

I don’t think they do a good job of this at certain companies, and they definitely don’t do this much in unversities from what I understand. But so much of the Software space is dominated by figuring out how to test things without “testing in production”, i.e. “[doing it live](https://www.youtube.com/watch?v=vu2NK5REvWM).”

Unit tests are fast, integration tests are slower but a bit more realistic, and things beyond that like UI tests or System tests act more like a user using your system than some contrived testing scenario.

Martin Fowler has a [good blog post](https://martinfowler.com/articles/practical-test-pyramid.html) on it, but getting good at testing is definitely something you should experiment with. Sometimes unit tests are just what the doctor ordered, and sometimes they’re a big pain compared with testing things at a higher level.

Knowing the tradeoffs, what things like “mocks”, “stubs”, and “patches” are and how to use them in your language of choice are super important to being an effective tester. Also knowing a little bit of how to run these tests in different environments (Continuous Integration sorta thing) will really help you be ahead of the game.

### The Right IDE for Your Coding Language

If you use Java, it’s probably IntelliJ.

If you use Javascript/Typescript, probably VSCode.

Python, PyCharm or VSCode as a toss up?

Go, Goland ($$) or VSCode again?

You probably know what an IDE is, but just using vim for everything or just using VSCode is probably not going to cut it. These IDEs are like tools in a toolbelt, you don’t hit nails with your screw gun or twist screws with the grippy side of your hammer.

Make sure you know which IDE is the best for the language you’re using, and use it, even if it costs money. The IDE licenses aren’t cheap necessarily but they’re worth it if you’re more productive.

And most of all, get GOOD with the IDE. Know the shortcuts and how to search for things/ move quickly around. So much of software development is just reading and digging for code. Being good with an IDE (or grep/vim?) can make you much quicker at finding what you need.

### Summary

- Be nice, but don’t take crap from your team. Be the helper, not the pariah.
- Know how the hell the code you write is actually used, so you can make it better.
- Get on the same page with developers you work with on how to write/maintain code.
- Know the terminal, filesystem, and git as well as you can.
- Figure out what a container is and how to use it.
- Learn how to test your software in an automated way
- Find the right IDE and become great with it

If you have any other things you think new developers (or I!) should know, let me know in a comment!

Thanks for reading :)
