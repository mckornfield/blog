---
title: "Helm Create Part 2: Resources"
date: 2023-01-01
medium_url: "https://medium.com/@mckornfield/helm-create-part-2-resources-4e73f650fbd0"
---

A guide to the output of running `helm create` , with a focus on the resources and tests it creates.

![The resources we’ll discuss in this article](/img/helm-create-part-2-resources/1_l9RQSEl4thL6YUzbq59Bsg.png.png)

*The resources we’ll discuss in this article*

Go to [Part 1](https://medium.com/p/9c4d9baa2e4e/edit) here if you want to learn more about the templating.

Recap: We created a chart using `helm create my-first-chart` and we’re walking through the files. We’ve gone through the Chart.yaml

```perl
$ tree -a my-first-chart/
├── .helmignore ✅
├── Chart.yaml ✅
├── charts ✅
├── templates
│   ├── NOTES.txt ✅
│   ├── _helpers.tpl ✅
│   ├── deployment.yaml ⏳
│   ├── hpa.yaml ⏳
│   ├── ingress.yaml ⏳
│   ├── service.yaml ⏳
│   ├── serviceaccount.yaml ⏳
│   └── tests
│       └── test-connection.yaml ⏳
└── values.yaml ✅

3 directories, 11 files
```

### Common labels

Almost all the following files will have these same

- `{{ include “my-first-chart.fullname” . }}` -> This will end up being “my-first-chart” if we don’t do any name overrides, and become the name of the deployment. Some folks add a suffix to this, like `-nginx` or whatever the resource represents.
- `{{- include “my-first-chart.labels” . | nindent 4 }}` -> These labels are often how you can query for parts of a chart, using something like `kubectl get pods -l app.kubernetes.io/name=my-first-chart`

### deployment.yaml

Now we’re into the “real Kubernetes” files. If you don’t know what a deployment is, the [k8s docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) are the best thing to read. My short answer is it’s creates and controls or more containers (Pods) that you want to run in the cluster. It does this through a `Replicaset` . The key to a deployment is that it creates an expectation for how many of these containers will run, what volumes, service accounts, and secrets they’ll use, and how they are upgraded.

Let’s go through the templating pieces that aren’t part of “common”.

- `{{- if not .Values.autoscaling.enabled }}` — This and the `replicaCount` are relevant to the `hpa.yaml` , which I’ll get to in a sec. The thing to know here is that if we don’t have autoscaling enabled we run the number of replicas (i.e. how many sets of the Pods) to run. Otherwise the `hpa` will control this.
- `{{- include “my-first-chart.selectorLabels” . | nindent 6 }}` — [Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors) are how you can designate can match a `Service` to your deployment. The `nindent` makes sure that you don’t get any errors when templating the yaml files. You can see how it looks by running `helm template .`if you’re inside the folder.
- `{{- with .Values.podAnnotations }}` — This will put annotations on the pod that might be useful if you want to pass information to the running application in the form of annotations. This `with` construct is a way to only add the key and values if something is provided
- `{{- with .Values.imagePullSecrets }}` — If you need to pull from a private registry, this is where you’d specify a reference to a k8s `Secret` that has the [credentials](https://kubernetes.io/docs/concepts/containers/images/#referring-to-an-imagepullsecrets-on-a-pod) you’d need
- `{{ include “my-first-chart.serviceAccountName” . }}` — This is how you use the service account created by this chart (or simply referenced if you set `.Values.serviceAccount.create` to false)
- `{{- toYaml .Values.securityContext | nindent 12 }}` and `{{- toYaml .Values.podSecurityContext | nindent 8 }}`— This determines what user runs the container, and any file system permissions. You can set it for all pods (PodSecurityContext) or for individual ones (securityContext), though in this starter chart they are equivalent
- `{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}` — A pretty fancy way to specify what image is pulled, using the app version if the tag isn’t specified
- `{{- with .Values.nodeSelector }}` `{{- with .Values.affinity }}` and `{{- with .Values.tolerations }}` — Various ways to specify what node a pod ends up on. `nodeSelectors` are ways to match labels for a node, `affinity` describes a node that would be preferred, a more controlled way to prefer a node than a selector, `tolerations` mean that the pod can handle a `taint` placed on the node.
- `{{- toYaml .Values.resources | nindent 12 }}` — The CPU and memory requirements of the pod. There are [sensible ways to set these](https://home.robusta.dev/blog/kubernetes-memory-limit), but tl;dr set the max and requested mem to the same, don’t request CPU.

A few I skipped over (the names, the service port, and pull policy) are basically what they say they are.

Phew, take a breath. That was the worst one (well the Ingress one is a bit tricky as well, but this had the most templating going on). Let’s move on to the…

### hpa.yaml

Horizontal Pod Autoscaler. This is a way to make it so that pods counts scale up and down based on resource usage. It is basically something that controls the `Deployment` and the corresponding `Replicaset` that the `Deployment` generates. You’ll see

- `{{- if .Values.autoscaling.targetCPUUtilizationPercentage }}`
- `{{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}`

These blocks add in a target that if exceeded, the HPA will trigger a scale up, assuming you’re not at `.Values.autoscaling.maxReplicas` . But other than that, this file is pretty simple. Note that this scale up and scale downs are not instant; there’s always a bit of a delay. Also the [algorithm is a bit funky](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-details), so be aware that the HPA might not always satisfy your needs.

The `minReplicas` and `maxReplicas` represent the range that the HPA will stay in. Exceeding the percentage for a short amount of time will scale up, while 300 seconds of being overutilized will trigger a scaleDown (though this can be [configured](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior)).

### ingress.yaml

This is our other difficult file to get through, so strap in. By default it’s not enabled, so you could ignore it if you don’t want to communicate with your `service.yaml` , but for most web application usecases you’ll need some sort of Ingress. You might want to jump to the `service.yaml` file before reading through the rest of this, to see what the ingress is targeting.

I wrote about Ingresses [in another article](/posts/ingress-talking-to-kubernetes-services-from-outside-the-clus/) if you want more details.

OK, there are lots of interesting conditionals in the form of:

```bash
semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion
```

These are because there were lots of backwards incompatible changes related to ingress classes. I’ll just pretend that we’re on `1.19+` and update the file without conditionals.

The file on 1.19+ would look something like the below. I’ll put comments inline on what I think bears explaining.

```yaml
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "my-first-chart.fullname" . -}} # Set variables
{{- $svcPort := .Values.service.port -}} # To reduce copy paste
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "my-first-chart.labels" . | nindent 4 }} # Indent 4 times
  {{- with .Values.ingress.annotations }}
  annotations: # Annotations that can alter properties of the Ingress
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  # Used to map to the Ingress Controller, described in my other article
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }} # HTTPS/TLS secured routes
  tls:
    # Range means this part operates as a loop over list elements
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }} # Puts things in quotes... pretty clear haha
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }} # Non TLS based domains/paths
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if .pathType }} # This is pretty fancy, 
                                # but if .pathType is a property of the data 
                                # we're looping over
            pathType: {{ .pathType }} # 
            {{- end }}
            backend:
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
          {{- end }}
    {{- end }}
{{- end }}
```

The example provided, if enabled, creates an ingress at the domain and path `chart-example.local/` that will map to the service, which we’ll get to right now.

### service.yaml

A service. What a generic name. This is the layer overlaying the pods created by the `Deployment.` that allows other services within Kubernetes or the Ingress to communicate with the application. It has 3 essential parts

- `{{ .Values.service.type }}` — There are [four of types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types), but for this example `ClusterIP` is what we’ll use, meaning it will only be used internally.
- `{{ .Values.service.port }}` — The port that other `Services` or an `Ingress` can communicate to this `Service` on, also in this case it’s mapped to the same port as the ones that the `Deployment` exposes
- `{{- include “my-first-chart.selectorLabels” . | nindent 4 }}` — This section under `selector` is the critical piece that binds the `Service` to the `Pods` running from the previously discussed `Deployment`

### serviceaccount.yaml

This file is the most vanilla. The `ServiceAccount` by default doesn’t do very much, but it’s a best practice not to use the default. If you want to give your application more behaviors, generally you have to add in some [Role Based Access Control (RBAC) to the ServiceAccount](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).

For using the service account with cloud providers is the `.Values.serviceAccount.annotation` comes in handy. It can let you use [IAM Roles for Service Accounts in AWS](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) or [Workload Identity for GCP](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).

### tests/

Any files in this folder will be installed but only deployed when using `helm test` . These come across as helm hooks, you can read more about helm test [here](https://helm.sh/docs/topics/chart_tests/).

### test-connection.yaml

This is a bizzare resource. It’s of type `Pod` , but if you run `helm test` after installing the chart, you’ll find that a `Job` gets created and spawns this Pod. The annotation `“helm.sh/hook”: test` is what allows helm to understand how to control the lifecycle of this `Pod`.

As it is, it will run a `wget chartname:servicePort` , which will fire off fine if the `service` and `pods` are running. Adding other helm tests into this folder will run them in serial, though you can pick them by name with `helm test --filter`

That’s all folks! Thanks for reading. Hopefully `helm create` is a little clearer to you.
