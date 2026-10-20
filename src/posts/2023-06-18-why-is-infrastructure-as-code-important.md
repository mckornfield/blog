---
title: "Why Is Infrastructure As Code Important?"
subtitle: "A short history lesson, with some examples of Infrastructure as Code (IaC)"
date: 2023-06-18
medium_url: "https://medium.com/@mckornfield/why-is-infrastructure-as-code-important-6d726f18e1d5"
---

A short history lesson, with some examples of Infrastructure as Code (IaC)

![Photo by Stuart Frisby on Unsplash](/img/why-is-infrastructure-as-code-important/0_a4jezS_CgoyRkZp8.jpg)

*Photo by [Stuart Frisby](https://unsplash.com/@mrfrisby?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### System Administrators, IaC pre-history

Historically, installing and managing software systems on machines was a manual process, relegated to IT professionals deemed “System Administrators.” These folks would receive tickets to update software, or install software on machines, and then use whatever tools/scripts they had devised to perform the updates.

Sometimes these were widely shared scripts within an organization, other times they were hoarded by individuals.

### Cloud Computing and the Need for IaC

With the advent of cloud computing, there were efforts on the part of cloud providers as well as their customers, to automate as many things as possible. It came almost out of necessity, as the amount of work required to maintain complex cloud-based systems magnified the amount of work traditionally put on the System Administrators’ plates.

Instead of using code to solve business needs, code was employed to solve software infrastructure needs (which, for companies like AWS, were the *new* business needs). The solution to this complexity problem was Infrastructure as Code (IaC). It’s the answer to the question: “how do I use code to define the state and changes to the state of my infrastructure?” It’s characterized by being:

- Repeatable (in the form of simply rerunning simple commands to apply changes represented in code)
- Version Controlled (Infrastructure as Code changes are merged into one or more repositories)
- Centralized (all infrastructures changes are mediated through ONE way to change them, be it Terraform, Ansible or a cloud specific style like CloudFormation)

### Imperative vs. Declarative IaC [1]

*Declarative*: Declare the state of the system, as you would want it to be. Declarative Infrastructure as Code is like describing the type of cake you’d want to someone who’s making it, down to where the icing will go. If you need to change the cake, you’d tweak your old description to match the new kind of cake you’d want.

[Terraform](https://www.terraform.io/) is one of the best open source examples of declarative IaC. If you use Terraform, you’d state in a .tf file “I’d like one VM, of this size, running in this VPC.” By applying this desired state, you’d store the state information somewhere (usually in a cloud based bucket) and Terraforms calls the necessary APIs to start the VM, and install any software it needs. When you want to change something, like the size of the VM, you simply update the .tf file, and apply the change, which will tell you as part of the plan what changes it will make to the infrastructure.

*Imperative:* To contrast with the Declarative style, instead of *declaring* what state you want, in Imperative IaC you list the set of steps that will bring your infrastructure into your desired state. In contrast to describing the cake you want in minute detail, you describe the *steps* and *ingredients* to make the cake, listed in an exact order.

[Ansible](https://www.ansible.com/) is one of the best examples of an open source imperative Infrastructure as Code framework. You declare in yaml a set of **tasks**that you apply to a list of hosts defined in one or more **inventory** files. Ansible’s main power is that you can make it idempotent, so if you’ve already completed one of the steps, Ansible marks it as “OK” and simply moves on to the next step.

In my experience, calling cloud APIs to create resources is best done in a declarative style, with something like Terraform, whereas making updates to running infrastructure is best done with an imperative style, like Ansible.

### To Summarize

Infrastructure as Code is a replacement for the manual mechanism of making infrastructure changes with terminal commands or scripts. IaC is characterized by being repeatable, version controlled, and centralized compared with its manual predecessor. It can be written in a declarative or imperative style.

[1] <https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac>
