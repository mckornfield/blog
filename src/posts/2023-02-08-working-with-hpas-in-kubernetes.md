---
title: "Working with HPAs in Kubernetes"
date: 2023-02-08
medium_url: "https://medium.com/@mckornfield/working-with-hpas-in-kubernetes-ced39263b596"
---

How to make your Kubernetes workloads scale with a few simple steps

![Photo by Pawel Czerwinski on Unsplash](/img/working-with-hpas-in-kubernetes/0_1V2m2s_r7evroNA3.jpg)

*Photo by [Pawel Czerwinski](https://unsplash.com/@pawel_czerwinski?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### What is an HPA?

HPAs (horizontal pod autoscalers) are one of the two ways to scale your services elastically within Kubernetes. In the event that your pod is under sufficient load, then you can scale up the number of pods in use. You can also scale down in the event that your pods are underutilized, thereby freeing up resources within your cluster.

The other way to scale, a VPA or vertical pod autoscaler, simply allocates more resources to your pods. We’ll ignore that for this deep dive.

Remember:

- Horizontal -> More replicas of the same thing
- Vertical -> A larger amount of resources for one thing

So how do we tell the HPA to scale up? Well, first we’ll need to have metrics about the pods themselves. That means we need.

### The Metrics Server

The most basic way to get resources exported in a Kubernetes cluster is to run the metrics server. It exports metrics at a minimum of 15 seconds, so there’s a bit of a delay, but it’s good enough for our HPA needs.

The installation is very simple if you have cluster-admin privileges.

As an apply:

`kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`

As a helm install:

```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm upgrade --install metrics-server metrics-server/metrics-server
```

You can see if it’s running by using

`kubectl get deployment metrics-server -n kube-system`

And in any namespace with runing commands like `kubectl top pods` will now return the memory and CPU usage for running pods.

There are more advanced ways to configure an HPA metrics source, such as [Prometheus](https://towardsdatascience.com/kubernetes-hpa-with-custom-metrics-from-prometheus-9ffc201991e), but the metrics server is the simplest way to get started with pod scaling.

### What are resource limits and why do they matter for HPAs?

If you aren’t aware of resource limits in Kubernetes, it might be worth reading through the [docs](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). The short version is that every Pod can have resource values set, in the form of a `request` and a `limit` .

As an example, you could set them like so, in a deployment

```yaml
      containers:
        - name: httpbin
          image: kennethreitz/httpbin
          resources:
            requests:
              memory: "16Mi"
              cpu: "50m"
            limits:
              memory: "50Mi"
              cpu: "100m"
```

This would guarantee that you have at least the requested amount available, and you’d be able to use up to the `limits` until which point you’ll get CPU throttled or OOM killed.

Setting limits is important because if we’re going to scale based on resources, then we need to set what the limit is for our memory or CPU, as this will indicate to the HPA when we should scale up or down.

### How to install one around a deployment

Let’s get into it, how do we install an HPA as part of our deployment? The key piece will be not setting the number of replicas in our deployment, and instead letting the HPA control the scaling count for your deployment.

Here’s a complete deployment you can copy into a file and apply that creates an HPA, Service, Deployment and Namespace to put everything in. It runs a container with [httpbin](https://httpbin.org/), a testing service for different types of HTTP requests.

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: httpbin
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpbin
  namespace: httpbin
  labels:
    app: httpbin
spec:
  selector:
    matchLabels:
      app: httpbin
  template:
    metadata:
      labels:
        app: httpbin
    spec:
      containers:
        - name: httpbin
          image: kennethreitz/httpbin
          resources:
            limits:
              memory: 2G
              cpu: 1000m
            requests:
              memory: 2G
              cpu: 1000m
          ports:
            - containerPort: 80
              name: httpbin-port
---
apiVersion: v1
kind: Service
metadata:
  name: httpbin
  namespace: httpbin
spec:
  selector:
    app: httpbin
  ports:
    - name: httpbin-port
      protocol: TCP
      port: 80
      targetPort: httpbin-port
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: httpbin
  namespace: httpbin
spec:
  maxReplicas: 10
  minReplicas: 1
  metrics:
    - resource:
        name: cpu
        target:
          averageUtilization: 60
          type: Utilization
      type: Resource
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: httpbin
```

**Edit:** You could also remove the last section defining the HPA in YAML and instead run the following to generate the HPA.

```python
kubectl autoscale deployment httpbin --cpu-percent=50 --min=1 --max=10
```

The most important thing to notice about the above is that we want the average CPU utilization of our Pods to be 60%. That’s 60% of our maximum, which is 1 core or 1000milliCpus.

You can verify all the pieces are there by running and verifying the different output from the below commands.

```csharp
kubectl get pods
kubectl get svc
kubectl get hpa
```

### How to simulate load and watch scale up events

Now to get some scaling to happen, we’re going to need to simulate traffic. Fortunately we can spawn another pod, let’s call this our “load-pod”, and let it perform a load test on our httpbin pods.

The testing tool I know the best is `locust` , so we’ll create this pod and put a very basic locustfile in it, and set it to run against our httpbin service.

Our test file, `locustfile.py` , looks like so:

```python
from locust import HttpUser, task


class HttpBindUser(HttpUser):
    @task
    def status_and_bytes(self):
        self.client.get("/status/200")
        self.client.get("/bytes/1000")
```

```bash
# Run all commands in the httpbin namespace
kubectl config set-context $(kubectl config current-context) --namespace=httpbin
# start the pod running
kubectl run load-pod --image python:3.8 -- sleep infinity 
kubectl cp locustfile.py load-pod:/locustfile.py
# install locust
kubectl exec -ti load-pod -- pip install locust
# start a test with 10 users
kubectl exec load-pod -ti locust --headless --users 10 \ 
  --spawn-rate 1 -H http://httpbin:80ba
```

Once this is running, open another terminal and run

`watch kubectl top pods`

And in another window run

`kubectl get hpa -w`

These will allow you to see the memory/cpu of the pods in the namespace, and the HPA, as it decides to scale up based on load. Once you see the HPA change its replicas column, like so:

```bash
NAME      REFERENCE            TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
httpbin   Deployment/httpbin   0%/60%    1         10        1          20m
httpbin   Deployment/httpbin   38%/60%   1         10        1          20m
httpbin   Deployment/httpbin   76%/60%   1         10        1          20m
httpbin   Deployment/httpbin   78%/60%   1         10        2          20m
httpbin   Deployment/httpbin   49%/60%   1         10        2          20m
httpbin   Deployment/httpbin   56%/60%   1         10        2          21m
```

You can view the event by running `kubectl describe hpa` and you’ll see an event like so

```
  Normal   SuccessfulRescale             33s (x2 over 10m)
      horizontal-pod-autoscaler  New size: 2; 
      reason: cpu resource utilization (percentage of request) above target
```

You’ll also notice more pods are running based on this scale up.

### Cleaning Up

Run `kubectl delete namespace httpbin` to clean up all the resources you’ve created.

### Summary

You can use HPAs to scale your pods based on resource utilization.

You measure resource utilization using a cluster service like metrics-server or Prometheus.

You then configure your HPA to scale based on a target metric threshold, like a CPU or memory percentage.

Finally you can load test your deployment to make sure that it scales as appropriate.

Thanks for reading!
