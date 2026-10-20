---
title: "Installing the Apache Solr Operator on DigitalOcean Managed Kubernetes"
date: 2023-05-18
medium_url: "https://medium.com/@mckornfield/installing-the-apache-solr-operator-on-digitalocean-managed-kubernetes-7129a65b50cb"
---

Using terraform!

![Photo by Eren Namlı on Unsplash](/img/installing-the-apache-solr-operator-on-digitalocean-managed/0_V7d_bk8RD_x0ZqFy.jpg)

*Photo by [Eren Namlı](https://unsplash.com/@ereneskiz?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I recently went through some gotchas to install the Apache Solr Operator in DO, and wanted to share it with ya’ll in case you hit the same. My in progress [PR is here](https://github.com/Greenstand/treetracker-infrastructure/pull/165/files).

### Gotcha #1: Authenticating with the DigitalOcean Terraform Provider

In our provider.tf file, if you simply declare

```bash
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.28.1"
    }
  }
}
```

You’ll see a prompt for entering your API key when you go to run any terraform commands. We’d used tfvars files before, so that with the below block we could pass in the [necessary token to the provider](https://github.com/Greenstand/treetracker-infrastructure/blob/27228c7e0cd0b42c0f95218a3e5c949d260857a2/bastion/provider.tf#LL12C1-L15C2):

```csharp
provider "digitalocean" {
  token = var.do_token
}
```

But in recently we’ve been able to simply use `DIGITALOCEAN_TOKEN` as an environment variable, which simplifies the terraform setup, and just requires running a script to load the appropriate token. A snippet might look like the following, assuming you place your DigitalOcean tokens in a `~/.netrc` file.

```bash
# export_do_tf_tokens.sh
my_env=${1:?Environment is required}
line=$(grep "digitalocean.${my_env}.org" ~/.netrc)
export DIGITALOCEAN_TOKEN=$(echo $line | awk '{print $6}')
```

and then `source export_do_tf_tokens.sh` before running any terraform.

### Gotcha #2: The weirdness of the spaces “s3 bucket” for tf state.

I still think this is weird, but the bucket we’re using to hold the terraform state looks like this:

```graphql
terraform {
  # DigitalOcean uses the S3 spec.
  backend "s3" {
    bucket   = "my-do-state-bucket"
    key      = "my-state-file.tfstate"
    endpoint = "https://sfo2.digitaloceanspaces.com"
    region = "eu-west-1"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
  }
}
```

Weird things to call out:

- The region, even though we’re using sfo2, we still use eu-west-1 as the region name
- Skipping some checks that will just fail when calling the spaces API
- The key setup, which, just like the provider setup, requires exporting `AWS...` keys to do the bucket authentication.

A snippet for exporting the spaces keys might look like:

```bash
netrc_string=$(grep "sfo2.${my_env}.digitaloceanspaces.com" ~/.netrc)
export AWS_ACCESS_KEY_ID=$(echo $netrc_string | awk '{print $4}')
export AWS_SECRET_ACCESS_KEY=$(echo $netrc_string | awk '{print $6}')
```

Where a line in your .netrc might be

`machine sfo2.dev.digitaloceanspaces.com username KEY password SECRET`

And `KEY` and `SECRET` are values you get from downloading an appropriately scoped DO spaces key.

Once that’s all set up, you can store your tfstate in the Spaces bucket. Yay!

### Finally installing the Helm Chart!

With all that setup, we can now run this little snippet to install the latest release of the `solr-operator` in our cluster.

```kotlin
data "digitalocean_kubernetes_cluster" "dev" {
  name = var.cluster_name
}

provider "helm" {
  kubernetes {
    host  = data.digitalocean_kubernetes_cluster.dev.endpoint
    token = data.digitalocean_kubernetes_cluster.dev.kube_config[0].token
    cluster_ca_certificate = base64decode(
      data.digitalocean_kubernetes_cluster.dev.kube_config[0].cluster_ca_certificate
    )
  }
}

resource "helm_release" "solr" {
  name             = "solr-operator"
  repository       = "https://solr.apache.org/charts"
  chart            = "solr-operator"
  version          = "0.7.0"
  namespace        = "solr"
  create_namespace = true


  values = [
    "${file("${path.module}/values.yaml")}"
  ]

}
```

The `helm` provider block reads information from the data block, which uses our API key to get kubeconfig information about the cluster, letting us connect and install the `solr-operator` assuming we are running with a token that has the right permissions.

The helm release is pretty vanilla, creating a namespace if one doesn’t exist, and using a `values.yaml` file for any overrides (though for now I just left it blank).

When I ran `terraform apply` I ran into my final gotcha —

### Gotcha #3: Resources not owned by the Chart

It turns out something else had installed solr at some point, so there were ClusterRoles/ClusterRoleBindings not bound to the namespace. I had a couple options here but decided to just remove the offending ones, and rerun the install. I also saw the installation crash looping since one CRD didn’t get installed. Since this was a one time deal, I decided to just have a one-off script next to the terraform to handle these two sets of issues:

```cpp
kubectl delete clusterrole solr-operator-role solr-operator-zookeeper-operator
kubectl delete clusterrolebinding solr-operator-rolebinding solr-operator-zookeeper-operator
kubectl create -f \
  https://solr.apache.org/operator/downloads/crds/v0.7.0/all-with-dependencies.yaml
```

Once that was done, the installation went through just fine.

### Summary

DigitalOcean’s terraform modules have a few gotchas that it’s worth understanding if you’re trying to manage DO resources with terraform. Also Helm Charts can have awkward dependencies on resources that other charts might have created, sometimes the simplest option is just to delete them and let the chart create them again.

Thanks for reading!
