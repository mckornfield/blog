---
title: "Connecting to an EKS Cluster via Bastion Host, Over a SOCKS5 Proxy"
subtitle: "Gluing some bits together to run an EKS cluster’s control plane privately"
date: 2024-11-15
medium_url: "https://medium.com/@mckornfield/connecting-to-an-eks-cluster-via-bastion-host-over-a-socks5-proxy-43df4da20948"
---

Gluing some bits together to run an EKS cluster’s control plane privately

![Photo by Belinda Fewings on Unsplash](/img/connecting-to-an-eks-cluster-via-bastion-host-over-a-socks5/0_M-qgnN1YJdprt6z1.jpg)

*Photo by [Belinda Fewings](https://unsplash.com/@bel2000a?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Context please?

Sure. If you’ve ever tried to set up an EKS cluster with private control plane endpoints (i.e., a way to use `kubectl` against a not internet accessible control plane) but don’t have a VPN set up, you might have stumbled upon [this list](https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#private-access) or [this article](https://docs.aws.amazon.com/mwaa/latest/userguide/tutorials-private-network-bastion.html).

It suffices to say that the context for this is:

- A private control plane endpoint for a Kubernetes cluster means it has no public (internet addressable) IP
- To access a private IP, you need a mechanism to connect to over the open internet (assuming you’re not on some “connected network,” i.e., a VPN)
- One such mechanism is a host that you can connect to, i.e. a “bastion host”, which lets you proxy traffic to the private control plane through this host
- There are a couple options to connect to this host, but we’ll use the one that AWS supports outside of standard ssh, [SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html)

### Terraform please

So to deploy this bastion host, you’ll need a terraform snippet like the following

The most important pieces of this are:

1. The subnet and security groups are from a previously created VPC and Cluster.
2. The managed policy ARN that will let us use SSM to connect to the instance
3. `assume_role_policy` that lets the EC2 instance assume this role
4. An EKS AMI lookup… this isn’t entirely necessary (can just be an AL2 AMI if we just use the proxying), but if we want some utilities they’ll already be there.

```ruby
# Above this are two module declarations, one for the VPC and one
# for the security groups associated with the cluster
locals {
  subnet_id = module.network.vpc_private_subnets[0]
  vpc_security_group_ids = [module.cluster.cluster_node_security_group_id]
}
resource "aws_iam_role" "bastion-host-instance-role" {
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonSSMManagedEC2InstanceDefaultPolicy",
    "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
  ]

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ec2.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "bastion-host-instance-profile" {
  role = aws_iam_role.bastion-host-instance-role.name
  tags = {
    Name = "bastion-host-instance-profile"
  }
}

data "aws_ami" "amazon-linux-2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amazon-eks-node-1.30-v*"] # this can be updated per the k8s version
  }
}


resource "aws_instance" "bastion_host_ec2_instance" {
  ami                    = data.aws_ami.amazon-linux-2.id
  instance_type          = "t3.micro"
  subnet_id              = local.subnet_id
  vpc_security_group_ids = local.vpc_security_group_ids
  iam_instance_profile   = aws_iam_instance_profile.bastion-host-instance-profile.name

  root_block_device {
    encrypted = true
  }

  monitoring = true

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }
  tags = {
    # This name will be relevant down below
    Name = "bastion-host"
  }
}
```

Once this is applied and our instance is up, we can get to the connection step.

### Connecting via kubectl

Assuming you’ve connected to your cluster with a command like the following. The region, profile, cluster name and role-arn are place holders you’d update as appropriate. This also assumes you have the AWS CLI installed.

```bash
#!/bin/bash
 aws eks update-kubeconfig \
  --profile my-profile \
  --region us-east-1 \
  --name my-cluster \
  --role-arn arn:aws:iam::012345678910:role/eks-cluster-access
```

There are a decent set of ways to connect via ssm, but I like this [library](https://github.com/mludvig/aws-ssm-tools) that simplifies the CLI args, which you can install via pip

```bash
#!/bin/bash
pip3 install aws-ssm-tools
profile=my-profile
region=us-east-1
cluster_name=arn:aws:eks:us-east-1:012345678910:cluster/my-cluster
kubectl config set clusters."${cluster_name}.proxy-url" \
    socks5://localhost:1080
# Note that we can use `bastion-host` instead of the instance name, since this
# tool can look it up for us
ec2-ssh ec2-user@bastion-host -N -D 1080 \
  --profile "$profile" --region "$region"
```

Now you should be able to connect to your private control point cluster, and the traffic will be proxied through your bastion host.

All your `kubectl` commands should now just work.™️

If you kill the terminal window you can simply rerun the following:

```perl
profile=my-profile
region=us-east-1
ec2-ssh ec2-user@bastion-host -N -D 1080 --profile "$profile" --region "$region"
```

Also I don’t believe [1080](https://kubernetes.io/docs/tasks/extend-kubernetes/socks5-proxy-access-api/) is a sacred port but it’s the one used in [the example Kubernetes provides](https://kubernetes.io/docs/tasks/extend-kubernetes/socks5-proxy-access-api/).

### Also Don’t Forget to Proxy the Terraform!

If you need to proxy your terraform providers for kubernetes/and/or helm, just add the following

`proxy_url = "socks5://localhost:1080"`

An example below:

```java
provider "kubernetes" {
  host                   = module.cluster.cluster_endpoint
  cluster_ca_certificate = module.cluster.cluster_ca_certificate
  token                  = data.aws_eks_cluster_auth.output_cluster_auth.token
  proxy_url              = "socks5://localhost:1080"
}

provider "helm" {
  kubernetes {
    host                   = module.cluster.cluster_endpoint
    cluster_ca_certificate = module.cluster.cluster_ca_certificate
    token                  = data.aws_eks_cluster_auth.output_cluster_auth.token
    proxy_url              = "socks5://localhost:1080"
  }
}
```

Hopefully this helps you out if you’re trying to connect to a private control plane with a bastion host. Let me know if this helps or if you have questions!
