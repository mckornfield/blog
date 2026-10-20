---
title: "Helm Create Part 1: Templating"
date: 2022-12-28
medium_url: "https://medium.com/@mckornfield/helm-create-part-1-templating-9c4d9baa2e4e"
---

A guide to the output of running `helm create` with a focus on the metadata and templating.

![Photo by Glenn Carstens-Peters on Unsplash](/img/helm-create-part-1-templating/0_yyKBsgweA-bzvNOW.jpg)

*Photo by [Glenn Carstens-Peters](https://unsplash.com/@glenncarstenspeters?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Prerequisites

If you’re new to `helm` , it’s one of the main ways people package, template and install applications in [Kubernetes](/posts/what-is-kubernetes/).

The [install instructions](https://helm.sh/docs/intro/install/) page boils down to:

- On a Mac:`brew install helm`
- On a Windows w/ [chocolatey](https://community.chocolatey.org/packages/kubernetes-helm): `choco install kubernetes-helm`
- Some Linux flavors: `sudo apt-get install helm`

## Let’s make a chart!

A `chart` is the name of any package that helm can create, install, depend on, or release. Charts are the building blocks of the `helm` world.

`helm create my-first-chart` will make your first chart. We’ll go through the items made by this command one by one. The ones without an hourglass we’ll go over in [Part 2](/posts/helm-create-part-2-resources/).

```ruby
$ tree -a .
├── .helmignore ⏳
├── Chart.yaml ⏳
├── charts ⏳
├── templates
│   ├── NOTES.txt ⏳
│   ├── _helpers.tpl ⏳
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml ⏳

3 directories, 11 files
```

### .helmignore

Not much different than a .gitignore, this will stop files from getting put into the tar file when you run `helm package` .

### Chart.yaml

This contains all the metadata about your chart. Most of the files in a helm chart will be in YAML format, e.g.

```markdown
key: value
aList:
  - 1
  - 2
  - 3
```

The keys in the Chart file are well commented, so I won’t add much here. When you use things like `helm repo search` and look for your chart, the name, description and version from this YAML file will power that search view.

If you want to add [dependencies](https://helm.sh/docs/helm/helm_dependency/) to your chart (e.g. add redis or an RDBMS chart), you would add a dependency block like so

```yaml
dependencies:
- name: nginx-ingress
  version: "0.15.2"
  repository: "https://helm.nginx.com/stable/"
```

And then with `helm dependency update` you’d have the other chart pulled down… but that’s probably a future lesson. Let’s go back to the starter chart.

### Charts/ Folder

This empty folder will hold any dependencies you create within the Charts.yaml file. They’ll get pulled down by running the command mentioned above. But your brand new chart doesn’t have any dependencies, so we can ignore it.

### NOTES.txt

If this is your first time looking at helm charts, you’re probably wondering “what the heck is up with all the `{{ .Values.stuff }}` . Well I mentioned the word *template* earlier, and that is a big part of what `helm` gives you.

In the Kubernetes world, everything is YAML (or JSON) files that represent resources. If you want to introduce options to change from a default set of files (instead of using something like the [Kubernetes client](/posts/getting-started-with-the-kubernetes-python-client/)), you can:

- Template using something like `helm`
- Patch files using something like `kustomize`
- Do a simple find and replace with any tool of your choice (`sed`?), then doing `kubectl apply`

But helm goes the path of templating, and their docs on it are [pretty good](https://helm.sh/docs/chart_template_guide/getting_started/). Basically things inside `{{}}` get substituted with variable values or fancy expressions.

All this NOTES.txt file does is print out after your chart is installed. Plain and simple. It will use this nice templating to fill out some sample commands so that a user could look at the `Service` you’re running using `kubectl` commands.

### \_helpers.tpl

This might be the most WTF file. Essentially it defines all the chart level “variables” that are reused throughout the different YAML files. Variables defined in here are referenced with the `include` syntax, e.g. `include “my-first-chart.fullname” .` . The dot is important! Something from [Go templating](https://stackoverflow.com/a/62476328/10061484), which is what a lot of the `helm` templating is based around.

Anyway, this file can be hard to look at but it is important, since it creates a set of variables that are reused across all the chart. 43 pairs of double curlies at the time of this writing!

You’ll notice most of these labels are truncated to 63 characters. That pattern is due to the DNS resolution within kubernetes, and the limit of each part of a hostname being limited to [63 chars](https://www.rfc-editor.org/rfc/rfc1123#section-2).

These go templating blocks define the following:

- `my-first-chart.name` — The name of the chart, used in the NOTES text and also in the selector labels, which we’ll get to in part 2.
- `my-first-chart.fullname` — The full name of the chart, which is used to name most of the resources that we’ll go over in part 2.
- `my-first-chart.chart` — The name of the chart, only used in the selector labels
- `my-first-chart.labels` — Labels used for every resource in the application. Can be good if you’re trying to describe/ get those resources by labels instead of names.
- `my-first-chart.selectorLabels`— These labels are just for matching the deployment to the service. I’ll explain this better in part 2 as well.
- `my-first-chart.serviceAccountName` — The name of the service account resource. This one is specifically templated because people tend to override service account names to reuse existing ones, created outside of the `helm install`.

### values.yaml

This file is well self documented with comments. The thing to draw attention to with this values file is that it is the default set of values that will be passed into the chart. You can install a chart with `-f my-values.yaml` to provide overrides, or other options like `--set`.

Certain pieces are commented out in here for reference, like the `resources` , but you’ll probably want [at least set the memory](https://home.robusta.dev/blog/kubernetes-memory-limit). If you want to change the name of the resources/ the chart, you’ll see `nameOverride` and `fullnameOverride` in here, which let you tweak the properties `name` and `fullname` we went over from `_helpers.tpl`

That’s all for now!

In Part 2 we’ll go over all the resources at a high level and the test file. [Click here to read on.](/posts/helm-create-part-2-resources/)
