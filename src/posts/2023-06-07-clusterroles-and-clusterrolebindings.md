---
title: "ClusterRoles and ClusterRoleBindings"
date: 2023-06-07
medium_url: "https://medium.com/@mckornfield/clusterroles-and-clusterrolebindings-f855faf25ea3"
---

The Jobs and Job Assignments of a Kubernetes Cluster

![Photo by Hamza El-Falah on Unsplash](/img/clusterroles-and-clusterrolebindings/0_SwtsxXFLQ4bNsv5q.jpg)

*Photo by [Hamza El-Falah](https://unsplash.com/@hamzaelfalah?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Today I thought I’d write about how you’d manage resources at the cluster level in Kubernetes, from within the cluster, and a core component of doing that is using ClusterRoles and ClusterRoleBindings.

There are also equivalently Roles and RoleBindings, but these are namespaced and can only interact with namespaced things, like Pods or Deployments.

If you want to control the Nodes within a cluster, for example, a Role would not be sufficient, since Nodes are a cluster level resource. So let’s talk through briefly what the two are and how you might use them.

### ClusterRoles

ClusterRoles are essentially the uniform/jobs that allow you to operate on a cluster. It’s an explicit list of access controls (RBAC -> Role Based Access Control) that tell you which operations you can do on which resources.

To relate this to something in the real world, if I had a ClusterRole to describe a firefighter, you might say that firefighters could run a siren, drive a firetruck, and put out fires on burning buildings.

You might also give firefighters another ClusterRole, i.e. acting as an EMT, or acting as a first responder to a car accident, even if there wasn’t a fire.

These ClusterRoles are permissions any firefighter has, regardless of who the person is or what neighborhood (namespace) they’re living in. The pieces to a ClusterRole are

- What the role is called (important for associating later)
- What resources the role can act on (and what group that resource belongs to, if any)
- What actions the role can take on those resources

Moving back to Kubernetes itself, let’s say you wanted to have a service that could get information about Nodes and update them, say with a taint (in the event that you wanted to evict pods) or annotation (in the event you want to say something is ready).

A sample of what that ClusterRole might look like would be:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-updater
rules:
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
    - watch
    - list
    - get
    - update
```

The `apiGroups` are blank because Nodes as a resource don’t fit into a group like `batch` (jobs) or `apps` (replicasets, statefulsets, daemonsets). The resources describe what you can act on (nodes) and the verbs describe what you can do.

### ClusterRoleBindings

Given the analogy about the firefighter, you might think of the ClusterRoleBinding as the registration of an individual as a firefighter. If I were to show up at the firestation, there would be locked doors and things preventing me from simply acting as a firefighter, whereas someone who was hired and processed would be given keys/ a PIN code/ a badge to act as the role of firefighter.

The firefighters could be hired as individuals (“users”) or they could be part of a group, maybe a class of firefighters that graduated all at once. Maybe some day, we’d have a firefighting robot, which we could consider the analogue for our “ServiceAccount.”

For ClusterRoles (and for regular Roles as well) there needs to be some component that binds the role to a principal (i.e. a user, group or service account). If we wanted to run this Node updater in a Pod, we’d have to associate the Pod with a ServiceAccount, and bind the ServiceAccount to the ClusterRole. An example might look like:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-updater-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: node-updater
subjects:
  - kind: ServiceAccount
    name: node-updater
    namespace: node-updater
```

This is given that we have a ServiceAccount (in the `node-updater` namespace) defined as

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: node-updater-sa
  namespace: node-updater
automountServiceAccountToken: true
```

In this case, we *do* want to mount the ServiceAccountToken, since we’ll need that to make Node updates via the API server.

Besides ServiceAccounts, a subject can be a [Group or a User](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-subjects).

If you want to test out what it would be like to create a Pod as this ServiceAccount, you can run the following, after creating the ClusterRole, ClusterRoleBinding and ServiceAccount

```bash
kubectl run test-perm -it --rm --image bitnami/kubectl:1.27.2  \
  --command   \
  --overrides '{"spec":{"serviceAccountName":"node-updater"}}' -- bash
```

This will launch a pod running as that service account, so calls to `kubectl get nodes` and `kubectl taint nodes <node_name> roll=true:NoSchedule` should succeed, based on our verbs list including `update` .

Thanks for reading!
