---
title: "The -Sets of Kubernetes"
date: 2023-03-21
medium_url: "https://medium.com/@mckornfield/the-sets-of-kubernetes-de5bd7382cb5"
---

How you specify how Pods run (that aren’t Jobs)

![Photo by Mark Harpur on Unsplash](/img/the-sets-of-kubernetes/0_vTTLLKodAOMlLAZd.jpg)

*Photo by [Mark Harpur](https://unsplash.com/@luckybeanz?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Kubernetes is a way to run containers. The way those containers are run can be divided into two categories:

- **Jobs**: Containers run once or on a schedule with a specific purpose and limited lifetime
- **-Sets**: Containers run for an indefinitely with a more general purpose

This article will focus on the different types of -Sets we can have. When I say -Sets, I am referring to the suffix to:

- Daemon**Sets**
- Deployments and Replica**Sets**
- Stateful**Sets**

Let’s go through the differences between them and their usecases.

### The Differences between the -Sets

The breakdown is fairly simple:

Daemonsets -> Run one Pod on each Node in the cluster, or as many nodes as deemed necessary by taints/tolerations etc.

Deployments/ReplicaSets -> Run a specified number of expendable Pods, though the amount can always be scaled with something like an [HPA](/posts/working-with-hpas-in-kubernetes/).

Also the Deployment is [the recommended level of abstraction](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#:~:text=A%20ReplicaSet%20ensures%20that%20a,lot%20of%20other%20useful%20features.) above a ReplicaSet, but a Deployment is 1 to 1 with a ReplicaSet

StatefulSets -> Run a specific number of Pods, with a well known name/ persistent identity, that boot up and shut down in a specific order

Let’s get into the details a bit more, starting with the —

### Daemonset

Daemonsets have a very specific set of use cases. You use them when you want every Node to have the Pod you care about running.

For example, a log exporter, [an image puller](https://codefresh.io/blog/single-use-daemonset-pattern-pre-pulling-images-kubernetes/) or metric collector would be great examples of things to run in a Daemonset.

You could imagine for an image puller, if you ran `kubectl get daemonset` on an 8 node cluster, you might see:

```sql
NAME                       DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
image-puller                     8         8         8       8            8           <none>          21d
```

Where each column marks information related to how many of the Pods are running (and whether or not they are healthy/ upgraded).

If you don’t have a need for one to run on every Node, but instead a more specific, use case driven count, you might want to use a —

### Deployment/ReplicaSet

Deployments are the bread and butter of a dedicated number of expendable Pods, but not ones you intend to tie to every Node in the cluster.

This would be for running a stateless webapp, or web servers, or any sort of “do work” Pods that sit and wait for requests.

Running `kubectl get deployment` will show the number running as well as the number ready, in case some are still spinning up or crash looping.

```vbnet
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
webapp-server                         2/2            2          2    21d
```

Similarly you can run `kubectl get replicaset` to see what is lying underneath the deployment:

```sql
NAME                       DESIRED   CURRENT   READY   AGE
webapp-server-567c955fd6   2         2         2       21d
webapp-server-5fd4845b5c   0         0         0       21d
```

You’ll notice two versions of the ReplicaSet, which correspond to new versions of the Deployment. This also allows for rolling updates/ rollbacks, which is why `deployments` are recommended over `replicasets` .

If you just `kubectl get pods` you’ll be able to see the deployments much like the Daemonsets, with a trailing random alphanumeric string (i.e. a psuedo-random identity).

```sql
webapp-server-tlr5x               1/1     Running             0          4m42s
webapp-server-v7z4l               1/1     Running             0          4h3m
```

Now, what if you want to make these instances have some sort of state? In that case, you should leave behind the ReplicaSet and turn to —

### StatefulSets

If you’re going to run a database, like [ElasticSearch](https://github.com/elastic/helm-charts/blob/main/elasticsearch/templates/statefulset.yaml) or [MySQL](https://github.com/bitnami/charts/blob/main/bitnami/mysql/templates/primary/statefulset.yaml), you’ll end up deploying a StatefulSet most likely.

The fact that a StatefulSet has a specific startup order by default AND that its identity is maintained between versions makes it fit the use case of a stateful service (hence the name **Stateful**Set).

Usually these stateful services are backed by a Persistent Volume or Volumes, and binding them to a StatefulSet makes better guarantees about which service has access to the data than something like a deployment.

Running `kubectl get statefulset` you might see this for a one node MongoDB cluster

```typescript
NAME      READY   AGE
mongodb   1/1     4d6h
```

And the corresponding `kubectl get pods`

```sql
NAME                           READY   STATUS             RESTARTS         AGE
mongodb-0                      1/1     Running            0                4d6h
```

Notice that the name of the Pod doesn’t have that same suffix. That’s the main way that its identity is preserved between upgrades.

### Summary

Daemonsets -> Run a Pod on all the Nodes

Deployments/ReplicaSets -> Run a stateless set of Pods on some Nodes

StatefulSet -> Run a stateful set of Pods on some Nodes

Thanks for reading!
