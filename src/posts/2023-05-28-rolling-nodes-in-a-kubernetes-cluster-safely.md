---
title: "Rolling Nodes in a Kubernetes Cluster Safely"
date: 2023-05-28
medium_url: "https://medium.com/@mckornfield/rolling-nodes-in-a-kubernetes-cluster-safely-1d7dc59d64e8"
---

Don’t blow up your long running workloads if you can help it!

![Photo by James Haworth on Unsplash](/img/rolling-nodes-in-a-kubernetes-cluster-safely/0_zcbDdJM1lXgY9zO_.jpg)

*Photo by [James Haworth](https://unsplash.com/it/@jameshaworth?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

There are a handful of options for rolling nodes in a Kubernetes cluster, and I’ll go through them here, with some code snippets and their tradeoffs.

### The Fast/ Not Safe Way

Sometimes you just want to move all the Pods off of a Node in your cluster, and if your workloads are resilient to being kicked off of a node, that’s totally fine.

Let’s say you have an EKS node, named `ip-10–1–1–1.us-east-1.compute.internal` that you want to get resources off of. (You might find the node by running `kubectl get nodes`). The fastest way is just to run the `drain` command.

```css
kubectl drain ip-10–1–1–1.us-east-1.compute.internal \ 
  --ignore-daemonsets --delete-emptydir-data
```

You’ll notice two additional flags, which won’t necessarily apply, but if they do will block your Node from draining. The `--ignore-daemonsets` flag is necessary if any Daemonset Pods are running on the Node, whereas the `--delete-emptydir-data` one is necessary if Pods are configured in a way to store state in an emptydir volume. 99% of the time, it will be safe to do this, since Daemonsets are by their nature, only as useful as the Node they’re running on, and emptydir data is usually not important data (otherwise hopefully it’d be in a Database, PVC or Object store).

Once the drain is complete, the Node will also be cordoned, meaning it will have a `SchedulingDisabled` label on it if you run`kubectl get nodes` .

If for whatever reason you want to bring the Node back in, you can run `kubectl uncordon ip-10–1–1–1.us-east-1.compute.internal` . That will allow Pods to be scheduled back on.

If you really want the Node gone, it depends on your cluster setup. For clusters with an [autoscaler](https://github.com/kubernetes/autoscaler) installed, the autoscaler *should* see the Node as not utilized and terminate it eventually.

If you happened to drain the node the autoscaler was running on, and it can’t be placed anywhere else, then another option is to simply terminate the Node, and rely on an autoscaling mechanism to replace it.

On AWS, assuming your node names map to the private DNS names, this might look something like

```kotlin
node_name=ip-10–1–1–1.us-east-1.compute.internal
instance_id=$(aws ec2 describe-instances \
   --filter Name=private-dns-name,Values=$node_name \
    --query "Reservations[*].Instances[*].[InstanceId]" --output text)

aws ec2 terminate-instances --instance-ids "$instance_id"
```

Once the Node is terminated, autoscaling should pick up that a new Node needs to be added, and reintroduce another Node into the cluster.

If you wanted to drain ALL the nodes in your cluster, you could run something like the following:

```bash
nodes=$(kubectl get nodes -oname)
for node in ${nodes}; do
    node_name=$(echo "$node" | cut -d/ -f2)
    kubectl drain $node_name \ 
      --ignore-daemonsets --delete-emptydir-data
done
```

Which would drain each node. This is probably something you want to do in concert with a scale up event, so new Nodes could come in and quickly replace your traffic.

### The Safe Way

While not remarkably different than the unsafe way, the safe way involves using `cordon` and `taint` instead of `drain` , that way you can let longer running batch workloads continue running. (Shoutout to my coworker for the idea for `taint`-ing the nodes).

Similar to before, if we use our one node, we can run

```bash
node_name=ip-10–1–1–1.us-east-1.compute.internal
kubectl cordon $node_name
kubectl taint nodes "$node_name" roll=true:NoExecute
```

What this does is:

- Stop the node from taking new Pods on (cordon)
- Taints the nodes with a NoExecute flag, so that any Pods running on it will be moved off

The beauty of the taint approach is that for your longer workloads, you can add a toleration to your Pods so they don’t immediately get booted off of the Node, and no new workloads will be able to run on the Node (due to the `cordon`).

To tolerate the `roll=true:NoExecute` taint, you’d add the following to your manifest/ scheduling code.

```vbnet
tolerations:
- key: "roll"
  operator: "Equal"
  value: "true"
  effect: "NoExecute"
```

This means that, while no new traffic would come to the Node, the old Pods can continue running until they’re done, in which case the cluster autoscaler will be smart enough to terminate/ scale-in the Node, since nothing new will be running on it.

If you want to bring the Node back in, you can run things in reverse. (Note the minus for the taint)

```bash
node_name=ip-10–1–1–1.us-east-1.compute.internal
kubectl uncordon $node_name
kubectl taint nodes "$node_name" roll=true:NoExecute-
```

Lastly, to do this for a set of Nodes:

```bash
nodes=$(kubectl get nodes -oname)
for node in ${nodes}; do
    node_name=$(echo "$node" | cut -d/ -f2)
    kubectl cordon $node_name
    kubectl taint nodes "$node_name" roll=true:NoExecute
done
```

One final tip, you can augment the list of Nodes you retrieve using the `-L` flag. For example, to get all the Nodes of a certain instance-type, you can run

```bash
instance_type=m4.large
kubectl get nodes -l node.kubernetes.io/instance-type=$instance_type -oname

# To show the information as a label in the output, use capital L
kubectl get nodes -L node.kubernetes.io/instance-type
```

Thanks for reading, hopefully that helps with rolling your Nodes!
