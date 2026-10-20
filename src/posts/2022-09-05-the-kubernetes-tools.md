---
title: "The Kubernetes Tools"
date: 2022-09-05
medium_url: "https://medium.com/@mckornfield/the-kubernetes-tools-39a730a7fceb"
---

If you don’t know what Kubernetes is, see [my other article](https://mckornfield.medium.com/what-the-heck-is-this-kubernetes-thing-7d66f4aa0812).

These are some tools you might use to manage a cluster, both to install resources and to give the cluster certain capabilities.

All of the tools mentioned below that are not tied to a specific cloud provider are Open Source.

## Installation Management Tools

![Photo by Alina Grubnyak on Unsplash](/img/the-kubernetes-tools/0_8QHeKY-GLLSTcoqZ.jpg)

*Photo by [Alina Grubnyak](https://unsplash.com/@alinnnaaaa?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### AWS EKS (Elastic Kubernetes Service)

Amazon (and every other major cloud provider) decided to get on board the Kubernetes train and set up the system for you. Control planes? Nodes? Nah you just do something like `aws eks make-me-a-cluster` (ok it’s a bit more than that).

The main advantage here is you don’t upgrade the individual nodes and control plane OS and other sorts of maintenance. That’s why you pay Amazon (or Microsoft or Google) money!

The equivalent for Azure is [AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/) and for GCP it’s [GKE](https://cloud.google.com/kubernetes-engine).

**Terraform**

So let’s say you want to manage a cluster, but you don’t want to run AWS commands (or azure/google cli commands), nor do you want to use the web console, but instead want some nice code controlled way to manage your cluster and any other resources (VPCs, Security Groups). What sort of tool might you use?

There’s more than one option but the one I’m most familiar with is terraform. It’s a declarative, jsonnet ([like JSON but weirder](https://jsonnet.org/)) way to say “I would like one AWS EKS cluster, in this VPC, with these size nodes, and these security groups.” You can apply the terraform manually, or build an automated pipeline to run `terraform apply -auto-approve` and watch as you create all your nice cloud things without clicking in the console or running cloud api commands.

The main advantage of this terraform besides having code document the state of infrastructure is how it does state management. Terraform allows you track state in a bucket (e.g. an S3 bucket) so that state changes/ the current state are stored in the cloud and not on Fred’s machine.

Terraform’s biggest learning curve is figuring out how to work with the jsonnet files and modules (reusable bits of terraform), but as an Infrastructure as Code tool it’s one of the most common. It’s also usable with different Cloud providers, which is nice.

To compare it with something like Ansible, Ansible is a tool that you use more for making sure a machine is set in a specific way, whereas Terraform is more for making sure a set of Cloud resources/ configurations exist and in the desired configuration. Resizing instances with terraform is as simple as changing the instance size and running an apply.

### kubectl

The bread and butter of Kubernetes interactions, this is basically your “Hey Kubernetes, give the pod logs.” Or whatever other operation you want to do.

It’s very well documented but unfortunately it is a CLI only tool. There are some nice things built on top of it that make it more of a GUI-like experience (k9s, the various Managed Kubernetes dashboards), but you’ll probably have to use kubectl at some point to debug things.

Notable uses of kubectl:

- Port forwarding
- Listing different resource types (Pod, Service, Deployment, Ingress, etc.)
- Getting Logs
- Running pods/ updating resources add-hoc

### Helm

Helm is likened to “a package manager for Kubernetes,” but it’s a little beyond that. It also provides a tool to template all of your resources, so they can have different behaviors in different environments (or be called different things if deployed to the same environment).

Helm uses the concept of [**Charts**](https://artifacthub.io/)asthese reusable packages that can be installed or templated over as part of your deployments. Helm is powerful but also can be quite convoluted as templating gets more complex, and as charts depend on other charts.

Helm comes with its own binary, *helm*, which you can pass the location of the chart (either local or in a helm repository) as well as environment values from a file or injected within the command.

One of helm’s main advantages besides templating is tracking installation versions. This can be helpful when doing upgrades/ seeing why new versions of things are going wrong. It has rollback mechanisms and will automatically rollback if deployments fail.

### Helmfile

Yet another layer of abstraction over helm, this tool basically makes the helm templating easier. The concepts of different environments is built into the tool, as opposed to helm, where you layer those abstractions over yourself using different environment files. The `helmfile.yaml` is where all these different environment configurations are stored and applied using `helmfile apply` .

### Kustomize

As a competitor to helm, Kustomize is basically a way to create different deployment behavior with patching instead of templating. You install some resources or charts but at a specific path/ set of paths, you overwrite the values with what you want.

### ArgoCD

Argo is a pull based deployment tool. What that means is that instead of have a Gitlab/GitHub actions pipeline that deploys your updated charts/k8s resources, you tell Argo *where to pull the code from*, and it uses Helm/Kustomize to do the work.

The main advantage of pull based tools is that they can recover very well if the whole cluster needs to be migrated across versions/ locations, or when setting up a new cluster. The main challenge is how you verify your deployments are successful or not, since you don’t actively *push* code, but instead rely on [GitOps](https://about.gitlab.com/topics/gitops/) to upgrade your infrastructure/ applications.

## Cluster Level Resources

![Photo by Billy Huynh on Unsplash](/img/the-kubernetes-tools/0_XHd-Xg-8QJu605nh.jpg)

*Photo by [Billy Huynh](https://unsplash.com/@billy_huy?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Prometheus/Grafana/Alertmanager (metrics)

One of the bread and butter tools for collecting and displaying metrics, Prometheus is a system that will scrape /metrics endpoints that display data in a very specific format, namely a metric name, some labels, and a numerical value.

These numbers are put into a Time Series Database (TSDB) that can be easily plotted using a tool like Grafana.

Rules within Prometheus can also trigger based on how data changes within this TSDB, in order to send alerts, which are forwarded with Alertmanager.

These three tools fulfill the role of “metrics” in the three pillars of observability (the other two are tracing and logs).

### Jaeger (tracing)

Jaeger is one of the main tracing tools (the other is Zipkin?) so that you can tell how long different parts of a call within an application take, and where errors are happening within a call stack between services.

The main advantage of tracing is for diagnosing live issues; it can be immensely beneficial when you know some user interaction is slow, but don’t know WHERE exactly the slowness is. Or if there’s a set of cascading errors, where the origin of those errors are.

Jaeger has a pretty simple UI that can be used to query and move through traces. A lot of systems will also pass back a trace id (e.g. x-trace-id header) to the caller, so you can look up the trace directly.

### Loki (logs)

Loki is a tool for ingesting logs that’s a lot simpler than ELK. It is basically a glorified zipping and grepping system, but it can feed into the Grafana/Alertmanager ecosystem pretty well, allowing you to visualize log error rates, set alerts, and query for logs from within Grafana.

Loki can be hooked up to container logs within a cluster using a loki daemonset (something that runs on every node), or other tools like Vector.

### Nginx-Ingress

One of the many options for an “Ingress Controller”, or essentially a reverse proxy for the cluster, [nginx-ingress](https://github.com/kubernetes/ingress-nginx) is an option for moving traffic from outside the cluster to within the cluster.

Essentially it maps inbound traffic, based on the path or domain, to the appropriate Service ([Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/)) within the cluster. It does this by constantly updating a config file based on all the [Ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/) that exist within the cluster.

### External-dns

So you have a new resource and a new ingress, but how do things outside the cluster hit the resource? Assuming you have an Ingress resource created, [external-dns](https://github.com/kubernetes-sigs/external-dns) will create a DNS record (for the EKS example, this would be a Route53 record) so that your ingress controller and next your Service are resolvable from outside the cluster.

In the example of AWS, these external-dns records map to a LoadBalancer (ALB or ELB) that is pointing at your cluster. So the eventual path is DNS resolving to a load balancer, to your Ingress Controller, to your Service, and then to your Pod.

### Did I miss anything?

If you have a tool or service you think is instrumental to Kubernetes, let me know!
