---
title: "Kubernetes: It’s a Bunch of Loops"
date: 2023-03-23
medium_url: "https://medium.com/@mckornfield/kubernetes-its-a-bunch-of-loops-c23659d3f955"
---

Apparently it’s that simple?

![Photo by David Streit on Unsplash](/img/kubernetes-its-a-bunch-of-loops/0_-6z1IfBkHIDILey4.jpg)

*Photo by [David Streit](https://unsplash.com/@daviidstreit?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

If you need a Kubernetes refresher, [the docs](https://kubernetes.io/docs/concepts/overview/components/) will probably do it more justice than I will, but I want to focus on a core concept, which is the idea of these “loops” that run, and how the things that power these loops work.

When you create/change any resource in Kubernetes, you take two pretty important steps

- You store some data in etcd, Kubernetes’ main storage mechanism
- You kick one or more *control loops* into action, based on that new data, which try to bring the

### Etcd

Etcd is a key-value store, and one that’s not purely tied to Kubernetes. But it provides a lot of features that make it a great storage mechanism for a non-centralized system like Kubernetes ([i.e. constitency and high availability](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)).

The important thing about etcd for our “bunch of loops” concept is that the loops have to act on *something,* and essentially the something is a *desired state*.

Desired state can be thought of as a person saying to you “I’d really like it if you’d take out the trash.” If you just stand there and stare back, the desired and actual state will probably never converge. But if you begrudgingly tie up the trash and take it out (come on it’s not *that* hard), then you’ve made the desired state match the actual state.

- Desired state: Trash in the outside trash bin
- Actual state: Trash in the kitchen
- Goal: Make the actual state match the desired state

The desired state in our example is what we’ll have in etcd, something like “4 Containers running Tomcat” or “1 Spark Job running every hour.”

The desired state is then brought up against the “actual state,” something that can be learned by querying other components of Kubernetes.

How do we find the actual state, well we can use something like the —

### Kubelet

Each Node in a cluster runs a kubelet (a fancy process) that is responsible for

- Making sure the PodSpecs given to it are running
- Reporting back the status of Pods that match up with the PodSpecs

These kubelets help inform our “actual state”, which we can match up with the “desired state” stored in etcd.

The kubelet is talked to indirectly though, through something called the “apiserver”. We won’t get into it much here, but think of it as a layer between the different components of Kubernetes that you can access like any application server (i.e. with endpoints, GETs, POSTs, etc.).

### kube-controller-manager

So back to our analogy about taking out the garbage, what actually ensures that the garbage is moved from the kitchen to the outside bin? In reality it’s your brain telling you that you should make the actual state match the desired state, either so that the person who asked you to take out the trash likes you, or if you’re telling yourself to do it, then it’s your own conscious that doesn’t like all the stinky trash to stay in the kitchen, and envisions a new desired state.

In Kubernetes, the primary mechanism that keeps desired state and actual state inline is the `kube-controller-manager` . You can think of it as the conscious of the cluster, constantly checking to see if the desired states in etcd match up with the actual states presented by components like kubelet (though there are other sources of “actual states.”)

And this gets us to our loop, from the [docs](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/):

> a controller is a control loop that watches the shared state of the cluster through the apiserver and makes changes attempting to move the current state towards the desired state

And the kube-controller-manager is a set of these loops all running as one process, making changes if necessary to align desired and actual states. These loops watch and update things from Jobs, to Deployments, to the Nodes themselves.

They run very frequently (think many times a minute), so that on a moment by moment basis, the cluster and its components will attempt to bring the desired state inline with the actual state.

We didn’t talk much about the `apiserver` , but in our analogy that would be the eyes attached to our conscious mind, able to see whether or not the actual state does or does not match the desired state.

Let’s take the trash example and finish it up with how Kubernetes might decide to “take out the trash.”

1. Kubernetes has a Deployment of one Tomcat server (stored in etcd)
2. Something deletes that Deployment from etcd, either because it’s no longer needed or going to be replaced by something else (this could be done through the apiserver, or something like `kubectl` which talks to the apiserver)
3. The `kube-controller-manager` sees that the Deployment is gone, but the Pod still exists on a Node (it asks the kubelet process through the apiserver)
4. `kube-controller-manager` sends a request to delete that pod back to the API server, which the kubelet process on the Node receives, and summarily terminates the container

There you go, hopefully the “loops” of Kubernetes are a bit clearer to you.
