---
title: "The OS of the Cloud: Kubernetes"
date: 2024-11-24
medium_url: "https://medium.com/@mckornfield/the-os-of-the-cloud-kubernetes-c5eaa55c3c54"
---

And why other deployment paradigms aren’t

![As mentioned in the Tweet, “Why Kubernetes is King”](/img/the-os-of-the-cloud-kubernetes/1_botfiC8YcjBpySfFJ-gwpQ.png.png)

*As mentioned in the Tweet, “Why Kubernetes is King”*

A coworker told me the other day about [an X Post](https://x.com/todaywasawesome/status/1782821797274218670) he’d read saying that Kubernetes is the OS of the cloud. I think it’s right, but more important than that, WHY it’s right.

### My Experience with Kubernetes

I had just started working as an IT consultant in Virginia in 2015. I knew nothing about containers, and [Kubernetes had been out about a year](https://en.wikipedia.org/wiki/Kubernetes). The product we worked with at that time was a classic Java app, running bare metal on Windows or Linux.

A friend of my boss was out with us at a bar and started talking about [a new paradigm for running software](https://en.wikipedia.org/wiki/Docker_%28software%29). He said that most of the time we think of either running software as a process on a machine, or as a VM, but that this new way gave the efficiency of a process, but the isolation of a VM. He was the first person who explained containers to me.

I ended up moving to the engineering side (which included a fun time learning Java), and got to see our company move from running it service as a process, to a set of containers, to a Kubernetes application. I saw us go from using a self deployed Kubernetes cluster (kops) to using Amazon’s managed solution (EKS).

Where I work now, we have a mandate to run as much of our software stack as possible within Kubernetes, even though much of the workloads are ML based and [require GPUs](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/).

To understand why Kubernetes is the OS of choice for the cloud, it might help to understand why other options are not.

### But What About Other FaaS and Managed Container Orchestration?

I’ve written before about why folks should prefer [Kubernetes over a tool like AWS Lambda](/posts/why-choose-kubernetes-over-serverless/), but I haven’t addressed something like ECS, or any of the other myriad runtimes that you can use with AWS (like Beanstalk or just plain EC2).

The biggest issue I have seen with any cloud specific runtime is a lack of portability. Let’s look at each in short:

### FaaS (Function as a Service)

If you want to redeploy your FaaS solution (let’s say AWS Lambda) to another cloud (let’s say Azure Functions), all of the wrapping around your setup has to be swapped out.

- You can’t simply port over the function signatures (they’re different)
- The mechanisms by which you call the functions (either CLI invocation or via API Gateway) aren’t the same
- The whole deployment story is different (even with a tool that supports multiple clouds, like Terraform)

You run into the case where you have to support two (or N?) deployment mechanisms if you build your software around FaaS.

As I also mentioned the previous time I wrote about them, there are some other drawbacks to going with a FaaS solution

- Cold starts (i.e. starting the whole container for one function call)
- Limited debuggability (the cloud provider is running things “for you”)
- The lack of a local experience (no equivalent to minikube/kind for local)

I think FaaS has its place, but it should be the exception, not the rule, when writing cloud based software.

**Managed Container Orchestration (Elastic Container Service, ECS, etc.)**

I think the argument against these is simpler than against FaaS. FaaS is a different way of viewing software (lifting a function to a service level), whereas tools like ECS to me are just Kubernetes without the common aspects of Kubernetes.

If you spin up an ECS Task, you’ll find that your window into how things are running is much more limited than having the set of kube APIs at your disposal. Same goes for Azure Container Apps or Cloud Run.

The managed container runtimes are most certainly running some version of Kubernetes (or a similar container orchestration mechanism), but abstract it all away. I believe this approach has many of the negatives of a FaaS solution (cloud specific lock-in, lower debuggability, no local experience), but also misses the upsides of FaaS (pay for what you use, much more limited surface areas).

In my opinion, cloud specific managed container runtimes are not something anyone should invest time in.

### What Makes Kubernetes the “OS” of choice

In my experience, there were only two open source container runtimes that got anywhere:

- Docker (Docker compose and docker swarm)
- Kubernetes

There are a few others as well

- Nomad (from Hashicorp)
- Openshift (from RedHat)

As a tool, I don’t know if Kubernetes is vastly superior to these (I’ve used docker compose/swarm and it seemed OK). I think, weirdly enough, what makes Kubernetes the OS of choice is that it was *chosen*.

There are so many tools that have been built specifically for Kubernetes, and just like Kubernetes itself, many of them are open source. This includes things like:

- Prometheus/Grafana (monitoring)
- All sorts of Ingress tools (Envoy based ones like Ambassador or Envoy Gateway, or Nginx Ingress)
- Various service mesh tools (Istio, Linkerd, Cilium)
- A Cloud Agnostic (or really, many cloud supported) Autoscaler
- Networking plugins for each of the cloud providers
- A bunch of cool deployment tools (ArgoCD, Flux)

You can see a more comprehensive list [here](https://github.com/collabnix/kubetools). Why so much support, especially in an open source setting? Being part of the [Cloud Native Computing Foundation](https://www.cncf.io/blog/2024/06/07/kubernetes-is-ten-years-old/#:~:text=On%20March%2010%2C%202016%2C%20Kubernetes,Beda%20explained%20its%20inner%20workings.) (CNCF) certainly helps. Another piece of its OS adoption I think is that, while it is a Golang rewrite of Google’s internal deployment tool, Borg, Kubernetes itself is not tightly coupled to any cloud provider.

Beyond this decision, all of the major cloud providers decided to offer a managed Kubernetes option, meaning the bar to getting started was lowered significantly from the days of using a tool like [kops](https://kops.sigs.k8s.io/).

All of this support comes with the ways that Kubernetes shines beyond FaaS or managed container runtimes, namely:

- You can dig deeper if need be, i.e., pop the hood, if things go wrong
- Its portability between clouds and local environments is better than most tools
- It provides a common deployment and packaging paradigm

### Kubernetes Might Be King, but it’s not Easy

I think the biggest misses Kubernetes has as a technology is that it doesn’t provide the same **ease of use** as the tools mentioned (like FaaS or cloud specific, managed container runtimes).

That is the tradeoff with [power: responsibility](https://en.wikipedia.org/wiki/With_great_power_comes_great_responsibility). But I think moving as much of the responsibility of the deployment and management of software to the person who’s creating that software is the right path to proper mastery, though it might not be easy. It’s what [DevOps means](https://www.blackduck.com/glossary/what-is-devops.html#:~:text=Definition,than%20traditional%20software%20development%20processes.), does it not?

That is something I think that is improved by making the technology itself easier to use, and also by improving how folks learn about the technology. The current best approaches to learning I have seen are online courseware that prepares you for a comprehensive test, like the [Certified Kubernetes Application Developer](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/) (CKAD) test.

I’d love to see it and also learning about container technologies show up at an earlier time, like in college or even high school. Being exposed to these technologies earlier I think will help the next generation of developers both be more comfortable with them, and improve them so they can be more extensible/ understandable.

I also think larger companies do a disservice to their employees when they wrap their deployment paradigm (Kubernetes or not) in so many layers of abstraction so that developers can’t easily see how things are “deployed.” I’ve done plenty of interviews where people mention they use an internal tool that functions more like a FaaS or managed container runtime, and doesn’t let you peel back the layers, especially when things go wrong.

### Summary

Kubernetes isn’t easy to use, but it’s supported by many many tools and most of the major cloud providers. It can be run locally and on a single node as easily as on 100s of nodes, making it a tool great for moving from experimentation to a fully operationalized system.

There’s no better single deployment technology you can learn and master if you want to become a solid DevOps Engineer.

## Cubed

*Thank you for being a part of the community! Before you go:*

- Be sure to **clap** and **follow** the writer ️👏**️️**
- Follow us: [**X**](https://twitter.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
- [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
- Visit our platforms: [**CoFeed**](https://cofeed.app/) | [**In Plain English**](https://plainenglish.io/) | [**Venture**](https://venturemagazine.net/) | [**Cubed**](https://cubed.run/)
