---
title: "Using Pod Identity in AKS with Terraform"
date: 2023-12-06
medium_url: "https://medium.com/@mckornfield/using-pod-identity-in-aks-with-terraform-bdede7ab1b0f"
---

Terraform-izing Microsoft’s tutorial

![Photo by Victor on Unsplash](/img/using-pod-identity-in-aks-with-terraform/0_2o1s4gtM4yQg1_KI.jpg)

*Photo by [Victor](https://unsplash.com/@victor_g?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Context

Most cloud providers have a way to give the Pods running in Kubernetes an “identity” that maps back to a role within the respective cloud providers.

For Amazon it’s **IAM Roles for Service Accounts (IRSA)**, and for GCP it’s Workload Identity. Azure follow’s Google’s naming convention closer with Entra Workload ID.

There’s a [decent tutorial](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity) on how to set this up manually, but I found I had to dig quite a bit for the right terraform resources to not create things using the `azure` CLI as they suggest, so I thought I’d share what I found.

### The AKS Cluster

The most important additions to a traditional AKS terraform block is that you need to enable the oidc issuer and workload identity.

[These will enable the cluster to](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview?tabs=dotnet#how-it-works):

- Properly issue tokens for workloads (i.e. to your Pods)
- Mutate your Pods to inject those tokens using a mutating webhook.

Instead of showing the terraform I used, I’ll just add into the examples in the terraform registry.

```java
// main.tf for the AKS cluster
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

resource "azurerm_kubernetes_cluster" "example" {
  name                = "example-aks1"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  dns_prefix          = "exampleaks1"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Production"
  }
  
  // These two are required!
  oidc_issuer_enabled       = true
  workload_identity_enabled = true
}
```

Depending on how you have your terraform set up, you’ll need one of the outputs from your cluster. If you’re using modules you’ll need an `outputs.tf` file with the following

```lua
output "kubernetes_oidc_issuer_url" {
  value = azurerm_kubernetes_cluster.example.oidc_issuer_url
}
```

Once our cluster is up, we’ll be able to see some `azure-wi-webhook` in the `kube-system` namespace, which will do the job of injecting the tokens.

Next we’ll create our Managed Identities and allow them to be assumed within the cluster

### Managed Identities

These identities are created using the `azurerm_user_assigned_identity` resource, which allows us to create an identity and give it whatever permissions we want (or are capable of bestowing).

Let’s create an identity and let it write to a storage account, while also allowing the AKS to issue a token to this identity (we do this with the `azurerm_federated_identity_credential` resource).

```java
// main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

locals {
  identity_name = "example_worker"
  resource_group_name = "example_resource_group"
  location = "West Europe"
  namespace = "my-namespace"
  service_account_name = "test-service-account"
}  

resource "azurerm_user_assigned_identity" "example_worker" {
  name                = local.identity_name
  resource_group_name = local.resource_group_name
  location            = local.location
}

// Allow our identity to be assumed by a Pod in the cluster
resource "azurerm_federated_identity_credential" "example_worker" {
  name                = local.identity_name
  resource_group_name = local.resource_group_name
  audience            = ["api://AzureADTokenExchange"]
  issuer              = var.kubernetes_oidc_issuer_url // Use the output from above or if in the same file
//issuer              = azurerm_kubernetes_cluster.example.oidc_issuer_url
  parent_id           = azurerm_user_assigned_identity.example_worker.id
  subject             = "system:serviceaccount:${local.namespace}:${local.service_account_name}"
}

data "azurerm_storage_account" "example" {
  name                = "example_storage_account"
  resource_group_name = local.resource_group_name
}

// Give our managed identity some permissions
resource "azurerm_role_assignment" "example_worker_blob_contributor" {
  scope = data.azurerm_storage_account.example.id

  // using azure defined role
  role_definition_name = "Storage Blob Data Contributor"

  principal_id = azurerm_user_assigned_identity.example_worker.principal_id
}
```

OK! Quite a bit there, but I think instead of explaining it without the last piece (the Kubernetes bit) I figured I’d just point out what we’re going to need for our Service Account and Deployment/Pod.

We’ll need the `client_id` for the user managed identity we just created. We can create another output if we’re going to install things outside of terraform or in another module.

```lua
output "managed_user_client_id" {
  value = azurerm_user_assigned_identity.example_worker.client_id
}
```

Once you run this Terraform, you should be able to see “Managed Identities” appear on the appropriate storage account as a Blob Contributor.

### Service Account and Deployment

The ServiceAccount we create that maps to this managed identity has to match up with the same Namespace and name as we had above, otherwise we won’t properly map any tokens.

```ini
namespace = "my-namespace"
service_account_name = "test-service-account"
```

The appropriate ServiceAccount needs one additional value, that client\_id from before, mapped to the appropriate annotation. A relevant ServiceAccount would look like so

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    azure.workload.identity/client-id: 29ad5555-7acdf-44a8-8aa5-1431283123
  name: test-service-account
  namespace: my-namespace
```

Where `29ad5555–7acdf-44a8–8aa5–1431283123` is a made up client\_id, but should map to the one you created with terraform.

The last piece we need is our Deployment. It needs to

1. Use the ServiceAccount we just created
2. Also have a special podLabel we have to add, `azure.workload.identity/use: "true”` , otherwise the webhook won’t do anything (despite using the ServiceAccount… anyway…)

An example deployment might look like (if we were just going to deploy `busybox` )

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: busybox
  namespace: my-namespace
spec:  
  replicas: 1
  selector:
    matchLabels:
      app: busybox
  template:
    metadata:
      labels:
        app: busybox
        azure.workload.identity/use: "true"
    spec:
      # The SA we created above
      serviceAccountName: test-service-account
      containers:
      - name: busybox
        image: busybox:1.30.1
        command:
          - "sh"
          - "-c"
          - "while true; do sleep 6000; done"
```

If you `kubectl exec busybox... -- env` and everything is set up correctly you’ll see the appropriate Environment variables for an Azure Identity Authentication (i.e. a client id, a token file).

Hopefully that helps you set up some Managed Identity Workloads in Terraform. Good luck!
