---
title: "What Does it Mean to Start an EC2 Instance?"
date: 2023-03-04
medium_url: "https://medium.com/@mckornfield/what-does-it-mean-to-start-an-ec2-instance-ee228165971f"
---

Or any VM in the cloud?

![Photo by Andy Hermawan on Unsplash](/img/what-does-it-mean-to-start-an-ec2-instance/0_WAyYyM9Kv4hcOFa6.jpg)

*Photo by [Andy Hermawan](https://unsplash.com/pt-br/@kolamdigital?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

In a program I volunteer for, someone asked what it means to “start an EC2 instance.” I thought I’d give explaining it a shot, given what I understand about AWS.

### Explain like I’m a 5 Year Old

Amazon is more than just a company that lets you buy things online. They have a lot of people that work together to run a huge number of computers, that are all connected to each other in a “cloud.” This huge number of people are part of Amazon Web Services, or AWS.

One of the main things that people at AWS let you do is basically rent a computer. This computer can be really small or really large, and the renting process is almost instant. Once you rent the computer, you can install whatever you want on it, and you pay for as long as you rent it and it’s on.

Renting a computer is like renting a car, but you can do it by the minute. You tell Amazon how big of a car you want, and they charge you for as long as you drive it around. Once you decide to shut off the computer, you “return” the car and don’t have to pay any more.

If you rent it and turn it off, you just pay to store whatever data that computer was using, unless you decide to delete that too.

Also if you want, you can pay to have that computer be able to talk to other computers, in case you want to run a website or something else like a gaming server.

### … Like I’m a 15 Year Old

The computer you’re reading this on, whether a mobile or desktop device, reaches out and talks to lots of other machines just like it. There are companies that run services where you can rent those machines to do any sort of work you’d like. Amazon’s tech arm, AWS, lets you rent servers through a service they call “Elastic Compute Cloud”, or EC2.

They let you rent servers with more RAM or CPU, in case you need to run a more resource intensive service, or they offer machines so small they act a free tier, if you just want to run a very simple program on their service.

Hitting the “launch instance” button on AWS, or using some other means, like other programs or the terminal, sets up your rental of one virtual computer. A virtual computer is basically a computer that thinks it’s a real computer, but is actually installed on another, usually larger computer, but sandboxed from the rest of the machine.

You can use more complicated processes to launch and manage multiple machines at once, in case you’re running a complicated set of workloads. Many companies do this instead of simply hitting the “launch instances” button. You can even tell AWS to scale up or down the number of instances you run if you need to (up to help with high traffic, down to save money), using something called Autoscaling Groups.

Some companies that run [their workloads on AWS include](https://www.linkedin.com/pulse/biggest-aws-users-nikhil-suryawanshi/):

- Netflix
- Twitch
- Facebook, Instagram and Whatsapp

EC2 Instances can be exposed to the internet or run in a “private cloud”, so that only other workloads or necessary things can access them.

### … Like I’m an IT professional

If you work with public cloud providers, chances are you’ll brush up against AWS. EC2 is the most basic way to run cloud based workloads, and can be the building block of other pieces, like self managed EKS clusters (Kubernetes), or ECS on dedicated EC2s (container based tasks).

Amazon has pretty good offerings as far as machine sizes and types, [offering different types of GPUs](https://aws.amazon.com/nvidia/) you might need for AI/ Deep Learning tasks, or super high performance [bare metal machines](https://aws.amazon.com/about-aws/whats-new/2022/04/amazon-ec2-bare-metal-instances/).

The VMs that you bring up on EC2 are managed by AWS’s system, but they are usually just a section of a blade server running a [hypervisor](https://aws.amazon.com/what-is/hypervisor/#:~:text=AWS%20Nitro%20System%20is%20a,to%20specific%20hardware%20and%20software.) and many other EC2 instances on the same machine. The cloud management system is responsible for allocating and assigning instances to users, as well as setting up any networking or disk (EBS) required to run the machine.

Launching EC2 Instances can be done with public IPs so that they’re accessible to the internet, or they can be put in private subnets, and accessed using various other means, like a [bastion host](https://towardsdatascience.com/connecting-to-an-ec2-instance-in-a-private-subnet-on-aws-38a3b86f58fb) or AWS services like SSM.

The networking security model is one of the more complicated but important pieces when it comes to running your EC2 instances securely. Understanding VPCs and subnets is just as important as understanding EC2 when working with AWS.

AWS as an organization tends to promote their serverless offerings (S3, Lambda, DynamoDB) over their “customer-managed” offerings like EC2, usually because it comes with less operational overhead. Many folks prefer EC2 because it’s easier to understand what’s going on, and because you have more control of the server, at a cost (you pay even if you’re not using it, whereas serverless is pay by usage).

---

Hopefully that helps paint a picture of what the “Launch Instance” button does. Thanks for reading!
