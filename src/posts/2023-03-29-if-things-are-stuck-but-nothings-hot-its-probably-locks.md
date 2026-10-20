---
title: "If Things Are Stuck, but Nothing’s Hot, It’s Probably Locks"
subtitle: "Locking is one of the necessary evils of the software world. I’ll talk through what it means for things to be “stuck”, “hot” and where…"
date: 2023-03-29
medium_url: "https://medium.com/@mckornfield/if-things-are-stuck-but-nothings-hot-it-s-probably-locks-4178b52b0d0"
---

![Photo by Markus Winkler on Unsplash](/img/if-things-are-stuck-but-nothings-hot-its-probably-locks/1_nn99zuvw5t2emIpPxbOPDg_2x.jpeg.jpg)

*Photo by Markus Winkler on Unsplash*

Locking is one of the necessary evils of the software world. I’ll talk through what it means for things to be “stuck”, “hot” and where locks come in.

### Stuck

Software systems generally have two sets of requirements

- Functional (does it do what I ask?)
- Non Functional (does it do what I ask *well?)*

When systems slow down or start returning timeouts, that’s generally when those non functional requirements start to matter.

If you have a system that’s experiencing some sorts of issues related to load that really slow it down, then you might say it’s “Stuck” if you’re being informal, but the correct term is “degraded.” A system can be degraded for more than one reason, but you’ll see certain signals like:

- Requests taking especially long or timing out
- A high concurrency number if the system can scale up extra threads or processes to handle traffic
- A quickly growing queue, if the system is able to properly queue messages

All of these signals indicate a lot of work *might* be getting done. Let’s suppose your system is really working hard, then we might say that it’s —

### Hot

Think of a car. Imagine the engine dial when you put your foot all the way down on the gas. That dial will go to a point and then stop. That’s the peak performance the engine can deliver. You’d say the engine is “running hot.”

Software systems have similar red lines.

At the machine level, all machines have finite resources (RAM, CPU, Disk) that serve as the upper limits of what the machine can handle.

These types of metrics can reach a point where they are full, i.e. “saturated,” just like the red line for your car engine. You’ve used all the CPU on the machine, or maxed out Heap memory or disk IOPs.

If you track down that requests are overwhelming your database, you might see high CPU or memory on the DB. Conversely, maybe you have a computationally intensive algorithm running on the server, like password hashing. Then you might see CPU jump on the application servers.

But what happens when *nothing* is hot, but requests are still getting backed up, things are still “stuck.” Then we’re probably dealing with —

### Locks

The source of the problem that locks are made to solve is that multiple threads/ processes try to alter the same resource, whether it’s an in memory value or a database row. If multiple things can access something concurrently, and if they were to do so in a “lock free” manner, you might get aberrant behavior.

Consider a bank account without locking. Two transactions come in, one to debit the account $1000, and one to credit the account $2000. Without locking, you don’t necessarily get $1000 as the final result. You could see:

- $1000 if the debit comes in after the credit
- -$1000 if they come in at the same time, but the debit transaction overwrites the credit transaction
- $2000 for the opposite case, where the credit transaction wins

With locking, we ensure that the new value is computed one transaction at a time.

The reason locks are evil is that they can create major performance/ non functional issues. Consider the [dining philosophers problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem), whose solutions involve some form of either locking or preferred access to a resource. Concurrent access can get messy very quickly.

So if you have a system that is stuck, but nothing is hot, most likely there is some locking happening. Lots of requests are most likely queueing around a lock, which can only process requests so quickly.

Besides scouring the code, using something like distributed tracing or profiling can reveal where locking related bottlenecks might be.

There aren’t always great solutions to dealing with locks, but some I’ve seen are:

- Narrowing the conditions under which you lock
- Using faster systems for managing distributed locks, like Redis instead of a Database
- Adding timeouts to locks, in case a process crashes with a lock still held
- Worst case: rearchitecting the transaction workflow to use fire and forget instead of locking, and resolving transactions in another system (maybe even a single threaded system, where concurrency doesn’t matter)

### Summary

Systems can degrade under load, but not always because they are running hot. Sometimes there are locks in place, and doing what you can to reduce the effect those locks have can save your system’s performance.
