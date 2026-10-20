---
title: "To Release… or Not To"
subtitle: "A question of what, not when"
date: 2025-08-16
medium_url: "https://medium.com/@mckornfield/to-release-or-not-to-a1c37580607b"
---

![](/img/to-release-or-not-to/1_IXzjWNF3EFkO2xqnYBqLLg.png.png)

### Another take on DORA.

There is a DevOps report ([DORA](https://dora.dev/research/2024/dora-report/)) that an old boss of mine would point to as the gold standard in development.

I remember being very into it a few years ago, back when I was drinking the DevOps Kool-Aid (OH YEAHH). The report slices the world of software into different levels of performance, based on various metrics, like **deployment frequency**, **lead time for changes**, **MTTR (mean time to recover) and MTBF (mean time between failures)**.

There are elite performers, low performers, and other levels in between, who correspondingly show better or worse on all these metrics.

What generally made high performers so good was a continuous and rigorous release process, ie., every change got pushed all the way to production, on merge, instead of via some auto-manual or calendar based process. If a change broke things, generally it was caught in lower environments, or in the worst case, would trigger a rollback in production.

I want to take another angle, which is my perspective on what the other types of release are, not by their DORA metrics, but rather the value the software provides and how that lines up with release cadence.

We’re talking about going from ideas to execution.

### Slideware

This is every UC pitch deck existence, or every piece of software in its earliest stage.

Maybe it can even demo, but the demo is too unstable to “do it live”, so screenshots or GIFs are your best bet.

Slideware does what its name suggests: populates slides, documents, or splash pages. Its value is to convey potential problem solving and TAM (total addressable market). It can make or break a startup’s ability to capture fundraising dollars, and is arguably valuable in its own right.

At bigger businesses, Slideware can drive an effort via a prototype or RFC, showing how something might be possible, allowing engineers to make early decisions about the trajectory of a product or feature.

Slideware is *never* released. Even if it is functional, it is inspirational for its ideas, its execution. Releasing software is all about getting *use* out of it, which we’ll get to shortly.

A strong piece of Slideware is *inception*, planting ideas in a buyer/engineer’s brain.

### Demoware

The next level of software is something that works, arguably not much more than a piece of Slideware. Its primary advantage is in capturing feedback on the user interaction side, and letting people get a better sense of how their ideas might manifest.

This type of software might feature heavy in a PoC (proof of concept), where usability and feature sets are more important than “actually being able to do the thing.”

Demoware is something you probably only release once or twice (an alpha or a beta), and any other iterations roll into a man product. Defects in it are either explained away or, worst case, patched and hopefully translated to the final product.

Demoware’s danger over Slideware is the lines between execution and ideas are blurred, to the point where effort can be misplaced (great demo, no product) or not enough (“we were expecting more in the proof event”).

A strong piece of Demoware knows its limits and refuses to do more, promising much but delivering what little it can.

### Enterprise Software

The step between Demoware and Enterprise Software is a difficult one.

I think once you are through a proof event, compares who buy software have pretty standard expectations:

- You release on a calendar Caderet (monthly/quarterly)
- You patch on a fighter cadence for bugs or vulns (weekly/monthly)
- Stability and reliability are more important than features and idees

The trite phrase “rubber meets the road” comes in here, but this is where I think software takes a turn. Demo- and Slideware are the land of dreams and promises, where Enterprise Software and SaaS are the land where dreams come true… or die — promises are made or broken.

A lot of people have opinions on what makes good enterprise software, and there are many smarter than me.. From my view:

- It works good enough
- Upgrading it isn’t painful and doesn’t break everything
- Broken things are fixed in a timely manner

I have worked on and used enterprise software that is doesn’t live up to those ideals, but I think that short list is what every user and Administrator of enterprise software hopes for.

The release cadence of Enterprise Software is also a point of contention, but I’d argue: anything more frequent than weekly wouldn’t matter to most enterprises.

Upgrading, even when it is smooth, is still non trivial for most businesses from a process perspective. More frequently than a week won’t matter to most customers, who probably will only upgrade when hey have to, on a weekly or quarterly cadence.

Worse, if your software has a reputation for buggy or shipping unstable releases, customers will purposefully stay on older versions, only upgrading at the last possible moment, or worse yet, trying outdifferent products.

Personally I don’t know what the “right” release cycle is for enterprise software. “More frequently” sounds right to me, as a painful release process done more often will force folks to make the process better, ([if it hurts, do it more frequently](https://martinfowler.com/bliki/FrequencyReducesDifficulty.html)), but on the flip side, companies can create rigorous, difficult release processes for Enterprise Software and refuse to compromise on rigor, meaning that there’s a minimum amount of pain that cannot be automated away.

Or can it?

### SaaS

The holy grail of releases: “whenever the heck you want!”

Software as a Service can be released less frequently than every change, of course, but the more frequent the more likely the release process is “dialed in”. This means we address all the “enterprise software upgrade/reliability issues,” replacing a rigorous auto/manual time-bound release process with a merge or “at will” based release process.

There is now not only the need for the software *itself* to work, but the systems that *release and check* the software to also work and be stable. Enterprise Software more and more on “hero work”, as gaps left by automation are filled by people working extra/off hours to ensure releases land. SaaS is not so forgiving.

For SaaS products, you can build all of this release process on your own, or rely on the trail blazed by AWS, GCP, OCI and Azure.

Less important than the technology though is the mindset change.

Enterprise Software and Saas both have the requirement to work, to *execute* properly, but only the latter has the requirement that the supporting release infra works just as well/better.

Enterprise Software has sign off, go and no-go reviews, and many gates and hoops to go through.

SaaS might have these things, but they are around feature flags being flipped, or the launch plan for new features.

The SaaS product separates deployment and release, whereas Enterprise Products necessarily couple the two (customers have to buy + download a specific version).

The value of SaaS is that it works, and when it doesn’t, it’s very quick to recover.

Both SaaS’s reliability and its fast recovery are made possible not just by having good automation, but more importantly good process that is either automated or quick to execute in the event of an error.

A few more things about SaaS, to its detriment. There is still a huge market for Enterprise Software, and that stems from concerns over things like data residency, as well as the [profit margins](https://www.cnbc.com/2024/10/31/amazons-cloud-unit-records-highest-profit-margin-in-at-least-a-decade.html) that come with various SaaS providers.

And arguably, SaaS is so far from the world of ideas, that the products themselves can become difficult to change (now instead of just changing a product, you also have to consider all of its accompanying infrastructure).

### Summary

Software is change management and codification of how to solve a problem. But it is also, in its early stages, simply an idea.

Early software slides and demos serves to inspire or provoke, creating decisions for organizations and customers to make.

Once sold on an idea, usually with some proof or demo, the option becomes whether to use a SaaS or Enterprise Product, both of which (hopefully) work, but which release at different cadences and have correspondingly different levels of reliability.

Thanks for reading!
