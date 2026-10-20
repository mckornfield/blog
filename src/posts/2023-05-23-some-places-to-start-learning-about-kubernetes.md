---
title: "Some Places to Start Learning About Kubernetes"
date: 2023-05-23
medium_url: "https://medium.com/@mckornfield/some-places-to-start-learning-about-kubernetes-83ee350e9e01"
---

Funnily enough, everywhere but in a book

![Photo by Agence Olloweb on Unsplash](/img/some-places-to-start-learning-about-kubernetes/0_wpIIlgJo-9C5Bp6b.jpg)

*Photo by [Agence Olloweb](https://unsplash.com/@olloweb?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Wait, Why Should I? Isn’t Serverless the Best?

[Myself](https://mckornfield.medium.com/why-choose-kubernetes-over-serverless-2aabd3ed56f4) and [others](https://medium.com/@nagarjoon.b/kubernetes-vs-serverless-how-do-you-choose-e066f2ad51ea) have written about why Serverless isn’t always the right option, but knowing about a technology is an important step in *not* selecting it.

If you’re a “serverless or nothing” person you might have some major blindspots (for example, GPU based workloads don’t work in serverless 😬). Suffice it to say that Kubernetes has cemented itself as the main, non-serverless, container orchestration mechanism (sorry Docker Swarm and OpenShift), so it’ll be a good one to know!

So where can you learn about it?

### Your Job! (or Free Time!)

This is probably the most concrete piece of advice. The way that I got half decent with Kubernetes was getting on projects where I got to work with it. All of the reading I link below isn’t worth much if you don’t go out and apply it. If you’re self employed, considering trying to set things up in Kubernetes on your own machine using minikube or kubeadm, or try something out in the cloud for some $$$. Learning by doing -> 💯

### Medium

I’ve read many a Kubernetes article on Medium, and I’ve written some as well! Hearing from people who work with the technology is a good way to get a sense of what it is and how they perceive it.

Some decently rated articles about k8s:

- [How Kubernetes and Kafka Will Get You Fired](https://medium.com/@jankammerath/how-kubernetes-and-kafka-will-get-you-fired-a6dccbd36c77) (clearly k8s is not all sunshine and rainbows haha!)
- [A Set of Modern Grafana Dashboards for Kubernetes](https://medium.com/@dotdc/a-set-of-modern-grafana-dashboards-for-kubernetes-4b989c72a4b2)
- [Build a Kubernetes Operator in 10 Minutes](https://betterprogramming.pub/build-a-kubernetes-operator-in-10-minutes-11eec1492d30)
- [4 Design Patterns for Containers in Kubernetes](https://itnext.io/4-container-design-patterns-for-kubernetes-a8593028b4cd)

My own writing:

- [What is Kubernetes?](https://mckornfield.medium.com/what-the-heck-is-this-kubernetes-thing-7d66f4aa0812)
- [The Kubernetes Tools](https://mckornfield.medium.com/the-kubernetes-tools-39a730a7fceb)

### Udemy Courses

There are plenty of good Udemy courses I’m sure, but one of the best and one I’ve taken all the way through is the prep course for the CKAD (Certified Kubernetes Application Developer) Certification. [Mumshad Mannambeth](https://www.udemy.com/course/certified-kubernetes-application-developer/) is a great instructor, and the sample environment is awesome. It will give you a solid foundation to the all of the resources within Kubernetes, as well as how to use the terminal to debug and change things.

### The Docs (for k8s itself and its tooling)

I think the Kubernetes docs are pretty great. Not too verbose, but very detailed. My only complaint is that there is a lack of examples in certain cases (but that’s why StackOverflow and sample repositories exist, isn’t it?).

If you want to understand things from a technical level, they do a great job at walking you through the *why* as well as a bit of the *how* behind the technology. I also think it’s important to know about tools that help you use and configure Kubernetes, like helm, terraform or a cloud specific autoscaler. Even minikube is good if you’re trying to run things locally.

- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [Helm Docs](https://helm.sh/docs/)
- [Kubernetes Provider (terraform)](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)
- [EKS Autoscaling](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html) (links to [Karpenter](https://karpenter.sh/v0.27.5/) and the [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md) docs)
- [Minikube Docs](https://minikube.sigs.k8s.io/docs/start/)

### Books?

I haven’t found any decent books on Kubernetes itself, though they might be out there! The best I’ve found was the [SRE book](https://sre.google/sre-book/table-of-contents/) from Google, which more describes their methodology (and technically they use Borg, their internal version of Kubernetes). If you know of a good book, let me know!

Hopefully those links help you on your journey.
