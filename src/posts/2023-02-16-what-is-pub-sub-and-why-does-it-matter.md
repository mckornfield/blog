---
title: "What is Pub/Sub and Why Does It Matter?"
date: 2023-02-16
medium_url: "https://medium.com/@mckornfield/what-is-pub-sub-and-why-does-it-matter-16b3c0f88c29"
---

Asynchronous and decoupled systems are more resilient and scalable

![Photo by Super Snapper on Unsplash](/img/what-is-pub-sub-and-why-does-it-matter/0_MFXerTOHgTnNWlM3.jpg)

*Photo by [Super Snapper](https://unsplash.com/@supersnapper27?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Pub/Sub

It’s short for Publish/Subscribe.

And it’s a very scalable way to architect a software system.

There, you don’t need to read any more… but feel free to read more if you’re interested.

### “Queue is 4 silent letters lined up behind the letter Q”

![Photo by Zichao Zhang on Unsplash](/img/what-is-pub-sub-and-why-does-it-matter/0_dmZxePN9ESzGzMev.jpg)

*Photo by [Zichao Zhang](https://unsplash.com/de/@shakusky?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

A publish/subscribe model at its most rudimentary level resembles a line or as the Brits would say, a queue. It’s a queue with a very special feature, which I’ll get to in a bit, the concept of multiple “ends” (subscribers) to the queue.

### PubSub in Real Life

Let’s imagine you’ve had bad service at a restaurant (oh no!).

Instead of sending a request and demanding an immediate response (I need to speak to the manager!) you write the manager a note and put it in the queue. Congratulations, you’re a publisher!

The queue (or for pub/sub they sometimes use the term “topic”) is read in this case by just one person, the manager (the subscriber). The manager reads your message, balls it up, and throws it in the trash. 😅

I mean… he comes up with a corrective action to improve the restaurant experience 😁

Why is this note system better than the angry synchronous system? It has a lot to do with resiliency and decoupling.

### PubSub — Resiliency

Queue and/or Pub/Sub systems are much more resilient than synchronous systems. During high load periods, messages take longer to get processed (the queue gets longer), but people that write into the queue are *not impacted* by the queue length.

Publishers write their messages and go on their merry way.

The subscribers might be sweating trying to bring the queue length down, but assuming the number of requests from publishers diminishes, those subscribers can catch up pretty easily.

If necessary **the subscribers can add more folks to subscribe** and help read through messages to up the throughput of the system.

What makes this setup resilient is that **it’s *not* a** “**serve responses or die**” scenario. There’s flexibility on how you handle load, compared with high traffic synchronous requests.

Also if the system is flooded with requests that are all duplicates, or all from the same user, it’s relatively easy to purge or filter those queue entries, since they’re just a pile of similar messages. This stops people from easily ruining your day with a long angry rant like a broken record (or in the server analogy, hosing your system with duplicate requests).

### PubSub — Decoupling

Great software architectures are all about decoupling. It allows you to evolve and change parts of the system independently, which goes a long way towards making software easy to iterate on.

When you take a synchronous call and make it asynchronous, you decouple the sender from the receiver. No longer must the two have a conversation immediately and come to some kind of conclusion.

Instead, once the queue message is processed (at some later point in time), if the publisher has information they want back, they can subscribe to some queue going the other way. This makes for a much more decoupled message interchange format.

Why this decoupling is so great is that, **if we want to change the way publishers send messages, or how subscribers read them,** **we can do so independently**. The message format is really the only contract between the two ends. Everything else is capable of changing independently.

Going back to our example of the angry letter to the manager, we can do some interesting things with this now decoupled message.

*On the publisher side*:

- We could change the mechanisms by which folks could write into the queue (e.g. email, text, phone call with transcription, a written letter scanned into a system). The only thing that needs to remain the same is the message format, running this system as a queue enables different inputs.

*On the subscriber side*:

- We could forward it to a legal body (i.e. add a new subscriber) if the message contained hateful or threatening language. Or any number of other subscribers, which could also manage reading responses via their own queues(a process called *Fan Out*).
- We could scale up or down the number of managers that read through these letters
- We could even filter some of them so no one has to read them.

All of these things happen without the publisher’s knowledge.

This would not be possible if we had to deal with the angry customer in a synchronous manner. Then you need all hands on deck and you can’t easily change the system until afterwards.

### Pub/Sub In the Public Cloud

If you’ve used a public cloud before, then it’s good to know these systems that implement the publish/subscribe architecture.

- Amazon SNS (Simple Notification Service), is one of the best examples, along with Amazon Event Bridge
- Azure Service Bus, for the Azure folks
- Google PubSub for GCP

These are the easiest ways to get started with a PubSub system built and battle tested by experts and many other software companies.

### Summary

Pub/sub is:

- A way to decouple sending and receiving messages
- A way to resiliently hold up to intense load
- A mechanism to send one message to many different folks at once while keeping both parties ignorant of how the message moves around

Give pub/sub a try, it might just save you some headaches in the future!
