---
title: "Load Testing but Easy? Use Locust!"
date: 2022-10-13
medium_url: "https://medium.com/@mckornfield/load-testing-but-easy-use-locust-1e270e0678bf"
---

Here’s what you need to know to use this great tool.

I recently encouraged an engineer on the team to use [locust](https://locust.io/) and remembered once again why it’s so great and thought I’d share.

### Getting Started

The [Locust docs](https://docs.locust.io/en/stable/quickstart.html#getting-started) themselves are great, so I won’t duplicate anything from there. As long as you have python and can do `pip3 install locust` , you’re off to the races. Maybe a rundown on the terminology could be useful though.

The concept of a “locust” is that it represents one of a swarm of users that are firing requests against the other system.

A simple `locustfile` looks like so:

```
from locust import HttpUser, between, task
```

```
class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
```

```
    @task
    def ready(self):
        self.client.get("/ready")
```

```
    @task
    def info(self):
        self.client.get("/info")
```

```
    @task
    def purchase(self):
        self.client.post("/purchase", {'money': 50.01})
```

`HttpUser` -> Represents the tasks that one user performs. Locust will spawn however many users you ask it to when running the test, though there are obviously limits as to what the host machine can handle.

`wait_time` -> how long one “user” waits in between executing one task to perform another, in seconds

`@task` -> used to define an action that is periodically performed in locust. Each “user” will randomly select a task, unless they are weighted.

`self.client` -> since we’re using an HttpUser, a basic http client supporting the methods you all know and love from something like `requests`

Once you run the file, just running `locust` in the directory will give you a nice little window that asks you the user count, the hatch rate (how many users to spawn per second) and the host.

You can also pre-fill these fields, for example, to run against localhost:8080 with 100 users at 5 spawning per second, you’d do

```
locust --users 100 -r 5 --host http://localhost:8080
```

And the UI will populate with fields prefilled. You can also run locust headless and you’ll just see a rolling show of the statistics.

Generally speaking, you’ll want to run the locust test on a different system than the one you’re testing against, but localhost is good just to try things out.

### The UI

One of the main reasons to use the UI is the graphs it can produce. Take a look at the below. What does it mean?

![A local run I did on one of our k8s services](/img/load-testing-but-easy-use-locust/1_zfpUj-9PnP3f9UjWZBXVvg.png.png)

*A local run I did on one of our k8s services*

What does the above mean? Let’s break it down

`RPS` Requests per second, basically the throughput of the application under the sustained load.

`Failures/s` The error rate, basically how many failures your users are experiencing per second.

`Median Response Time` The time in milliseconds for which 50% of requests fall under. That means that if you have a median response time of 5000 milliseconds, you know half of users are experiencing that’s AT MOST that slow. You also know that the other half of users are experiencing AT LEAST that slow. A good indicator of overall throughput of the system.

`95% percentile` Similar to the median but move the line upward, this is the time that 95% of requests fall under. This means 95% of users experience a time AT MOST this amount. This number being very high is an indication that a handful of users are experiencing really bad latencies.

How about a run that hoses the system? What might that look like? Take a look at the below, for a system that was under-resourced in Kubernetes.

![Look at that climb in errors, poor k8s pods](/img/load-testing-but-easy-use-locust/1_sqycdnmMHcqdJt3HLJFBpQ.png.png)

*Look at that climb in errors, poor k8s pods*

You can see the failure rate jumps super high, and the median response time plummets? Why is that?

### The signals

Locust gives you access to three of the four golden signals from the outside of the system. The golden signals from the Google SRE book are **Errors, Traffic, Latency and Saturation**. Since we don’t have much of an idea what the “saturation” is from the outside (i.e. queue limits, CPU limits etc.) we really can only see:

- Traffic (we know how many users we’re throwing at the system)
- Latency (we have the median and 95% response times in the graphs)
- Errors (we know if we get a 4xx or 5xx error back)

As the errors shoot up, our latency shoots down, *because we get really fast error responses.* That’s why you generally need to know about more than one signal at a time, otherwise you might think “well we have great responsiveness.” When what’s really happening is that we’re super fast at telling people that the website is down.

### The Stats

If you use the UI or headless mode, you’ll get stats that look like so, both continuously updated and finally stated once the test is ended.

![DATA](/img/load-testing-but-easy-use-locust/1_XdU5YvxeWrHVeU_XGjSlaQ.png.png)

*DATA*

What you get that’s more granular from here is a larger set of percentiles broken out, as well as getting them broken out by endpoint. Getting this more fine grained data might be TMI for most people, but can be useful if you’re trying to see which endpoint is causing the larger latency spike, and might be an indicator of an area of improvement.

### Summary

Locust makes load testing super easy. It gives you a useful set of signals to tell where errors or latency issues might be occurring, and just requires a simple python library install to get up and running.
