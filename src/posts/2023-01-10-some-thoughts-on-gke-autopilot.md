---
title: "Some Thoughts on GKE Autopilot"
subtitle: "Let the cloud provider do the cluster management! But be patient"
date: 2023-01-10
medium_url: "https://medium.com/@mckornfield/hands-on-with-gke-autopilot-11d5a1a2141b"
---

Let the cloud provider do the cluster management! But be patient

![Photo by Sangga Rima Roman Selia on Unsplash](/img/some-thoughts-on-gke-autopilot/0_OMFqG6drOs4hKIug.jpg)

*Photo by [Sangga Rima Roman Selia](https://unsplash.com/@sxy_selia?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### What’s GKE Autopilot?

To back all the way up, Google Kubernetes Engine is Google Cloud’s managed Kubernetes service. One would hope that the folks that developed and open sourced Kubernetes would have a good managed Kubernetes setup, and I think Google delivers a decent product with their Autopilot.

Autopilot adds on top of the basic Kubernetes management the ability to attach and detach nodes based on requests. It does have some hiccups though when it comes to attaching certain node types (namely GPUs).

### The Good

If you’ve ever had to worry about autoscaling on your own, then you know it can be a bit of a pain if you’re trying to find the right node size to scale up or scale down. Generally speaking you’ll either be under-utilized (nodes with spare resources) or you’ll hit your max and your Pods won’t have anywhere to go.

Fortunately the autoscaling for Autopilot is pretty smart. For regular CPU workloads I didn’t have any issue with scale-ups, and the nodes that were attached were just the right size to fit my Pods, and were quietly moved away once the Pods spun down (I was testing out a Job based workflow).

[Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) is automatically set up, which is nice if you want to create trust relationships between ServiceAccounts running in the cluster and GCP resources, like a GS bucket. Just one less thing to think about.

### The Bad

GPU Usage can be a bit of a pain. As of this writing; I had to also stand up a [GKE Autopilot cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster#set-version) on a rapid release cycle, so that I could get all I needed as far as GPU support. I also had to do the dance of raising quotas in the various regions/zones, and waiting for the attachment request for the GPU to finally succeed. It was a bit of a nail-biter.

Zooming out, because you are leaving your node attachment to the Autopilot autoscaler, you can’t do things like set up a warm pool to help your nodes come on with images etc. that might take time to pull. You also are at the mercy of the autoscaler to find and attach nodes, which for GPUs was definitely playing the waiting game.

Pulling images can be slow, as the images I was pulling were stored in an ECR registry. Cross-cloud is not the best way to go 😆.

### Final Thoughts

If you’re looking to experiment with managed k8s options, I’d give GKE Autopilot a shot. If you’re trying to work with GPUs though, or you have requirements on how long it should take for resources to be ready, you might be better served with an AWS offering or possibly Azure.

Thanks for reading!
