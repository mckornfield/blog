---
title: "What is Kubernetes?"
date: 2022-09-05
medium_url: "https://medium.com/@mckornfield/what-the-heck-is-this-kubernetes-thing-7d66f4aa0812"
---

![Photo by garrett parker on Unsplash](/img/what-is-kubernetes/0_FDdgvvUjF4oqLoIw.jpg)

*Photo by [garrett parker](https://unsplash.com/@garrettpsystems?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Let’s start with the very basics. I mean super basic, like what is a computer, and what are the different ways it can run? That’s what we’ll need before we get to “k8s” (as some people refer to it, notice “ubernete” is 8 letters).

Also Kubernetes means “helmsman” in Greek, so that might explain the weird sea association all the tools have.

## The Basics (feel free to skip if you are an IT pro💪)

### Computers and Virtual Machines

A computer is a pretty versatile piece of technology that can execute instructions handed to it, either in a language it understands (machine code) or in a language it doesn’t understand but a friend (such as a Virtual Machine) understands. It executes these instructions using some the parts you might have heard of (a CPU, RAM, Disk) etc.

Wait hold on, *virtual machine*? Yes, basically a computer running inside of a computer. There’s something very fancy that allows these Virtual Machines to talk to your physical machine, a *hypervisor*. I won’t go into any other detail other than that they are fancy, and they turn instructions that only a Virtual Machine (VM) understands into instructions your machine understands.

So computers are machines that execute instructions, and virtual machines are an abstraction OVER those machines.

Some awesome examples of Virtual Machines include:

- the Java Virtual Machine (yes that’s every Android smartphone)
- the Javascript V8 engine (every browser basically)
- Amazon’s Virtual Machines, EC2s ([33% of the internet?](https://www.forbes.com/sites/danrunkevicius/2020/09/03/how-amazon-quietly-powers-the-internet/?sh=908974309206))

So if you use a computer or a phone, you probably use a Virtual Machine.

### It’s all about the namespaces

But what if you don’t want to use a virtual machine? Or, you don’t need to use all of the resources that it’s using at once? [Some super smart people at Google figured this out](https://en.wikipedia.org/wiki/Cgroups) because they wanted to use the VMs/ physical machines they had set up more efficiently. So instead of having a VM (which can be heavy weight) or one physical machine running a bunch of processes that can all interact with each other, these engineers came up with *cgroups*.

The tl;dr version of cgroups is that they allow processes to think that they’re the only processes running on the machine (i.e. “namespaced processes”). And they can have access to a snapshot of a file system, a set of “bins and libs”, that only they know about. These cgroups are a pretty low level linux thing, so some other people came along and productized things.

Enter “Docker”

### Containers (and Docker)

![docker architecture from openclipart.org](/img/what-is-kubernetes/1_OfMW2VvQBEnt6ftKRBAxlw.png.png)

*docker architecture from [openclipart.org](https://openclipart.org/detail/226503/dockerarchitecture)*

The concept of C-Groups is sometimes called “OS-level virtualization.” This describes the namespaced processes concept in another manner. What the difference is between Docker and other technology like it, is that they add more abstractions that make it easier for folks to use cgroups.

[Docker](https://en.wikipedia.org/wiki/Docker_%28software%29) is the biggest name in the “container runtime” space, probably because they set up a really good ecosystem around managing these file system snapshots, or “images”.

Images are the file system that a namespaced process/container sees, including a version of the OS (which is weird), binaries (stuff to run), libraries (things you depend on to run other things) and files (whatever else).

With Docker and its supporting image repository, [Dockerhub](https://hub.docker.com/), it’s super easy to push and pull images and run containers with nothing other than the docker runtime setup.

Some advantages of containers include:

- Reusable and immutable code execution
- Consistency across environments
- Lightweight resource utilization (based on process, not on whole OS)
- Fine-grained control over resource utilization (can kill runaway processes)

### OK please just tell me what Kubernetes is

Alright, alright, we finally know enough (at a 10,000 foot view) to know what Kubernetes is:

It’s a (very complicated) layer of abstraction over containers. This family of technologies is known as “Container Orchestration.”

Instead of explaining Kubernetes, let’s take what we’ve learned so far and analogize it. Imagine you own an apartment complex. There’s a few ways you could manage the properties, you could buy and sell each unit as its own property, and there’d be some fees they’d pay to you as the “property manager” (that’s our closest analogy to a virtual machine running on a physical machine).

Now let’s say instead you decide to turn each unit into a rental. OK, there’s still a lot of work to do to manage people coming in and out and renting, and leases are usually for a while, so that ties up resources for quite a bit (these are our “containers”, but we just run them and don’t actively manage anything once they’re set up unless things change).

Lastly, let’s say we decide to turn them all into Airbnbs. Now each of them are in use only when people are renting them, and we can more finely control how the pieces are used. We also use Airbnb to advertise when the rentals are available and allow people to schedule/book them through the site. Airbnb is our Container Orchestration in this analogy.

Airbnb is our Kubernetes. It offers ways to have these containers (in Kubernetes parlance, Pods) talk to each other and to the outside world. It can schedule those Pods on different nodes in case something happens to that node. Kubernetes is the big brother/ Airbnb of container orchestration. It is Google’s opensource version of their tool, [Borg](https://research.google/pubs/pub43438/).

### Cluster you say? Nodes you say?

![Kubernetes image from wikipedia.org](/img/what-is-kubernetes/1_2n7a_9paxCGgdTzaKqqJtA.png.png)

*Kubernetes image from [wikipedia.org](https://commons.wikimedia.org/wiki/File:Kubernetes.png)*

One of the core principles of Kubernetes that makes it go beyond “containers” is that you imagine that one or more nodes could go down at any time. Maybe someone tripped over a cable, or maybe the data-center lost connection to the internet.

Cloud Providers offer ways to avoid an outage by having Data Centers in different “availability zones.” Kubernetes helps with this by allowing you to have nodes and the control plane running in different zones, and rebalancing the placement of services if one or more Nodes are unresponsive.

The true power of this tool is that you abstract away “where things are” so that you can survive high load/ high traffic events or disasters that knock out part of your cluster. It’s all in the Container Management 👍

## What sorts of terms do I need to know?

- `Node`  
  - A Virtual/Physical machine that represents a single unit in the cluster  
  - These can be worker nodes or part of the Control Plane (which is where the “management” pieces of the cluster run instead of the “application” pieces)
- `Pods`  
  - One or more running containers that can be part of a ReplicaSet or Deployment
- `ReplicaSet`  
  - A resource that states how many pods should be running, based on what is the “required number”  
  - The Kubernetes Controller will do its best to schedule Pods
- `Deployment`  
  - An abstraction over a Replicaset, defining a shared set of labels/ configuration  
  - A notable difference between this and a statefulset is the names of Pods from a Deployment are semi-random, with hashes in them.   
  - Deployments are by their nature replaceable and scalable, and the order by which things spin up or down doesn’t matter
- `Daemonset`  
  - A special kind of Pod controller where a Pod is run on every node that it can (see Taints and Tolerations)
- `StatefulSet`  
  - A special kind of Deployment where the names are known and numbered  
  - The order that StatefulSets start and stop is determinate  
  - It’s understood that these Pods are storing some kind of state, though they don’t HAVE to
- `Labels`  
  - Metadata attached to any Kubernetes resource that changes how it can interact  
  - A notable usage includes allowing Services to match to Pods based on the labels present on the Pods
- `Taint`  
  - A special label applied to a node, so that Pods will not schedule there unless they have a…
- `Toleration`  
  - The ability to spawn on a node with a certain taint
- `Services`  
  - An abstraction over one or more pods that represents some sort of endpoint that can be hit.  
  - This endpoint is largely controlled by labels, and matching to them
- `Ingress`  
  - A resource that represents a way to get into the cluster. Usually done through an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)

### What tools do folks use with Kubernetes?

[See my article about tools](https://mckornfield.medium.com/the-kubernetes-tools-39a730a7fceb).
