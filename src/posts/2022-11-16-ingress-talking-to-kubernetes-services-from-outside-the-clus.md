---
title: "Ingress: Talking to Kubernetes Services from Outside the Cluster"
subtitle: "🎶Hello from the outside🎶"
date: 2022-11-16
medium_url: "https://medium.com/@mckornfield/ingress-talking-to-kubernetes-services-from-outside-the-cluster-333ba1f7c665"
---

🎶Hello from the outside🎶

![Photo by Michael Barón on Unsplash](/img/ingress-talking-to-kubernetes-services-from-outside-the-clus/0_njiPm5FSH-9-2_6Q.jpg)

*Photo by [Michael Barón](https://unsplash.com/@michaelbaronr?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

## What is Ingress?

The [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/ingress/) are pretty thorough, so I’ll just try to address what it is from a laymen's perspective. (If you don’t know what Kubernetes is, I did my best to explain it [here](https://medium.com/@mckornfield/what-the-heck-is-this-kubernetes-thing-7d66f4aa0812).)

For systems that communicate over the internet, there are two paths of communication: outward (egress) and inward (ingress). The reason that Kubernetes needs to be explicit about how things talk to it is that by default, Pods and Services can only be reached from within the cluster.

Because of the nature of Kubernetes, you can’t simply port-forward a worker node and just set up a domain pointing to the IP address of that node, namely because:

- Your Pod could be rescheduled onto another node
- The Node could itself could be rolled/removed from the cluster

Besides those obvious points, it seems like you’re missing a big piece of abstraction if you don’t use something like `Ingress` to talk to services within your cluster.

## Options for Ingress

You have a few categories of options for how to talk to things within a Kubernetes cluster.

A few bits of terminology to lay out:

- DNS -> Domain Name Service, also used as shorthand for the beginning part of the URL that your site has, e.g. `k8singress.com`
- `Service` -> A Kubernetes Service, which represents some sort of network based communication against one or more `Pods`
- Ingress-Controller -> A [Web Server](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) that is used to route traffic based on a properly defined `Ingress` resource
- TLD -> Top Level Domain, a domain that you can host multiple services under, e.g. `google.com` for `mail.google.com` and `docs.google.com` .

### One domain per service

Imagine that you have are running your own business and you have a couple of services within your cluster that you need accessible to customers. For this example we’ll use the `k8singress` TLD. Let’s say it’s a shopping website `shopping.k8singress.com` and a payments service that the website uses, `payments.k8singress.com`. These both map to Python applications we have running in our cluster.

In order to accomplish this, we’ll use the one two punch of [external-dns](https://github.com/kubernetes-sigs/external-dns) and [ingress-nginx](https://github.com/kubernetes/ingress-nginx). Both of them rely on those `Ingress` resources we mentioned earlier. Let’s just look at what the `shopping-ingress.yaml` might look like:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shopping-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: shopping.k8singress.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: shopping-flask
            port: 
              number: 12345
```

This relatively simple `Ingress` resource is all that’s required for external-dns and ingress-nginx to kick into action, assuming both are both installed in the cluster and properly configured. What will happen is:

- external-dns will create a DNS record that points to a LoadBalancer pointed at your cluster ([example for AWS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md))
- ingress-nginx will update one of the ingress-controller’s configs to map requests inbound on that domain to your appropriate service
- Once DNS propagates, your `shopping.k8singress.com` should be accessible to the web!

This is a pretty standard workflow for clusters hosting heterogeneous services. They each get their own domains and external-dns will do its bets to update records, assuming it has access to create them for the domains specified. It makes a ton of sense too if you plan to add/remove domains under some TLD at will.

### A domain per cluster, and a path per service

Another approach is just having one domain for the whole cluster. This would be represented as a `Service` of type `LoadBalancer` that points at your cluster on one domain. You could still use external-dns for this, but it might suffice to use something more basic, like `terraform` , since `LoadBalancer`s are much more stable than k8s resources.

Now you could handle the mapping using ingress, but what if you just want something that forwards on the URL path and ignores the domain.

Imagine your shopping site is now simply `shopping.k8singress.com/site/` and your payment API is now hosted at `shopping.k8singress.com/payments/` . This would be a better set up if you have a lot of homogeneous services and simply want to rely on paths as the resource mapping.

A good solution to this path mapping approach is [Ambassador](https://www.getambassador.io/docs/edge-stack/latest/topics/running/ingress-controller/), another type of Ingress-Controller, but one that operates on a Custom Resource called `Mapping` s.

Here’s an example of what a `Mapping` might look like for our shopping site:

```yaml
apiVersion: getambassador.io/v3alpha1
kind:  Mapping
metadata:
  name:  site-mapping
spec:
  prefix: /site/
  service: shopping-flask
```

It’s similar to the ingress in that it maps *something* to a service, but in this case it will update the Envoy proxy that Ambassador is based on to point to your service, instead of an nginx-config. It will also do it based on a path and not based on an incoming domain. In this event, you don’t use the `Ingress` resource at all at the service level, it’s managed at

### Other ways

There’s plenty of other options for [ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) though I don’t believe many more paths exist as far as pairings of domains/paths. For systems that aren’t HTTP based, it might make sense to have routing based on RPC calls, which you can still do with [nginx-ingress](https://kubernetes.github.io/ingress-nginx/examples/grpc/) but might require some extra annotations.

If you have any thoughts or questions let me know!
