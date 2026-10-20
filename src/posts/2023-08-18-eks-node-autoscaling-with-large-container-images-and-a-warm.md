---
title: "EKS Node Autoscaling With Large Container Images and a Warm Pool, a Tragedy in Three Parts"
subtitle: "Our journey through improving autoscaling"
date: 2023-08-18
medium_url: "https://medium.com/@mckornfield/eks-node-autoscaling-with-large-container-images-and-a-warm-pool-a-tragedy-in-three-parts-ed3400995ce0"
---

![Photo by Ed Robertson on Unsplash (a warm pool! ha ha)](/img/eks-node-autoscaling-with-large-container-images-and-a-warm/0_6wdzW0B0lJK92A3B.jpg)

*Photo by [Ed Robertson](https://unsplash.com/@eddrobertson?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (a warm pool! ha ha)*

Imagine you’re trying to scale GPU-based workloads up and down quickly in an EKS cluster. You have some constraints, mostly that the images you’re pulling have CUDA drivers that are GB in size.

So a 3–4 GB image, pulled through a private ECR registry, still takes a minute or two. Add the EC2 start time, and it’s 2–3 minutes before you’re ready.

What could you do to make things faster? We already used an [ASG with a warm pool](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html), so why not just pull images during initialization?

Why not, indeed.

### Part 1: Pull images on a warm pool startup

You can do things in the user-data script when instances are launched into the warm pool. This makes it so you can do things like:

```bash
#user-data.sh
for image in $images{@}; do
  docker pull $image
done
```

Well, with some auth and stuff sprinkled in (also, we used [crictl](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md) because Docker is soooo 5 k8s versions ago). But that’s it! Simple, right?

We had this set up before I joined, but it caused some nasty issues. Nasty meaning corrupted docker images and things failing all over the place.

“We’re not turning that back on,” said the lead engineer.

Well, that sucks.

What else could we do then?

### Part 2: Reuse the warm pool on scale in

Amazon has this great feature for ASGs, [reuse on scale in](https://github.com/hashicorp/terraform-provider-aws/issues/23735)! Even the terraform provider supports it!

So I turned it on, and… nothing happened.

The times were still slow. WTH! I looked at the ASG logs, and sure enough, the instances were just getting terminated. So much for reuse!

Well, it turns out the [cluster autoscaler doesn’t support warm pools](https://github.com/kubernetes/autoscaler/issues/4005). It should, but it doesn’t! So setting this flag has no effect. Your poor nodes get terminated instead of getting returned to the warm pool.

Well, that also sucks… what else?

### Alternative part 2: SOCI snapshotter?!

This seemed the most WTF option, so I didn’t even go down it, but there’s [a pretty nifty feature from GKE](https://cloud.google.com/blog/products/containers-kubernetes/introducing-container-image-streaming-in-gke) to stream images so Pods can start faster. Of course, there are plenty of restrictions, one being you must be in GKE.

So we’re in EKS (AWS). What do we do then? Apparently, EKS supports the [SOCI Snapshotter](https://github.com/awslabs/soci-snapshotter) (so-CHEE) that represents an equivalent, but…

1. You have to install a plugin on the cluster (woof)
2. You have to push metadata to your OCI registry for every image (double woof)
3. I had no idea if this would even make a dent in the job start time or just move the start time into the job execution itself

So I didn’t even try it! Maybe it works but seems like a lot of extra stuff for possible gain.

Well, that possibly sucks but sounds nifty though. :)

### Part 3: Create an AMI with the images loaded

I thought this was it.

I’d talked about putting our images on an AMI since I’d heard about this issue.

“Just make it an AMI,” I said. “And all our problems will be solved.”

What could go wrong?

[AMIs are lazily loaded.](https://www.google.com/search?q=amis+lazy+loadd&oq=amis+lazy+loadd&aqs=chrome..69i57j33i160l2j33i299.2335j0j7&sourceid=chrome&ie=UTF-8) That means instead of pulling your ECR image from ECR (s3), you pull your lazily loaded AMI/EBS volume (also s3). Turns out that it’s just as slow!

Also… the time to *initialize* the [EBS volume using dd or fio](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-initialize.html)? Really long! Like, double the time to pull the dang things (10–15 minutes).

Well, that sucks x3! How will this tragedy end?

I tried initializing the EBS volumes only on the [warm pool entry side](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks-overview.html) of the lifecycle, but at that point, I think I had discovered what went wrong in Part 1 of this tragedy.

### Conclusion: Return to part 1 with lifecycle hooks

So, I think I got it figured out. We could keep doing our `for image` pull, but all we needed to do was [add a lifecycle hook](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/autoscaling_lifecycle_hook) with a sprinkling of terraform and turn back on our ill-fated friend from Part 1.

The cause of those image errors was most likely because the image was partway through getting pulled when the instance got pushed into the “Stopped” state, making it appear “pulled” but in actuality, it was *corrupted*.

Pending times for cold starts dropped from 5 minutes to around 1 minute. Pretty snazzy!

The only gotcha was that the lifecycle hook runs for both launching into the warm pool and scale-out events, so you have to tell AWS that the instance is “ready” with a [lifecycle action](https://docs.aws.amazon.com/autoscaling/ec2/userguide/tutorial-lifecycle-hook-instance-metadata.html) and make sure you only pull images during the warm-up phase. Here’s an example snippet to do this:

```bash
REGION=us-east-1 # or wherever you're at
EC2_INSTANCE_ID=$(ec2-metadata -i | cut -d" " -f2)
LIFECYCLE=$(aws autoscaling describe-auto-scaling-instances \
  --region $REGION --instance-id $INSTANCE_ID \
  | jq ".AutoScalingInstances[].LifecycleState")
if [[ $LIFECYCLE == *"Warmed"* ]]; then
# for loopy guy from before
fi
```

Hopefully this will help you with your autoscaling adventures!
