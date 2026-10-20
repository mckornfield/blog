---
title: "Should We Pay Open Source Developers?"
subtitle: "Or does that defeat the point of the whole thing?"
date: 2023-02-15
medium_url: "https://medium.com/@mckornfield/should-we-pay-open-source-developers-8c4ab57d7ee0"
---

Or does that defeat the point of the whole thing?

![Photo by Sam Dan Truong on Unsplash](/img/should-we-pay-open-source-developers/0_J6eyDKUDc9pQ8lE7.jpg)

*Photo by [Sam Dan Truong](https://unsplash.com/@sam_truong?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

This article is largely in response to the maintainer of core-js’s post about how [he’s tired and done with a fundamentally broken system](https://github.com/zloirock/core-js/blob/master/docs/2023-02-14-so-whats-next.md).

But is it broken? Or are his expectations?

### The Price of Free

There really is nothing in the world that is free.

- Free food is marketing.
- [Free applications are tracking systems.](https://www.indiatoday.in/technology/news/story/duckduckgo-launches-new-tool-to-stop-google-facebook-from-tracking-android-users-1879493-2021-11-22)
- [Free money means inflation](https://www.npr.org/2022/10/18/1128561539/pandemic-fraud-billions-california).
- Free software comes at a maintenance/liability cost.

### Free, Open Source Software

If you use Free Open Source Software (also known as **FOSS)**, you’re doing it to reduce the amount of code you or your organization has to write/maintain. But you still inherit all of the [liability when you use an open source solution](https://www.apache.org/licenses/LICENSE-2.0).

If there’s something that needs to be changed, you can either:

1. Badger the community/individual that maintains it
2. Submit the change yourself and badger them for an approval/ new release
3. Fork it and basically own a copy of the code

I’ve seen all of these things happen and they all kind of stink. But it is par for the course: *you didn’t pay for the software*. So the way you pay is dealing with this odd feedback loop to maintain the system. Remember, nothing is free.

All three of this options can be preferable to building your own thing, or buying something that doesn’t work.

### The Value of Open Source Software

Most open source software packages are solutions to specific problems. They are oftentimes solutions that you as a developer would take a while to get right, or something that might be nearly *impossible* for you to get right ([advanced mathematics for example](https://en.wikipedia.org/wiki/NumPy#:~:text=The%20ancestor%20of%20NumPy%2C%20Numeric,software%20and%20has%20many%20contributors.)), so using the FOSS solution is a no brainer.

The other piece of what makes open source software so valuable is that it is really *low cost*. I mentioned the maintenance feedback loops above, which can be painful, but are not nearly as expensive as paying for something or building and maintaining it yourself.

We know that FOSS is successful because it is so pervasive in the industry. Operating systems that almost a million servers run on FOSS (i.e. [Linux](https://truelist.co/blog/linux-statistics/)) and [1000s of Java libraries rely on the recently infamous log4j](https://mvnrepository.com/artifact/log4j/log4j).

OSS is obviously valuable; the [software economy would be very different](https://www.infoworld.com/article/3652268/harvard-census-identifies-most-commonly-used-open-source-packages.html#:~:text=%E2%80%9CFOSS%20has%20become%20a%20critical,products%20we%20use%20every%20day.) if these packages were not available to any startup or large company trying to run its software business (things would probably be much worse).

That being said…

### If You Want to Get Paid, You’re Describing a Company, not FOSS

It’s clear that Open Source Software has value, and that it has a cost (the strange maintenance loop). The problem appears when folks work on a system that is supposed to be offered freely, but want to be paid or tipped.

Working on a product that you should be paid for is not the description of Open Source Software. Now you’re talking about productized software.

And that comes with business folks (sales, marketing etc.) who do their very best to sell or promote the things you’re creating. Simply writing code and wanting people to pay for it without even one salesperson (it could be yourself) is a losing strategy.

There are two ways I know of to properly monetize a FOSS product:

- Offer a premium tier ([take something like Elasticsearch](https://opensourceconnections.com/blog/2021/01/15/is-elasticsearch-no-longer-open-source-software/), which was FOSS but changed after a battle with Amazon)
- Offer a managed version that is paid (Platform as a Service, like [Grafana Cloud](https://grafana.com/products/cloud/))

All other forms of FOSS, like core-js, are not something easily monetized. Largely because if you presented what the library does to a business person, they’d scratch their head about how to make money with it.

This is the description at the top of the README for core-js:

> It is the most popular and the most universal polyfill of the JavaScript standard library, which provides support for the latest ECMAScript standard and proposals, from ancient ES5 features to bleeding edge features like iterator helpers, and web platform features closely related to ECMAScript, like structuredClone.

Clearly it’s doing something *useful*, but if you can write a business plan around this description, you’re probably quite the salesperson.

I have nothing against the maintainer; I understand his plight, he spends a lot of time maintaining a useful software system for $0.

But writing code is not something that people actually get paid to do. They get paid to help design, build and *maintain* a product that can be sold, can be marketed, and can be promoted. A lot of FOSS unfortunately does not fit into that bucket.

### In Summary

We need FOSS, but we need developers to also have an understanding of the markets they operate in so they don’t kill themselves for no money.

FOSS is an opportunity to volunteer and give back, not a career or a way to support yourself…

Unless you follow the monetization paths I mentioned above (premium or PaaS).

But in that case, the FOSS is just like free samples: marketing :)

Thanks for reading!
