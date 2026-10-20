---
title: "The Automation Reality"
date: 2024-09-21
medium_url: "https://medium.com/@mckornfield/the-automation-reality-7cc17a6ae00a"
---

Automated things require lots of manual work to maintain

![Photo by Built Robotics on Unsplash](/img/the-automation-reality/0_tuJeiN4cPJPdqod8.jpg)

*Photo by [Built Robotics](https://unsplash.com/@built?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### “You Didn’t Build That”

Famously (or infamously if you’re a friend of big business), Barack Obama, on the campaign trail admonished his opponents:

> Somebody helped to create this unbelievable American system that we have that allowed you to thrive. Somebody invested in roads and bridges. If you’ve got a business, you didn’t build that…

If you set up an automated system to run your business, using tools like Zapier, Google Docs, or any of the myriad tools and cloud services, let me tell you that these systems are anything but automated… i.e. “*You didn’t build that”…* The manual parts are just invisible to you.

In programming there’s the idea of the [OSI model](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/), a set of layers that all systems have to move through, but I’d like to divide our automation systems into the manual or “toil” layers.

This stack of invisible things is:

- Utilities
- Hardware and Servers
- Open and Closed Source Code
- Data

### Utilities

Every piece of software running uses electricity.

*There were* [*mechanical computers*](https://en.wikipedia.org/wiki/Antikythera_mechanism) *at one point (could you imagine an Internal Combustion powered computer? I’m sure Exxon-Mobile could…)*

Anyway, electricity is never free. It has both a monetary and environmental cost. Massive power plants and even small solar arrays all cost money, time and physical resources to create and maintain. Nothing that produces electricity will run forever (even the sun has a life expectancy, albeit in the billions of years).

Another piece of the utility puzzle is internet connectivity ([in the form of terrible oligopolies](https://equitablegrowth.org/research-paper/communications-oligopoly-steroids/)). Also a form of electricity transfer, albeit in the form of data, these “utilities” come with high maintenance costs that they push onto consumers.

Building and maintaining power plants and data lines is anything but automated; it requires

### Hardware and Servers

When GPT 4.0 cost “[over a $100 million](https://www.wired.com/story/openai-ceo-sam-altman-the-age-of-giant-ai-models-is-already-over/)”, most of that cost went to renting server space. Included in that cost was the aforementioned electricity cost, but the lion-share was renting the compute, which we can see from how much these components cost to acquire and maintain.

Nvidia sells GPUs that range from ~$500 (user grade) to [$50,000](https://www.cnbc.com/2024/03/19/nvidias-blackwell-ai-chip-will-cost-more-than-30000-ceo-says.html). These make up just one part of a server setup; the rest of th components within a similar range, $100s of dollars to $1000s for [a functioning blade server](https://www.theserverstore.com/dell-servers-dell-blade-servers).

All of this needs to be racked, cabled, and housed somewhere with stellar internet access and reliable power output in order to be remotely useful to any consumer.

Data centers. Anything automated these days is not running on a server in someone’s basement; it’s running on a server. (Especially any [AI system worth it’s salt](https://www.goldmansachs.com/insights/articles/AI-poised-to-drive-160-increase-in-power-demand).) These things have a significant operational cost, [in the millions of dollars](https://www.streamdatacenters.com/resource-library/glossary/data-center-cost/#:~:text=The%20average%20yearly%20cost%20to,maintenance%20of%20applications%20and%20infrastructure.) levied by yet another set of oligopolies.

On top of moving all these parts around, a very real *manual* cost is getting all these materials out of the ground and into hardware products. [It’s mining operations](https://hackaday.com/2021/11/15/mining-and-refining-pure-silicon-and-the-incredible-effort-it-takes-to-get-there/), [it’s children shoveling coltan](https://theconversation.com/what-coltan-mining-in-the-drc-costs-people-and-the-environment-183159), and towards the end of the process, it’s a set of concentrated (as in oligopolies), [extremely high tech operations to create semiconductor components](https://www.reuters.com/breakingviews/tsmcs-most-complex-engineering-task-is-itself-2024-04-03/#:~:text=TSMC%27s%20dominance%20owes%20much%20to,tech%20giants%20like%20Apple%20%28AAPL.).

### Open and Closed Source Code

The internet largely runs on Linux servers, an open source operating system. Its frontends are powered by Javascript and Typescript, languages built on open standards. Its backends are powered by similarly open standard languages, i.e. Python, Go, Rust, and Java (though not nearly as open thanks Oracle).

But while languages evolve relatively slowly, the frameworks built on top of them that “do the work” evolve on a day to day basis. New vulnerabilities are found that need to be patched, new systems require new clients and protocols to interact. If you look at a GitHub repository for any open source framework (say [PyTorch](https://github.com/pytorch/pytorch), [Kubernetes](https://github.com/kubernetes/kubernetes), or [React](https://github.com/facebook/react)), you’ll find a large number of issues and active work to maintain/add features to these frameworks.

A large number of these regularly used frameworks are *open source*, meaning anyone can use them free of legal challenges. But that doesn’t mean no one is doing any work. There’s still millions of developers who have to maintain these systems.

So much of closed source code (i.e. code that companies copyright and do not share) is built on top of open source ([GitHub says this number is 97%](https://venturebeat.com/programming-development/github-releases-open-source-report-octoverse-2022-says-97-of-apps-use-oss/)).

### Data

For a long time, data meant accurate tracking. Meta and Google made their money by being able to sell and serve the most tailored ads, which was part of the contract of using their products for free. This data, and the ads it allowed the companies to target us, with paid for all of the infrastructure and development costs above.

But many companies bought and sold our data, like [credit reporting companies](https://www.investopedia.com/ask/answers/102814/how-do-credit-bureaus-make-money.asp#:~:text=Credit%20bureaus%20make%20money%20by%20collecting%2C%20storing%2C%20and%20analyzing%20your,loan%20or%20market%20to%20you.) (who are also [good at leaking our data](https://www.ftc.gov/enforcement/refunds/equifax-data-breach-settlement)), so this idea of data as a product is nothing new.

For automation, data was the currency, allowing closed source companies to pay to maintain and build out their automation stacks. But things have changed.

With the massive push in AI of the last few years, data is now the *input* that creates the value generating system: one or more AI models.

The largest cost to AI outside of training is in creating useful data. *Useful* can mean more than one thing, but in the case of AI, this means data that is *labelled* so an AI model can be trained on it. Data in its raw format isn’t enough, and machines aren’t intelligent enough (yet) to self label, so in the meantime, this data is [hand labelled by humans](https://www.linkedin.com/pulse/human-touch-behind-chatgpt-understanding-importance-data-dave/).

One of the largest successes in the AI revolution was not an ML model, but [a large, labeled image dataset](https://www.image-net.org/) that could be used to benchmark and train models. Data has to come first.

At some point (or maybe already?) we’ll reach a point where the data needs of our AI systems outstrip our ability to hand label a bunch of data, either because [the data is put behind paywalls](https://digiday.com/media/why-protecting-paywalled-content-from-ai-bots-is-difficult-business/), [has privacy concerns](https://arc.net/l/quote/mtjqaboq), or simply because the volume/complexity of the data required is beyond what is available. This means we’ll see [synthetic data companies come into their own power](https://www.bccresearch.com/pressroom/ift/synthetic-data-generation-market-to-skyrocket-to-21-billion-by-2028); but those companies will still rely on all the other layers of the onion we’ve discussed so far, using data and all the other tools available to become data factories.

### Automated? Or Automanual?

Automated systems are at the fringes of a very manual stack, of real humans doing real work.

Putting an automated system in the loop means having a support network of humans to build and maintain that automated system; jobs are not being stolen, but rather shifted around and consolidated into a handful of oligopolies.

Engineers work to build an interconnected network of electricity and data, that can shuffle work done by high powered hardware devices to consumer grade devices. The software that powers these devices is all built around Open Source, code that is maintained by individuals working around the globe. The data used to both pay for and create these automation systems is created by selling human data and by having humans hand label data.

The common theme is, when you automate anything, you’re twisting knobs at the edge of a very complicated and expensive plumbing system, one that only a handful of organizations control the pieces of, and one where humans are constantly working.
