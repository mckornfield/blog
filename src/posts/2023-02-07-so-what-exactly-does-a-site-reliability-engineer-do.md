---
title: "So What Exactly Does a Site Reliability Engineer Do?"
subtitle: "Do you just type terminal commands all day? Look at graphs?"
date: 2023-02-07
medium_url: "https://medium.com/@mckornfield/so-what-exactly-does-a-site-reliability-engineer-do-6da1a25d8bb5"
---

Do you just type terminal commands all day? Look at graphs?

![Photo by Gabriel Heinzer on Unsplash](/img/so-what-exactly-does-a-site-reliability-engineer-do/0_ureaNbwX16pe7C62.jpg)

*Photo by [Gabriel Heinzer](https://unsplash.com/@6heinz3r?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I get this question from folks quite a lot, so I thought I’d explain it at different levels of detail, so that whatever your level of tech-savviness, something will get through to you. What I do is similar to what thousands of other Software Engineers do, which is maintain systems that allow applications to continue working or support new workflows.

### (As context for where I work now… to a 5 year old)

I work for a company that helps people or other companies generate data. Data is any sort of information you can write down about a person, like how old they are or how tall they are.

A lot of the time, companies aren’t allowed to share certain data, like someone’s name. My company helps make data that looks like the original data, but doesn’t have anything like a specific person’s name or date of birth.

### Explain Like I’m 5

What I do for the company is help make it so we can release new changes safely and make sure that the old way continues to work, and works well. That means making sure people don’t run into errors, or that they can make changes to their data like they want.

There are people that are smarter than me that work on how exactly we generate that data, something called “Machine Learning.” I help those people get their work to customers, either through our platform or a platform they run on their own. A “platform” in this sense means a place where the code can run.

### Explain Like I’m 10

If you’ve heard of [ChatGPT](https://openai.com/blog/chatgpt/), I work at a company that allows people to train and create Machine Learning models just like it to generate “fake” data, or what we call “synthetic data.”

My role is to help maintain, release and get visibility into how customers use our models. A lot of things can go wrong, either on their side while configuring how to train the data, or on our side due to unforseen edge cases or changes in the services we use. My goal is to make sure we can make changes without fear of breaking things for people and not knowing about it.

### Explain Like I’m 20

I work at a synthetic data startup. My role is primarily to make sure things are running as well as they can, and that customers have a reliable service to run their workloads on.

Reliability can mean a lot of things, but generally it involves making sure there are low error rates and low latencies where we can improve the time to do things like get a job into a starting state. Working at a startup also means that I have freedom to get more involved in other pieces of work, like our CI/CD infrastructure or also help improve our security posture.

### Explain Like I’m Another Engineer

I help develop a cloud based ML ops platform. I work primarily in a couple different languages to help the release and processing of requests to train synthetic data workloads on my company’s platform.

I also use a good amount of Terraform as well as Kubernetes related knowledge to roll out new releases and changes to our cloud platform, and to package up reusable resources for on-premise deployments. We use our cloud vendors’ monitoring tools to get visibility into when there are issues (and where), and I help maintain or improve that observability system.

Hopefully these explanations at different levels of detail help you understand what I do. Thanks for reading!
