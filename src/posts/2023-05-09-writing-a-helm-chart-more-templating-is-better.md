---
title: "Writing a Helm Chart: More Templating is Better"
subtitle: "All the Things vs. YAGNI"
date: 2023-05-09
medium_url: "https://medium.com/@mckornfield/writing-a-helm-chart-more-templating-is-better-9502795a533f"
---

All the Things vs. YAGNI

![Photo by Gavin Allanwood on Unsplash (Your helm chart here!)](/img/writing-a-helm-chart-more-templating-is-better/0_ot4Jh1FNdYPdMt6R.jpg)

*Photo by [Gavin Allanwood](https://unsplash.com/@gavla?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (Your helm chart here!)*

### It’s just YAML, man

Helm charts, or kustomize templates, or whatever jsonnet/ksonnet is. They’re all just YAML or JSON after the many hoops you jump through.

You convert something like this

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: {{ template "fullname" . }}
    chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
    release: {{ .Release.Name | quote }}
    heritage: {{ .Release.Service | quote }}
    version: {{ .Chart.Version }}
  name: helloworld
```

into this

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: release-name-helloworld
    chart: "helloworld-1.0.0"
    release: "release-name"
    heritage: "Helm"
    version: 1.0.0
  name: helloworld
```

And a lot of times, all this templating isn’t *strictly* necessary. But in my experience it’s better to have more things templated with sensible defaults, vs. more things hard coded.

In the software world, and especially the Infrastructure as Code world, limiting options means people will either work around your setup, fork it (which is not a great user experience), or not use it at all.

### Template it all, but don’t make people *specify it all*

If you’re providing a chart for others to use, then introducing a lot of templating is probably the way to go. You want to give people *more* options, not fewer.

The key to templating everything is providing sensible defaults. You can do that by including a `values.yaml` file along with your chart, so that if a user doesn’t provide a value, you can still have the value be templated and just default.

Some great things to default are:

- Image references (especially if your chart version is tied to an Application version)
- Resources
- Names of certain generated but replaceable resources, like a ServiceAccount

You can default these values using the `values.yaml` as I mentioned, or one of those mysterious `_helpers.tpl` files ([I’ve written about them elsewhere](https://mckornfield.medium.com/helm-create-part-1-templating-9c4d9baa2e4e)).

Think they’ll never change the NodeSelector for your chart, or the Tolerations for it? Think again: people can have all sorts of crazy cluster setups and even your one simple chart will need all sorts of customizations to fit a square peg in a round hole.

### But what about YAGNI?

YAGNI, or You Ain’t Gonna Need It, is a prevailing maxim in the software world. It means you shouldn’t build something if you aren’t going to need it. And it makes a lot of sense, because building things always comes with a maintenance cost as well as a higher level of complexity.

The problem with something like a Helm chart is that knowing everything a user might need is an impossible task.

So what’s the antidote to adding all of this extra templating and possible confusion? (The YAGNI folks at least have that part right… just look at this [values file](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/values.yaml#L7).)

The best thing I’ve found is to pair your sensible defaults with decent inline comments that you can use to [autogenerate a README](https://github.com/bitnami-labs/readme-generator-for-helm). It’s always irksome to have to poke at a default values file (or a \_helpers.tpl file) to figure out what’s going on, and a decent README can help with that. You’ll especially want this if you have dependent charts in your chart.

Also having something to stop users from putting in crummy like simple Values validations or [JSON schema validations](https://austindewey.medium.com/helm-tricks-input-validation-with-values-schema-json-austin-dewey-b6b3417e3d34) helps keep the YAGNI people from tearing out all your double curly braces.

### A good chart is like a Subway sandwich…

A good helm chart has a lot of ways for you to change it (need to update the IngressClass, sure!) but doesn’t *force* you to specify a million things just to get it working.

It’s like building your own sandwich at Subway, you can ask for each individual thing, or just say “give me the main five vegetables with tuna.” Both people get the sandwich they want, but they don’t have to select each and every option unless they want to.

Too much templating? Hooey I say, template it all! (Who knows, *someone* might need it!)

Thanks for reading!
