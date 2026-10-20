---
title: "Weird Gotchas with EKS Autoscaling Groups"
subtitle: "Some things that have bitten me recently that I thought might be worthwhile to pass on"
date: 2023-09-19
medium_url: "https://medium.com/@mckornfield/weird-gotchas-with-eks-autoscaling-groups-c8e1eeaa04ea"
---

![Photo by Ivan Rudoy on Unsplash](/img/weird-gotchas-with-eks-autoscaling-groups/0_OqQYfZRZBTrts2Jx.jpg)

*Photo by [Ivan Rudoy](https://unsplash.com/@rudoy?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Availability Zone Rebalancing Taking Down Nodes

AWS Autoscaling Groups (ASGs) have a feature known as “AZRebalancing”. This is touted as a [benefit by AWS](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html), essentially they will launch instances for you in different AZs, and then turn off other instances.

This is fine if you’re running only stateless workloads, but if you have some long running workloads you’d rather not restart (especially if they’re stateful), then you can simply disable this feature, though the terminology is bizarre (you “suspend a process”).

If you’re using the `aws_autoscaling_group` terraform resource, you can disable it like so:

```bash
resource "aws_autoscaling_group" "group" {
  ...
  suspended_processes = ["AZRebalance"]
}
```

We use the [cluster autoscaler](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md), which currently terminates nodes individually (more on that in a moment), so the fact that AWS is taking nodes down in your ASG based on “scale-in” might be something completely undesired.

If you’d like to stop nodes from getting taken down because of scale downs, you can set nodes [to be protected from scale in](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-protection.html). In terraform this would be:

```bash
resource "aws_autoscaling_group" "group" {
  ...
  protect_from_scale_in = true
}
```

This will still let the cluster autoscaler terminate your instances but not AWS’ own autoscaling logic.

Speaking of the cluster autoscaler…

### Reuse on Scale-in Doesn’t Work with the Cluster Autoscaler

If you’ve used warm pools to try to speed up your autoscaling, you might have tried to work with the [reuse on scale in](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_InstanceReusePolicy.html) setting. But as I [wrote about before](https://medium.com/better-programming/eks-node-autoscaling-with-large-container-images-and-a-warm-pool-a-tragedy-in-three-parts-ed3400995ce0), this feature doesn’t work currently, since the cluster autoscaler simply terminates the instances instead of trying to work with a regular set of instance scale-in.

Conceivably it could be made to support it by disable protection on a node, cordoning it, and lowering the instance count, but we’re not there yet, so our protection from the first section remains the same.

### Lifecycle Hooks Can Be Tricky

If you’re trying to use a warm pool/ hook into the lifecycle phases that AWS presents when starting a node, you’ll need to be wary of the extra permissions required to run these lifecycle hooks.

Your nodes will need permission to update the lifecycle hook themselves, i.e. a policy document similar to the following:

```kotlin
data "aws_iam_policy_document" "node_policy" {
  statement {
    actions = [
      "autoscaling:CompleteLifecycleAction",
    ]
    resources = ["*"]
  }
}
```

If your workers don’t have this action, they can’t call

```typescript
aws autoscaling complete-lifecycle-action ...
```

successfully, meaning they’ll go into an error state and the phase will follow whatever you set it to do (Continue or Abandon).

Hopefully one of these gotchas helps you with ASGs in EKS!
