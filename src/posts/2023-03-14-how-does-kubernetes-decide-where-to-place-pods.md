---
title: "How Does Kubernetes Decide Where to Place Pods?"
subtitle: "Where, oh where, should I place this Pod?"
date: 2023-03-14
medium_url: "https://medium.com/@mckornfield/how-does-kubernetes-decide-where-to-place-pods-2f6701b3ca55"
---

![Photo by Mila on Unsplash](/img/how-does-kubernetes-decide-where-to-place-pods/0_nu5TMOCndj9lfLnY.jpg)

*Photo by [Mila](https://unsplash.com/@imoflow_me?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Kubernetes sits somewhere in between a fully serverless system like AWS Lambda and a dedicated server system like EC2.

In Lambda or any serverless setup, you have almost no control over where your containers run, other than the region.

In a dedicated server setup, you specify exactly where you want software to run, using Ansible, terraform, or simply running BASH commands to install services.

With Kubernetes, there’s basically a set of rules that determine where your running containers (i.e. Pods) end up. It’s a choice between the various places in the cluster, known as Nodes.

How does this work?

Well, it’s basically a set of decisions the [kube-scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/) has to weigh. There’s the question of possibility (can this actually go here?) vs. preference (is this node a *better* place than another one).

Somewhat in order, the scheduler cares about:

- Resources
- Taints + Tolerations
- Node Selectors
- Affinity and anti-affinity

Let's walk through what each of these are and how they play into the scheduling process.

### Resources

Pods can specify a number of resources in the form of *requests* and *limits*. If the scheduler can’t find any Nodes with resources available to meet the requested amount, it will show up in the description of the Pod.

(Note, there will also be something mentioned in this warning about *preemption* here, which is a fancy word for moving Pods from where they’re currently running. If Pods are able to be [preempted](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#preemption), the scheduler will move them to help schedule pods.)

[Resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) requests can be for:

- Memory
- CPUs
- GPUs
- Temporary storage

Assuming you have at least one Node available that meets the resource request, the scheduler will place it there. In the case where no Node is available, but a new Node being added would help, a [cluster autoscaler](https://github.com/kubernetes/autoscaler) can come into play to give the scheduler the ability to place a pod.

### Taints and tolerations

A `taint` is a marking on a Node that prevents pods from being scheduled there. Think of it like adding anchovies to the Node. If your Pod doesn’t like anchovies, then it won’t schedule on that node.

```perl
kubectl taint nodes my-node topping=anchovies:NoSchedule
```

In order for a Pod to be scheduled on a Node with a taint, it needs to be able to handle that taint. The mechanism to handle a taint is a `toleration` .

Under the tolerations section for a Pod/Deployment/Daemonset, you’d add something like

```vbnet
tolerations:
- key: "topping"
  operator: "Equal"
  value: "anchovies"
  effect: "NoSchedule"
```

To be able to handle the anchovies taint. This would allow your Pod to schedule on the tainted node.

### Node Selectors

Nodes can have labels. Most nodes in a cluster have lots of labels, everything from the instance type if running in a public cloud, to the type of processor. Just in `minikube`, the label for my node looks like:

```bash
Labels:             beta.kubernetes.io/arch=arm64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=arm64
                    kubernetes.io/hostname=local
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=62e108c3dfdec8029a890ad6d8ef96b6461426dc
                    minikube.k8s.io/name=local
                    minikube.k8s.io/primary=true
                    minikube.k8s.io/updated_at=2022_12_08T16_09_19_0700
                    minikube.k8s.io/version=v1.26.1
                    node-role.kubernetes.io/control-plane=
```

These labels can be added, using something like `terraform` or just a `kubectl` command:

```perl
kubectl label node local my-label=go-here
```

NodeSelectors are a way to decide what node you want to place a Pod based on the `labels` that a Node has. If I wanted to match the `mylabel=go-here` , I’d place this in the `nodeSelector` section for my Pod.

```yaml
  nodeSelector:
    my-label: go-here
```

In the event that no label matches, the Pod would fail to schedule unless the autoscaler could help once again by scaling up to bring a Node in that matches the labels.

## Affinity

### Node Affinity

Slightly different than the concept of Node Selectors is Node Affinity. The main differences are:

- Node Affinity is expressed as a list of weighted matches
- Node Affinity can be required or preferred

If you’ve ever seen a Node Affinity block, you’ll remember this enormous key, `requiredDuringSchedulingIgnoredDuringExecution` or `preferredDuringSchedulingIgnoredDuringExecution` . They mean what they say, which is the `required` block acts much like a `nodeSelector` block, but the `preferred` helps the scheduler make a decision, but is not blocking (i.e. if no Node matches, the scheduler will simply ignore the `preferred` block).

The `IgnoredDuringExecution` bit just means that once you place the Pod, even if the labels change, the Pod won’t necessarily be evicted.

Here’s an example, matching the label from before in a required-ness sense, but matching a new label based on preference.

```yaml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: my-label
            operator: In
            values:
            - go-here
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: my-other-label
            operator: In
            values:
            - go-there
```

A use-case for the preferred label could be a Node that’s labeled as being warm/cached, in the event that there’s some Kubernetes driven startup.

Most of the time you’ll want to require Pods to be placed on Nodes if there are special features to those nodes, like different hardware (e.g. GPUs) that you want only GPU-based jobs to run on.

### Pod Affinity and Pod Anti-affinity

Our last category of placement is Pod affinity and anti-affinity. This functions just like Node Affinity, but instead, we’re going to either seek out or avoid being placed on the same Node as other Pods.

A good reason for Pod anti-affinity is if Pods interact poorly when scheduled on the same Node. Conversely, if you have a reason for wanting Pods to be placed on the same Node, Pod Affinity will do the trick.

Similar to our example before, the affinities can also be `required` or `preferred` .

```yaml
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - redis-cache
        topologyKey: "kubernetes.io/hostname"
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - ml-training
          topologyKey: "kubernetes.io/hostname"
```

You could imagine the above Pod Affinity/Anti-affinity would be for an application server Pod, that wants to be close to the redis-cache running in the cluster, but doesn’t want to be on the same node as any Machine Learning jobs that could be resource intensive.

## Summary

To summarize, there are many ways that the kube-scheduler decides where to place Pods. They are:

- Resources (what will this Pod use to run?)
- Taints + Tolerations (which Nodes is this Pod even allowed to run on?)
- NodeSelectors (which Nodes does this Pod *want* to run on?)
- Affinities/Anti-affinities (which Nodes/Pods does this Pod want to run on/ not run near, or *prefer* to run on?)

I tried to keep honest with the docs [here](http://Taints%20+%20Tolerations%20%28which%20Nodes%20is%20this%20Pod%20even%20allowed%20to%20run%20on?%29), feel free to check them out if you want more examples. Thanks for reading!
