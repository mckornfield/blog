---
title: "Debugging Kubernetes Pods"
subtitle: "I have spent a lot of time with botched Kubernetes deployments, and I thought it might be worth sharing some of the things I’ve come…"
date: 2022-09-19
medium_url: "https://medium.com/@mckornfield/debugging-kubernetes-pods-7bc2aba66628"
---

![Photo by Rachael Gorjestani on Unsplash](/img/debugging-kubernetes-pods/0_XQMOSn36MyRJ2KiD.jpg)

*Photo by [Rachael Gorjestani](https://unsplash.com/@rachaelgorjestani?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I have spent a lot of time with botched Kubernetes deployments, and I thought it might be worth sharing some of the things I’ve come across, typically when a `helm install` hits a wall or a `kubectl apply` goes awry.

All the variables below like `$NAMESPACE` are things you should replace with values corresponding to what you’re trying to debug.

My tl;dr list is

```
# Set the current namespace
kubectl config set-context --current --namespace $NAMESPACE
```

```
# Describe pod state
kubectl describe pod $POD_NAME
```

```
# Pod logs, following output
kubectl logs -f $POD_NAME
```

```
## Pod logs optionally with container name if necessary
kubectl logs $POD_NAME -c $CONTAINER_NAME
```

```
## Pod logs on the previous container
kubectl logs -p $POD_NAME
```

```
# Port forwarding
```

```
## Either the service
kubectl port-forward svc/$SERVICE_NAME $LOCAL_PORT:$SERVICE_PORT
## or the pod itself
kubectl port-forward $POD_NAME $LOCAL_PORT:$POD_PORT
```

### Pods stuck in a starting state

![Photo by Jonathan Farber on Unsplash](/img/debugging-kubernetes-pods/0_O-VESIjXNSlZ_-Z7.jpg)

*Photo by [Jonathan Farber](https://unsplash.com/@farber?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

This one is always annoying. Sometimes the image you put it in is wrong/ doesn’t exist. But you’ll see something like `0/1` or `1/2` for the number of pods that are up (numerator) vs. the number you asked to be up (denominator).

Generally speaking the best way to debug it is to `describe` the pod. I’ve found that aside from getting the pod logs, this is probably the most useful debugging command.

```
kubectl -n $NAMESPACE describe pod $POD_NAME
```

Or if you want to set your kubectl config so you don’t have to type `-n $NAMESPACE` every time.

```
kubectl config set-context --current --namespace $NAMESPACE
kubectl describe pod $POD_NAME
```

(For the rest of the article, assume your context is already set up as above.)

That command will be your bread and butter. You might even want to pipe it to less in case the pod description is very verbose.

```
kubectl describe pod $POD_NAME | less
```

Generally the pod will be stuck in states like `ContainerCreating` or if there’s an image issue you might see `ImagePullBackoff` , possibly indicating the image couldn’t be found or authenticated to.

If I suspect something is wrong with the definition of the pod, I might query it via:

```
kubectl get pod $POD_NAME -oyaml | less
```

To view the pods information in its realized YAML format, which can be a bit hard to look at compared with the deployment files, which don’t have all the state information that the live resources do.

Using

```
kubectl edit pod $POD_NAME
```

You can test making changes on the fly, although some changes are forbidden. Because of that and the fact that the pod could get moved, deleted, you might want to edit the deployment that oversees the pod and have the change trickle down, i.e.

```
kubectl edit deployment $DEPLOYMENT_NAME
# or if you just want to view the information
kubectl get deployment $DEPLOYMENT_NAME -oyaml
```

### Getting Pod Logs

![Photo by Marko Horvat on Unsplash](/img/debugging-kubernetes-pods/0_GOEgrHyxVrgUag7c.jpg)

*Photo by [Marko Horvat](https://unsplash.com/@lemondyt?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Pods will have one or more log streams coming out of them depending on how many containers you have within the pod. You can access them with:

```
kubectl logs $POD_NAME
# or if you want to follow continuous output
kubectl logs -f $POD_NAME
```

The logs command can be a bit tricky in the event where there’s more than one container, you might either see an error message or a message about defaulting to a certain container. To pick a specific container’s logs, use:

```
kubectl logs $POD_NAME -c $CONTAINER_NAME
```

Another super useful debugging tool is the `-p/--previous` flag, which you can use in the case that an instance keeps crashing/ there was an unexpected restart.

```
kubectl logs -p $POD_NAME
```

### Port forwarding

![Photo by Jainath Ponnala on Unsplash](/img/debugging-kubernetes-pods/0_1EWY72ktqFF6JNQE.jpg)

*Photo by [Jainath Ponnala](https://unsplash.com/@jainath?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

In case you can’t communicate with the pod via its `Service`or via the `Ingress` then port-forwarding is probably your best option.

There are two ways to port-forward a pod, either from its service or the pod itself. This is a very useful tool to communicate with the pod/service to see what might be going wrong, if things like healthchecks are failing, or endpoints don’t exist.

To port-forward the pod, use:

```
kubectl port-forward $POD_NAME $LOCAL_PORT:$POD_PORT
```

This will run continuously in your terminal, so you’ll need another terminal to further debug, or you need to send the command to the background like so:

```
kubectl port-forward $POD_NAME $LOCAL_PORT:$POD_PORT &
```

The last thing you might want to try port-forwarding is the `Service` , which represents that layer of abstraction on top of your pods (especially if you have more than one in a `StatefulSet/ReplicaSet)` . If port-forwarding the pod seems fine it might be worth port-forwarding the service, like so:

```
kubectl port-forward svc/$SERVICE_NAME $LOCAL_PORT:$POD_PORT
```

A last little trick is that if you leave the `$LOCAL_PORT` blank, then `kubectl` will select a random open port for you locally (and it should print it out).

```
kubectl port-forward svc/$SERVICE_NAME :$POD_PORT
```

### Recap

You can use `kubectl` to view the pod definition, the state it’s in, the description of it and its deployment, the logs corresponding to the pod, and port-forward the pod or its corresponding service. With all of that you should be able to debug most Kubernetes pod related issues.

That’s all I’ve got!
