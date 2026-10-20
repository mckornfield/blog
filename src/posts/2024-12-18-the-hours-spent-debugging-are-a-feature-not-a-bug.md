---
title: "The Hours Spent Debugging are a Feature, Not a Bug"
date: 2024-12-18
medium_url: "https://medium.com/@mckornfield/the-hours-spent-debugging-are-a-feature-not-a-bug-ccad5430fa78"
---

It just matters WHEN and WHERE you have to do it

![Photo by Timothy Dykes on Unsplash](/img/the-hours-spent-debugging-are-a-feature-not-a-bug/0_UeOa2T39j_B7Eo1p.jpg)

*Photo by [Timothy Dykes](https://unsplash.com/@timothycdykes?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Move Fast and You Will Break Things

As long as I’ve been in software development, I’ve tried to rush things. Wanting to get onto the next “cool thing”, I’m easily bored by repetitive, grinding tasks like debugging a piece of code that you (or someone else) wrote and why it’s going wrong.

That being said, rushing in software ultimately just means you’re delaying the debugging task for *later,* where it will be more difficult and possibly more costly (if it’s in a customer’s hands).

A good example is recently I merged a change to lookup a hostname to validate if it was a local address (fun fact, <http://localtest.me/> resolves to 127.0.0.1, a local loopback IP).

I used `socket.gethostbyname` , tested with a handful of URLs, and voila, I was good. After merging the change, a bunch of integration tests failed because they were running into the fact that this [function doesn’t work if the first substring of the URL is over 63 characters](https://github.com/python/cpython/issues/77139).

Great.

The fix was to use `dnspython` , but it suffices to say that my testing and debugging was insufficient up front, meaning I had to do it *eventually*, but not without breaking a bunch of tests in a lower environment.

And breaking things is not the end of the world in software as long as you —

### Break Things at the Right Time

The best places to break things in software are in your test environment or early on in its path into a user’s hands. “Right” in this case is probably synonymous with “early”.

The fewer people affected, and the closer they are to the code, the less of a big deal it is when something is broken.

Ideally the only person who has to interact with a broken system is the person changing it. And who do you accomplish this? With —

### Fast Feedback Loops

Some people toot the horn of TDD, but I like to think of it a bit differently. If you’re changing a complex system, ideally you have some form of fast feedback loop for the code you’re changing.

A unit test is great, or in lieu of that, a way to run your code in an integration format with quick redeploys (like a quick docker push and update into a sandbox environment). The importance is not if you are appeasing the TDD gods (I think Bob Martin is one?) but rather that you are able to break things at the right time and debug *quickly*.

Because as the amount of time you’re required to wait for feedback increases, you’ll either have to go a *lot* slower, or, if pressed, simply merge something that’s untested. Either is bad, but slower is better than broken. As they say in the military —

### Slow is Smooth, Smooth is Fast

The antithesis of the phrase “move fast and break things” is “slow is smooth, smooth is fast.” If you have fast feedback loops, you can shorten your time to move, but [a real promotion pipeline for a piece of software is still *slow*](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/).

Run the fast tests. Then the slow tests. Then the tests in the first environment (dev). Then the second (test), etc. If anything fails, abort!

Depending on how many environments, how many tests, and how slow they are, this can be a *slow* process. But slow is good; slow means you’re putting changes through their paces, instead of just “pushing and praying” to a production environment.

A pipeline can also be a bit simpler, i.e., push to an environment, and only schedule releases on certain times so changes have time to “bake.” Not as nice as a continuous delivery pipeline, but still embodying the “slow” mantra.

And inevitably you’ll have to debug things when they break, either from test pipelines, or alerts failing. And when that happens, hopefully you have fast feedback loops to test your changes to do it all over again.

### Closing Thoughts

A lot of software development comes down to debugging. You will spend many hours debugging why code works (or doesn’t work) the way it does.

This is the way things are supposed to be; doing the right thing is not the easy thing. And the more you can speed up the debugging process with fast feedback loops, as well as shift left the failures presented by code changes with a slower, more rigorous testing process, the better the code you produce will be.

Debugging is a part of the job, and making it happen earlier is a part of being *good* at the job.

Thanks for reading!
