---
title: "Explain like I’m 5: SRE"
subtitle: "Failure and toil are inevitable. How do you deal with it?"
date: 2023-01-04
medium_url: "https://medium.com/@mckornfield/explain-like-im-5-sre-c3aa483e8dae"
---

Failure and toil are inevitable. How do you deal with it?

![Photo by Ani Kolleshi on Unsplash](/img/explain-like-im-5-sre/0_4joCaYXS5SRETuYf.jpg)

*Photo by [Ani Kolleshi](https://unsplash.com/@anikolleshi?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

SRE -> Site Reliability Engineering, a discipline Google developed internally and [wrote extensively about](https://sre.google/).

Before I lay out SRE, let’s discuss the two worlds: Traditional Reliability and Modern reliability.

### Traditional Software Reliability

![Photo by Berkeley Communications on Unsplash](/img/explain-like-im-5-sre/0_twGpQR2CDsqVpVWc.jpg)

*Photo by [Berkeley Communications](https://unsplash.com/@berkeleycommunications?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

In the not too recent past, software was shipped on floppies, CDs or hard disks, and there wasn’t much that you could tell was wrong other than…

*Support Staff: 📞📞ring ring📞📞 Hello?*

*Jared: Yes this is Jared, my SOFTWARE isn’t working.*

*Support Staff: Hold on Jared, let me pull up your file. I’m going to need some more information…*

The alert system was the customer. Your software’s availability was more up to how people installed and used your software than to your developers.

### Modern Reliability

![](/img/explain-like-im-5-sre/1_AO3pbmKTCTfNLFb-swxvbg.png.png)

But things progressed (or regressed to mainframes) where applications and software are now back in the hands of corporate IT/ engineers.

The main difference is this revolution was both old and new. The original “computers” of the 50s were gigantic mainframe machines. Logging systems and monitoring systems were more word of mouth and “add a print here” than what we have today.

Systems weren’t very “distributed,” they were for the most part localized (usually by necessity; [data transfer rates were very low](https://media.nngroup.com/media/editor/2019/09/27/nielsen-law-bandwidth-growth-1983-2019.png)).

In the AWS/Azure/GCP world we live in, reliability is more complicated than the volume of phone calls.

It’s a set of targets an engineer seeks to achieve. And the process of making those numbers a reality is Site Reliability Engineering.

### “The Numbers” — Error Budgets

Nothing is infinite in life. In cloud based software systems that fall apart, the finite value is “availability.” Sometimes phrased as “9s”, it’s what percent of the time a system is operating “properly.”

Properly means more than one thing, but consider a Google search that took 2 minutes to return. That wouldn’t be something you’d say was working “properly.”

Here’s a table of how long over a year something can be down. The number of 9s in the left is what people refer to when they say “three 9s” or “five 9s.”

*1–5 9s of availability.*

The job of an SRE is not to achieve five 9s or more, but instead to determine what your *target* is, and *what it will take* to achieve that target.

For some systems, one 9 is plenty (like a batch system that can be retried, and only runs once a month).

For other systems, one 9 is unacceptable (imagine if your internet was out for 2 and a half hours a day… lots of phone calls!).

That amount of downtime allowed is essentially the “error budget.” Example: if you have 3 9s of availability, and your system is down for 10 hours, then you’ll have exceeded your error budget.

When a system starts going over its error budget, that’s when SRE has to be the bad guy (no new releases, need to reassess system design/ monitoring etc.) T

### Toil

Besides reliability, another stated goal of SRE is to reduce *toil.* Toil is any intervention that an engineer has to make in order to maintain a system. This could be rolling out new releases, debugging issues in production, or any “manual” task that ideally could at least be documented, if not automated.

Toil and error budgets go hand in hand, in that systems that violate their error budgets also tend to be systems that cause a lot of *toil*.

### *How do SREs achieve their objectives?*

Through practices that I’ll outline in another article, such as:

- Runbooks
- Post-mortems
- Release Planning
- Monitoring and Alerting
- Continuous Integration/Delivery Tooling

But each of those deserves its own topic…

So! In closing: an SRE has two goals:

- Determining the proper availability targets for a system (9s)
- Reducing toil to maintain a system (manual effort)

And they employ various practices to achieve the above goals.
