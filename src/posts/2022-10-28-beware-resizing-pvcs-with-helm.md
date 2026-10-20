---
title: "Beware Resizing PVCs With Helm"
date: 2022-10-28
medium_url: "https://medium.com/@mckornfield/beware-resizing-pvcs-with-helm-fcdb1f20d52b"
---

I thought cloud technologies were supposed to make disk resizing easy?!

![Photo by Jéan Béller on Unsplash](/img/beware-resizing-pvcs-with-helm/0_X6iLkAWMWOgov5lG.jpg)

*Photo by [Jéan Béller](https://unsplash.com/@jeanbeller?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

If you’ve ever performed a helm upgrade on a `StatefulSet` where you want to increase the disk, you will probably have seen this annoying error:

```
UPGRADE FAILED: failed to replace object: StatefulSet.apps \"my-statefulset\" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'template', 'updateStrategy' and 'minReadySeconds' are forbidden"
```

There is an issue on [Elasticsearch](https://github.com/elastic/helm-charts/issues/893) for this, that points at an issue on [Kubernetes itself](https://github.com/kubernetes/kubernetes/issues/68737), which boils down to: “one does not simply resize the PVC of a StatefulSet.”

Well this is pretty annoying if you’re about to run out of disk and you thought changing the helm value would buy you some more time, so what are your options?

### Use Kubectl

Very simply, if your statefulset is in dire need of more disk, but helm just barks at you that it can’t do anything about it, you simply need to do:

```
kubectl patch pvc $STATEFULSET_NAME'{ "spec": { "resources": { "requests": { "storage": "${NEW_STORAGE_NUMBER}Gi" }}}}'
```

Once that patch operation is done, running your helm change should go through just fine. A word to the wise on this as well: once you increase your disk size (assuming the StorageClass supports it), you can’t *decrease* it very easily.

### Use an Operator

So what’s the big brain approach instead of using our handy-dandy `patch` call is to use an operator. This introduces custom resources that have wrappers to handle things like resizing.

For Elasticsearch as an example, there’s a set of [autoscaling features](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autoscaling.html) that are available if you use this “[elastic cloud on kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html)” setup. It defines custom resources that correspond to things like Elasticsearch and Kibana (and the rest of our friendly stack) and it knows how to handle things like resizing via a *controller,* without encountering our dreaded `failed to replace object` error.

If you want to learn more about how to write your OWN operator, be prepared for a big dig, but here are the [docs](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

### Bonus: Cleaning things up

Maybe you just want to delete some old files and not resize things. That’s totally an option too!

Let’s say you want to delete files older than 30 days in a folder, maybe a set of logs or flat storage. Linux has you covered:

```
k exec $STATEFUL_SET -- find /data/ -mtime +30 -delete
```

Thanks for reading!
