---
title: "What is AWS and Why Should I Care?"
subtitle: "30% of the Internet You Say?"
date: 2022-11-02
medium_url: "https://medium.com/@mckornfield/what-is-aws-and-why-should-i-care-a701769f3751"
---

30% of the Internet You Say?

![(Don’t you just love greenfield work?) Photo by Cristina Anne Costello on Unsplash](/img/what-is-aws-and-why-should-i-care/0_tCjXr89vtnpYxGsb.jpg)

*(Don’t you just love greenfield work?) Photo by [Cristina Anne Costello](https://unsplash.com/@lightupphotos?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

If you were to be randomly dropped into a software company, chances are if you tapped a developer on the shoulder and said “what cloud provider(s) do you use?” you’d hear the word “AWS” pop up in there. Even if it wasn’t the main way they hosted their software, maybe they’d compare their cloud solution to AWS or in some part of their toolset, AWS would pop up.

Well, what is this acronym exactly? Amazon Web Services? What’s that mean?

### Why does it exist?

The same reason things like Borg (and then Kubernetes) exist for Google:

- Amazon had a need, how were they going to run amazon.com
- Something grew within their company to fill that need (and also came with [an API mandate](https://nordicapis.com/the-bezos-api-mandate-amazons-manifesto-for-externalization/))
- The need existed for other companies and Amazon could use what had grown internally to service the world
- Lots of $$$ flowed in, and so many more data centers and AWS engineers followed

### What is AWS?

It is a MASSIVE ecosystem of cloud based services that Amazon offers to the world (for a price, of course). The products page includes over [200+ distinct offerings](https://aws.amazon.com/products/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all) at this time. The term “web service” describes the fact that these different offerings help power things on the web, but they fall into a set of distinct categories.

### Storage

You may or may not have heard of things like [S3](https://aws.amazon.com/s3/) (Simple Storage Service), a super reliable way to store file objects in AWS. Its uses are more than I can count, but I’ve seen it used to:

- Host images and static content (like a website)
- Host installation packages
- Store configuration data
- Log files!

There’s all sorts of cost structures for it but essentially the sooner you want to retrieve it, the more it will cost you.

There’s many other storage options, like RDS (Relational Data Service), a set of self hosted RDBMS offerings, or Elasticsearch/Opensearch for running a NoSQL storage solution. There’s a queue service (Amazon SQS), and genericdisk storage for servers (EBS or EFS storage). Basically if you want to store something in the Cloud, there’s an AWS offering for it.

### Workloads

The three most common families of workloads that you run in AWS are:

- Serverless (Lambda) -> You run some code but you pay by how often the code is run, not for a dedicated amount of space. You also have to have a “serverless” mindset when you do this.
- Server based (EC2) -> You run code on a dedicated server that you pay for hourly. Just like the good old days.
- Kubernetes (EKS) -> You run your workloads in an Amazon managed Kubernetes cluster. It’s basically a hybrid of the two; you pay for the nodes that are running in your cluster, but you can scale down if your don’t have that many workloads to run.

There are also some fancy machine learning things I know nothing about (yet! maybe someday 💭).

### Networking

Amazon can act as a registrar, Certificate Authority, and Authoritative Domain Name Server, meaning:

- You can register a website, like my-sick-site.com with amazon
- You can request a certificate to make the site https (i.e. secured)
- You can tell Amazon Name Servers where my-sick-site.com points to (your Load Balancer in front of your EKS/Lambda deployments, or just a dedicated EC2 as an example)

This means all your networking needs can be fulfilled without going to GoDaddy or elsewhere. You can also set up virtual private clouds (VPCs) within AWS, so your workloads and storage is not accessible over the open internet.

### Why do people pay for these things? Why do we care?

The biggest reasons to use ANY cloud provider are:

- You get a ton of compliance checks as a given (Amazon and other cloud providers
- Data backups, multi-regionality are first class features
- You aren’t running a data center (which can get pretty costly)
- Software Engineers can focus on problem solving and rely on a super comprehensive platform

Why do we care? Well, even if you know 0 things about software, maybe you use Netflix, or heck buy things off Amazon. AWS is the virtual infrastructure that many (~30% of the internet) relies on to deliver the services you rely on.

AWS is basically the trucks, roads, gas stations and inventory systems of all these companies, if you want to think of them as distributors of goods. If AWS just shut their doors overnight, it would take the internet a while to recover!

Thanks for reading!
