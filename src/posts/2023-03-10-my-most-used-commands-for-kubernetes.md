---
title: "My Most Used Commands for Kubernetes"
date: 2023-03-10
medium_url: "https://medium.com/@mckornfield/my-most-used-commands-for-kubernetes-97f7baeea59e"
---

And how you can find yours

![Photo by Andras Vas on Unsplash](/img/my-most-used-commands-for-kubernetes/0_Gqv0VmRHZDn-41bC.jpg)

*Photo by [Andras Vas](https://unsplash.com/@wasdrew?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Thought it might be a silly exercise to see which commands I’ve run the most, maybe they’ll be helpful for your Kubernetes journey.

Let’s take a look!

### How Do You Query for Them?

The `history` command will spit out your old commands but it also includes nubers to refer back to the command. I was able to instead grep my `~/.bash_history` file for certain commands, and then cut the output so that I could see what commands I issued the most by the relevant pieces.

### The Results

Just the first field, i.e. which command do I use most, `kubectl` or its alias, `k` (which I highly recommend to save yourself some typing)

```bash
cat ~/.bash_history | grep -v '#' | grep -E '(^k |^kubectl)' \
    | cut -d" " -f1 | sort | uniq -c | sort
 177 kubectl
3052 k
```

Clearly `k` wins.

Now for the second field

```bash
cat ~/.bash_history | grep -v '#' | grep -E '(^k |^kubectl)' \
    | cut -d" " -f1-2 | sort | uniq -c | sort
  32 k run
  36 k top
  66 k port-forward
  74 k config
  80 kubectl get <--- same as `k get`
 106 k exec
 124 k delete
 289 k describe
 339 k logs
1902 k get
```

Clearly I run a lot of `get` and `logs` .

Third field wasn’t all that interesting, but with four fields, I saw one of my favorites.

```vbnet
  32 kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name,STATUS:.status.phase
  33 k get nodes -L
  41 k get svc
  82 k get ns
 129 k get nodes
1145 k get pods
```

Notice there’s some abbreviated gets, like `svc` and `ns` . It’s good to know the [shortnames](https://akhilsharma.work/kubectl-get-resource-short-names/) to save some key strokes.

Used 32 times, the get pod command will print out a nice format of the states and what nodes they are on. An example when run on minikube:

```sql
kubectl get pod \
    -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name,STATUS:.status.phase
NODE    NAME                            STATUS
local   busybox-579dbc5484-fp2ks        Running
local   busybox-test-job                Succeeded
```

Last set of commands of note, ones that weren’t just`get`

```bash
cat ~/.bash_history | grep -v '#' | grep -v "get" | grep -E '(^k |^kubectl)' \
    | sort | uniq -c | sort
10 k run test-perm -it --rm --image amazon/aws-cli:latest --command --overrides '{"spec":{"serviceAccountName":"my-job-controller"}}' -- bash
10 k port-forward mongodb-0 27017 &
11 k port-forward svc/agent 8080
12 k exec -ti job-metrics -- tail nohup.out
20 k exec -ti load-pod -- bash
27 k top pods
```

`kubectl top pods` is a great one for looking at memory and cpu usage, refreshed every 15 seconds. It requires having the [metrics server installed](https://github.com/kubernetes-sigs/metrics-server), but is pretty great, especially with something like `watch`

`watch -n 15 kubectl top pods` will run the command every 15 seconds in the window, so you don’t have to keep running it.

`kubectl port-forward` is a classic for accessing pods, but it can also be used to access services with `svc/service-name` . One super important thing to note is that this actually is a hack and [only port-forwards one pod](https://github.com/kubernetes/kubernetes/pull/103526), so it’s not appropriate for testing the service itself. But it can be useful for *debugging* the service.

Also sending the port-forward to the background with `&` can be useful if you want to pass traffic in the same terminal, and then kill the port-forward with `kill %1` , assuming it’s the only background process you have. You can list background processes with `jobs` .

For existing pods, `kubectl exec -ti pod-name -- bash` is a classic way to hitch a ride, or tailing a specific file with `-- tail filename` to see if something’s writing to it can be pretty useful.

This longer run command is a fun one for testing the permissions of a service account, i.e.

```bash
k run test-perm -it --rm --image amazon/aws-cli:latest \
  --command \
  --overrides '{"spec":{"serviceAccountName":"my-job-controller"}}' -- bash
```

This lets you bind the `my-job-controller` service account to a test image that you can run and debug in. Especially useful for testing something like [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html). Once you exit the container, it’ll get deleted (that’s what the `--rm` is for), and the `--command` just makes sure that the entrypoint of the container is blank, so it doesn’t interfere with the `bash` command passed at the end.

Thanks for reading, hopefully you learned something!
