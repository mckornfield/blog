---
title: "Getting Started with the Kubernetes Go Client"
subtitle: "I mean… Kubernetes is written in Go right? So this is what you should use?"
date: 2023-01-17
medium_url: "https://medium.com/@mckornfield/getting-started-with-the-kubernetes-go-client-7087e45da491"
---

I mean… Kubernetes is written in Go right? So this is what you should use?

![Photo by aisvri on Unsplash](/img/getting-started-with-the-kubernetes-go-client/0_DIRzwATcC9sFk9_w.jpg)

*Photo by [aisvri](https://unsplash.com/@aisvri?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### What’s a Kubernetes Client (again)?

I’ll do the short explanation here since I’ve explained it in a bit more of a long form for the [Python client](https://medium.com/@mckornfield/getting-started-with-the-kubernetes-python-client-ac48199537a9). Any Kubernetes client is a way to communicate with a running Kubernetes cluster in order to do things like get the state of Pods and other resources, or create/destroy these different types of resources.

Go(lang) is one of Google’s and many other company’s backend server language of choice (makes sense for [Google since they came up with it](https://go.dev/solutions/google/)). It’s strongly typed, but not Object Oriented (take that Java!), so you’re using `functions` and `structs` instead of classes.

### Why use Go and not Python or something else?

- If you dislike Object Oriented programming (C/Rust fan-boys unite!) Go is up your alley
- It’s fast ([but maybe not as fast as Rust](https://medium.com/star-gazers/benchmarking-low-level-i-o-c-c-rust-golang-java-python-9a0d505f85f7))
- Strong typing, always good for complicated things like Kubernetes resources
- You can compile straight to binaries without weird environment dependencies, great for [building slim docker images](https://dev.to/chseki/build-a-super-minimalistic-docker-image-to-run-your-golang-app-33j0)
- Go is widely used within the Kubernetes and Docker stack, as well as for many Kubernetes Operators

There’s other cool reasons that I won’t bother with but you can read about [elsewhere](https://softwareengineeringdaily.com/2021/03/03/why-we-switched-from-python-to-go/). (Channels ooo)

### How do I download the Kubernetes client?

If you don’t have a module set up, you’ll want to follow the [formal instructions](https://go.dev/doc/tutorial/create-module). But it will something alone the lines of be:

```bash
mkdir $YOUR_PACKAGE
go mod init github.com/$YOUR_USERNAME/$YOUR_PACKAGE
```

Assuming you have a module set up, to get the latest version run:

```go
go get k8s.io/client-go@latest
```

I recommend using VSCode as well, with the Go language package installed, so you get some nice autosuggestion.

### Wait don’t I need a Kubernetes cluster?

You sure do… your best options are to use something locally like [minikube](https://minikube.sigs.k8s.io/docs/start/) or [run a trial cluster](https://github.com/learnk8s/free-kubernetes) on something like GKE or AKS. Might take you a bit to set up but it’ll be worth the wait :)

### How do I authenticate with the client?

From outside the cluster, you’ll use something like:

```go
package main

import (
 "context"
 "fmt"
 "os"
 "path/filepath"

 "k8s.io/client-go/kubernetes"
 "k8s.io/client-go/tools/clientcmd"
)

func main() {
 home, _ := os.UserHomeDir()
 kubeConfigPath := filepath.Join(home, ".kube", "config")

 config, err := clientcmd.BuildConfigFromFlags("", kubeConfigPath)
 if err != nil {
  panic(err)
 }
 client := kubernetes.NewForConfigOrDie(config)
// More to come
}
```

From inside the cluster, it’ll look like

```go
package main

import (
 "context"
 "fmt"

 "k8s.io/client-go/kubernetes"
 "k8s.io/client-go/rest"
)

func main() {
 config, err := rest.InClusterConfig()
 if err != nil {
  panic(err)
 }
 client := kubernetes.NewForConfigOrDie(config)
 // More to come
}
```

The former relies on a kubeconfig being set up, while the later relies on the config/token injected into the running pod. The path based kubeconfig is good for operating

### What can I do with this new client we created?

Anything and everything you can do with `kubectl` . Since both use the same client/server interaction.

Here’s a few ideas with sample code:

**Getting pods in a namespace**

You might do this to see what’s running, similar to a `kubectl get pods` , but then consider doing select operations, like deleting ones that fall under a set of conditions.

```go
// You can build/ use other context and opts, but this is the most basic way
ctx := context.TODO()
opts := metav1.ListOptions{}
// We ignore errors below, but they could happen.
namespace := "my-namespace"
pods, _ := client.CoreV1().Pods(namespace).List(ctx, opts)
for _, pod := range pods.Items {
  fmt.Println(pod)
  if pod.Name == "test" {
   fmt.Println("deleting test pod")
   deleteOpts := metav1.DeleteOptions{}
   client.CoreV1().Pods(namespace).Delete(ctx, pod.Name, deleteOpts)
  }
}
```

**Labelling nodes**

You could do this for lots of reasons, but a reason might be to designate a node for a specific purpose, or indicate that it’s ready. In this case we’ll say that a node “accepts-jobs”, indicating it is ready after some sort of warm up or testing period completed. You might also label a node if it is misbehaving, so that it can be cleaned up later.

```go
func labelNode(nodeName string, client *kubernetes.Clientset) error {
 ctx := context.TODO()
 opts := metav1.GetOptions{}
 node, err := kube.CoreV1().Nodes().Get(ctx, nodeName, opts)
 if err != nil {
  return err
 }
 node.Labels["accepts-jobs"] = "true"
 updateOpts := metav1.UpdateOptions{}
 node, err = kube.CoreV1().Nodes().Update(ctx, node, updateOpts)
 return err
}
```

**Scheduling Jobs**

If you built a system that scheduled jobs based on requests to an API, you could use the k8s API to schedule those jobs. This is the funkiest bit of Go code so I’ll explain it inline

```go
 
 activeDeadlineSeconds := int64(600)
 ttlSecondsAfterFinished := int32(1200)
 job := batchv1.Job{
  ObjectMeta: metav1.ObjectMeta{
   // This is the prefix for the job name
   GenerateName: "api-workload",
   Namespace:    namespace,
  },
  Spec: batchv1.JobSpec{
   // The typing is weird on this vars, so they have to be address references
   ActiveDeadlineSeconds:   &activeDeadlineSeconds,
   TTLSecondsAfterFinished: &ttlSecondsAfterFinished,
   Template: v1.PodTemplateSpec{
    // Simple label for pod, it could be something more dynamic
    ObjectMeta: metav1.ObjectMeta{
     Labels: map[string]string{"app": "api-job"},
    },
    Spec: v1.PodSpec{
     RestartPolicy: v1.RestartPolicyNever,
     // This is just a simple busybox container, it would be something
     // More useful in a real workflow
     Containers: []v1.Container{{
      Name:    "workload",
      Image:   "busybox:1.35",
      Command: []string{"sh"},
      Args:    []string{"-c", "exit", "0"},
     }},
    },
   },
  },
 }
 opts := metav1.CreateOptions{}
 createdJob, err := client.BatchV1().Jobs(namespace).Create(ctx, &job, opts)
 if err != nil {
   panic(err)
 }
 fmt.Println(createdJob)
```

This will simply create one job, that runs the busybox container which just no-ops. It could be a custom application container that did something a bit more useful.

**In summary**

The Kubernetes client in Go is a good way to build an in-cluster service (maybe something complicated like [an operator](https://github.com/prometheus-operator/prometheus-operator)?) or a scripting utility run by a user or service account to operate on a cluster.

Thanks for reading!
