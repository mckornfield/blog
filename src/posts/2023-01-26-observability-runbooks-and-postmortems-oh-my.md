---
title: "Observability, Runbooks, and Postmortems (oh my!)"
subtitle: "Bad things are going to happen, might as well be prepared"
date: 2023-01-26
medium_url: "https://medium.com/@mckornfield/dealing-with-failure-observability-runbooks-and-postmortems-80ff3544365c"
---

Bad things are going to happen, might as well be prepared

![Photo by Agence Olloweb on Unsplash](/img/observability-runbooks-and-postmortems-oh-my/0_RWGGZyfF6B-oZsGv.jpg)

*Photo by [Agence Olloweb](https://unsplash.com/@olloweb?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Things Fall Apart

Part of running software systems is dealing with and mitigating failures. A piece of software that runs completely fine, without any changes, will still encounter failures if it operates in the wild, i.e. some other server admin installs it not quite right, or there’s a hiccup with one of the cloud services you use.But most of the failures you’ll experience are a result of some sort of change in SOME part of the system system, whether in one that you own or write, or one that you use.

But people who use your software don’t care WHY it doesn’t work, they only care how quickly you can get it working again. They want you to live up to [the availability targets that you promise](https://medium.com/@mckornfield/explain-like-im-5-sre-c3aa483e8dae).

Assuming things are going to go wrong, what are some of the tools you can use to try and stay within your error budget? Lets start with:

### Observability

The [first step in alcoholic’s anonymous](https://www.aa.org/the-twelve-steps) is admitting that you are powerless over alcohol. How is that relevant to observability? Well, the first step in observability is admitting that you won’t always know why a system isn’t working.

You have two goals with observability, which are more of a sisyphean task than a set of achievable goals:

1. Learn that a system isn’t “performing” **as early as possible** (hopefully without a user telling you)
2. Be able to figure out **why** the system isn’t “performing”

Performing is in quotes because it could mean a lot. It could mean that the system is just broken (i.e. every request is a failure) or that the system is “misbehaving” (e.g. slow requests, invalid responses).

Knowing when a system is misbehaving more importantly means knowing what it means for a system to *behave*. [This is where the SRE concepts of SLIs and SLOs are most relevant](https://sre.google/sre-book/service-level-objectives/).

SLIs are your indicators. They tell you your:

- Error rates
- Saturation levels
- Traffic
- Latency

In isolation, an SLI is just a number. What you want on top of that SLI is some sort of watermark, some line in the sand that says “this much latency is too slow.” Those are your SLOs, your *objectives.*

An example objective might be

- 99% of requests are successful (1% error rate)
- CPU utilization stays under 99%.
- 100 requests per second for one Pod
- 95% of requests take under 1 second.

When these things are violated, either something manual should have to occur (an engineer is notified) or maybe something automatic (scale up more instances.) Either way, these objectives define what “performing” means for your system.

Once you have SLIs/metrics, you can start to set and tune your SLOs.

If you set them too conservatively, you’ll never be alerted when things misbehave; Set them too aggressively, and your alerts or scale ups will constantly be firing.

There are many options for observability, which will take too long to go into here, but at the bare minimum using whatever your cloud provider offers is the best place to start.

Now what do you do once something goes wrong? Well maybe it’s time to crack out your…

### **Runbooks**

A runbook is simply a manual or auto-manual way to deal with some sort of issue. Sometimes they’re issues like “how do I deploy a new version?” which aren’t necessarily related to an incident, but oftentimes a runbook answers a question related to some sort of error signal you get from your observability (which we’ll get into shortly).

Let’s say that you receive an alert saying that Pods are failing to schedule. You dig into the alert a bit more and find out that a specific node is the culprit.

What do you do when there’s a node on the fritz? You consult the “*Bad Node Runbook*” written on your company’s internal wiki. It reads like:

1. Increase the Autoscaling group for the node to bring another node online (if only one node is in the group)
2. Once the new node is available, drain the old node `kubectl drain $nodeName`
3. Ensure all Pods are now going onto the new node, and are successfully scheduled
4. From the CLI or the Console, terminate the old Node
5. Lower back the autoscaling group if necessary

Runbooks can be a set of commands to run, a set of steps, or a mix. You can even use something like a [Jupyter notebook](https://docs.gitlab.com/ee/user/project/clusters/runbooks/) to make it so that you just have to run the appropriate cells that help deal with the issue.

Runbooks are a powerful tool to deal with recurring issues in a way that a brand new hire could hop on and deal with, or a recent transfer, or someone who just forgot how to deal with bad nodes.

They’re a great response to any incidents that you might have had in the past, or a good resource if you have to do something manually and there’s not much utility in fully automating a solution. Documentation is much cheaper than code you have to maintain, and oftentimes the right choice for transient but tricky errors.

Where do runbooks come from most of the time? A good source of them is…

### Postmortems

When a person dies, there’s generally some investigation into the cause of death. Sometimes it involves running more invasive tests on the corpse, but it’s an exercise in revealing WHY someone died. It can matter a lot if there are legal consequences, like if the person was murdered —

🎶[YEAHHHhhhhhhhhh](https://youtu.be/zNWjcTPVUoM?t=15)🎶💥💥💥🚗

OK couldn’t avoid a CSI Miami joke when talking about Postmortems, even if it didn’t really make any sense…

Anyhow, postmortems for *software* (instead of people) center around capital-i *Incidents*. When something goes wrong that negatively affects the system, and involves lots of members from different teams for extended periods of time, usually a postmortem is called for.

The goal for most postmortems is to be a [blameless assessment of what could have been improved/ avoided about the incident](https://sre.google/sre-book/postmortem-culture/#:~:text=A%20postmortem%20is%20a%20written,prevent%20the%20incident%20from%20recurring.). It’s not trying to find out who was the murderer (*git blame says it was Jeremy!)* but rather how the system could have been put into such a state as to cause chaos for end users and support/engineers within the company. Generally you care about

- What went well (Yay us!)
- What went wrong (Root cause)
- Where we got lucky (Phew!)

And most importantly

- What could be improved -> Durable Preventative Actions

Durable Preventative Actions, or DPAs, are really the most useful action items to come out of a postmortem (assuming they actually are acted upon). They can include things like

- improving observability (we needed more logs or traces at this part of the system, an alert should have fired here but never did),
- adding/improving runbooks (if this alert goes off, then go through this runbook)
- improving the architecture of the application in question

Postmortems are also a fun time to crystallize some really rough times that your support group might have gone through. They can be fun stories to tell the new folks so they don’t feel so bad about the incidents they have to deal with.

### In Summary:

Bad things are going to happen, you use Observability to know about it, Runbooks to deal with it, and Post-mortems to try and ensure we…

🎶[Won’t Get Fooled Again](https://www.youtube.com/watch?v=UDfAdHBtK_Q)🎶🎸

Thanks for reading!
