---
title: "Why Choose Kubernetes Over Serverless?"
date: 2023-02-01
medium_url: "https://medium.com/@mckornfield/why-choose-kubernetes-over-serverless-2aabd3ed56f4"
---

Managing infrastructure stinks, doesn’t it?

![Serverless tech fighting Kubernetes over DevX and Cloud Agnosticism](/img/why-choose-kubernetes-over-serverless/1_EAZRtMSA_JCfaWT7O7g2FQ.png.png)

*Serverless tech fighting Kubernetes over DevX and Cloud Agnosticism*

### To Server or Not To Server

Applications built using “serverless” technologies are all the rage these days.

Azure Functions, Google Cloud Serverless, AWS Lambda and I’m sure there are equivalents on all the other cloud providers (DigitalOcean calls them Functions too!)

The main appeal with a serverless setup is that [you pay as you use it](https://aws.amazon.com/lambda/pricing/). You aren’t paying for dedicated VMs unless your serverless functions are getting called, so you can save costs when you don’t use them, and scale up and down pretty easily. It seems like a no brainer to move away from running your own server and/or VMs and shift to running in a serverless architecture, doesn’t it?

### The Drawbacks to Serverless

I really have only seen two major things that impede the adoption of serverless at the companies I’ve worked at. They are:

- Development Experience
- Lack of Cloud Agnosticism

For both of these points I’ve felt the serverless technology I’ve worked with most (AWS Lambda) has a handful of deal breakers. Let’s get into why each is lacking for serverless, and why something like Kubernetes is a better fit.

### Development Experience for Serverless

Projects that I’ve worked with that involved serverless had very awkward development workflows. These included things like deploying over a lambda in a shared environment, or merging and praying that the lambda update would be the way folks wanted. A lot of this had to do with how serverless changes are applied.

Since serverless requires some sort of cloud based deployment (i.e. running a CloudFormation script or some terraform), it’s generally a bit more complicated to namespace and deploy changes from a branch. I haven’t seen a very good approach to this, and don’t think serverless really has namespacing in mind, like Kubernetes does.

AWS Lambdas used as a web service are generally locked down, to where you can’t easily invoke them except through an API gateway. You *can* open them up to be invokable, but the [payloads to send to Lambdas](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html) are also not very straight forward.

You can [develop and test lambdas locally](https://medium.com/geekculture/developing-aws-lambda-functions-locally-879dad302e5a), sure, but you miss out on integrating and testing them within a larger architecture, and you also get away from developing in a “cloud native” way.

Compare these development experience woes to Kubernetes.

- In Kubernetes, namespacing is a first class concept, where resources can run in their own namespace and be completely separated from each other. It’s also easier to have multiple deployments next to each other with names based on a development branch
- Kubernetes is not as prescriptive about the message formats either, as it allows you to deploy whatever type of application you want, be it a node.js server or fast-api app

### Lack of Cloud Agnosticism With Serverless

The main benefit to serverless, the fact that you don’t worry about managing infrastructure, alsos comes at a cost.

Someone IS managing that infrastructure, specifically the cloud provider you’re paying for. That cloud provider has a very specific mechanism to deploy into its serverless architecture, which does not translate across vendors.

Take a supposedly cloud agnostic deployment mechanism, like Terraform. Terraform has separate resource types for the different cloud providers serverless technologies ([AWS](https://registry.terraform.io/modules/terraform-aws-modules/lambda/aws/latest) vs. [GCP](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function) vs. [Azure](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app)).

If you’re trying to sell a software product that can be deployed across different clouds, you’re going to need to package and maintain multiple configurations to deploy your application.

Conversely, Kubernetes is built as a technology that is supposed to be “Cloud Agnostic.” You can also run it locally using minikube. What this enables you to do is package and release a single set of manifests, i.e. a helm chart or a set of resources with a kustomize file, and then anyone can install them with a sprinkling of cloud specific tweaks, e.g. annotations specific to AWS, Azure or GCP, and be up and running pretty quickly.

The best thing about this Cloud Agnostic aspect to Kubernetes is that the layer of Kubernetes serves as an abstraction layer, so that you can ignore the fact that your application is in AKS instead of EKS or GKE.

It matters very little if you’re just running your application in one cloud provider and never migrate it, but if your goal is to run your application in separate clouds or have customers run it themselves, Kubernetes provides that shared understanding you can install into.

### The Best of Both Worlds, Serverless In Kubernetes?

Yes, such a thing exists. [Knative](https://knative.dev/docs/) is one of the implementations of this sort of setup, and having your node scaling set up properly for the Kubernetes cluster means you can get similar cost savings to serverless, but run your workloads in a Cloud Agnostic, better Development Experience workflow.

But that’s a story for another time. Just know that it or something like it can help get the benefits from serverless but in a Kubernetes environment.

Thanks for reading!
