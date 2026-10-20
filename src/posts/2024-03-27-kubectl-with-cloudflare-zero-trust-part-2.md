---
title: "Kubectl with Cloudflare Zero Trust, Part 2"
date: 2024-03-27
medium_url: "https://medium.com/@mckornfield/connecting-to-a-private-kubernetes-control-plane-with-cloudflare-91f86a107d4b"
---

An addendum to Cloudflare’s blog post

![Photo by Faris Mohammed on Unsplash](/img/kubectl-with-cloudflare-zero-trust-part-2/0_EaDYzx-_t0R1pe6B.jpg)

*Photo by [Faris Mohammed](https://unsplash.com/@pkmfaris?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Context

There’s a [Cloudflare blog](https://blog.cloudflare.com/kubectl-with-zero-trust) that looks promising for those who want to set up a [private control plane for EKS](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#private-access) (or any Kubernetes cluster type, for that matter). But once you follow along, you realize you’re only 60–80% of the way there. I thought I’d write a couple things the blog is missing, and which aren’t very clear from the docs.

### What the Blog in Question Gets Right

The blog has almost all the right pieces there, namely:

- You’ll register a Cloudflare Tunnel on the Cloudflare side of things (they used to be called “Argo Tunnels”)
- You need to add routes that correspond to the private IP space of your Kubernetes cluster (but this part is not well explained)
- You’ll need to add rules for not inspecting traffic
- You’ll have to run the Cloudflare Tunnel from WITHIN the Kubernetes cluster, corresponding to the one you registered and added rules/routes to

Seems super straight forward right? Well…

### Which Details Need to Be Fleshed Out

There are a few big pieces that the blog glosses over, that I think are worth calling out since they confused me. I have to give credit to this [gist](https://gist.github.com/andymotta/5919912e348f8a85b159d35e0901b38e), which made me understand what this “zero trust” piece really accomplishes.

There are two ways to route using Cloudflare to your Kubernetes Control Plane.

1. Using a [socks](https://kubernetes.io/docs/tasks/extend-kubernetes/socks5-proxy-access-api/) proxy, which there are some [threads on](https://community.cloudflare.com/t/releasing-kubectl-support-in-access/168594/3) but this is not really “zero trust”, rather an authenticated proxy
2. Connecting two networks together (the network your machine is on, and the Kubernetes cluster)

(2) Is normally accomplished with something like a VPN or corporate network, but the whole point of “zero trust” is that we can make a local network in the cluster appear as a local network on our machine (like a VPN), BUT the network will be connected to some arbitrary local network, and only allow requests on a *per machine* basis.

Doing so requires that we install the “WARP” app (essentially Cloudflare’s version of [Wireguard](https://www.wireguard.com/)) and configure it so we have a session corresponding to our Cloudflare account. We then need to set up the tunneling so that, when we try to reach out the local address space of the Kubernetes cluster, the WARP app properly redirects the requests to the IP space of the cluster via the tunnel.

### How to Set Up Cloudflare Zero Trust on Your Machine

The docs are pretty clear on this so I’ll just redirect there:

1. Set up a [Zero Trust Organization](https://developers.cloudflare.com/cloudflare-one/setup/#install-the-warp-client-on-your-devices) in the Cloudflare Console
2. [Follow their directions](https://developers.cloudflare.com/cloudflare-one/setup/#install-the-warp-client-on-your-devices) on how to download the WARP app
3. You’ll need to do some sort of “log in”, which will be specific to your Zero Trust organization. If you don’t, the default WARP app appears orange. For me, that meant associating with a Google account and logging in via a browser redirect
4. Once you have this part set up, you’ll have at least a blue “Zero Trust” switch displayed on the app

### How to Deal with Overlapping IPs

This is a major part that the blog glosses over, so let’s revisit it (just for IPv4, but the same will go for IPv6).

The blog throws this IP CIDR out `198.51.100.101/32` seemingly from nowhere. But this represents a [reserved internal IP space](https://en.wikipedia.org/wiki/Reserved_IP_addresses), and one that is specifically used for documentation. Your cluster might use something like `10.1.0.0/16` or `192.168.248.0/21` , or any of the private reserved IP CIDRs listed in that wikipedia article that are allowed within a VPC.

The key point is that you are going to make that “local IP space” appear local to your machine, meaning network traffic will be rerouted to the cluster, based on the use of the WARP app. BUT by default, your Zero Trust app doesn’t necessarily peer the Kubernetes network to your own. So you’ll need to do a few more things before `kubectl get pods` will do anything.

1. Set up a [device profile](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/configure-warp/device-profiles/) (or mess with the default if you’re feeling lucky)
2. Set up a [split tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/warp/configure-warp/route-traffic/split-tunnels/#change-split-tunnels-mode) to *include* traffic for your Kubernetes IP address, so requests to your local cluster will be sent through Cloudflare to the tunnel, and then routed to the private control plane endpoints.

Lastly, if you run into issues where multiple clusters use the same local addresses, you’ll want to consider adding [multiple virtual networks](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/private-net/cloudflared/tunnel-virtual-networks/), which you can then select from within the WARP application.

### The Chicken and Egg Problem

One thing the article completely glosses over is: how do you connect to your Kubernetes cluster to install the Cloudflare Tunnel, if you haven’t connected before? I’ll list out the options, starting with what I did:

1. Simply start with a public control plane. The threat level is relatively low to your cluster if there’s nothing in it, and once you get things working, you can switch the cluster to be completely private.
2. Use a bastion host (i.e. a machine connected to the cluster’s private network), you could also install the Cloudflare Tunnel on this machine, and then install it in the cluster using the host’s, or use a cloud specific tool like [SSM to tunnel to the instance](/posts/connecting-to-an-eks-cluster-via-bastion-host-over-a-socks5/)
3. A VPN? (But that kind of defeats the whole point of using WARP doesn’t it…)

### Summary

The tl;dr from what’s missing in [this blog](https://blog.cloudflare.com/kubectl-with-zero-trust)

- The IP CIDR it not well explained, but it’s the IP space used by the control plane of your Kubernetes cluster
- Setting up Zero Trust is not trivial and will take some time to get right
- You need to set up split tunnels (and/or multiple networks) to properly map the IP addresses
