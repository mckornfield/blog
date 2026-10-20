---
title: "Switch Between Kubernetes Clusters Quickly"
subtitle: "If you have more than one cluster to deal with, this can save you some time"
date: 2023-03-01
medium_url: "https://medium.com/@mckornfield/switch-between-kubernetes-clusters-quickly-bf6dc004142d"
---

If you have more than one cluster to deal with, this can save you some time

![Photo by Leo Rivas on Unsplash](/img/switch-between-kubernetes-clusters-quickly/0_9Ufnqq5MZRvBvbcs.jpg)

*Photo by [Leo Rivas](https://unsplash.com/it/@leorivas?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Context is Key

If you use `kubectl` , most of your commands are going to rely on what your current `kubeconfig` is set up with.

When you have more than one Cluster you have to switch between, you’ll probably see something like this when you run `kubectl config get-contexts`

```ruby
CURRENT   NAME          CLUSTER                                  
          cluster-1     arn:aws:eks:us-east-1:X:cluster/cluster-1
          cluster-2     arn:aws:eks:us-east-1:X:cluster/cluster-2
*         cluster-3     arn:aws:eks:us-east-2:X:cluster/cluster-3
```

Granted, you’ll have a few more columns and they’ll wrap, but this is probably the most important part of the output: the cluster and the name. The star next to the context name lets you know which one is the current one.

So what would you do to set your contexts normally? Well you might…

### List Your Configs, Then Pick One

This was my standard workflow for a long time. I would run:

```ruby
$ kubectl config get-contexts
CURRENT   NAME          CLUSTER                                  
          cluster-1     arn:aws:eks:us-east-1:X:cluster/cluster-1
          cluster-2     arn:aws:eks:us-east-1:X:cluster/cluster-2
*         cluster-3     arn:aws:eks:us-east-2:X:cluster/cluster-3

# And then I copy paste the name of one
$ kubectl config use-context cluster-1
```

If you only switch clusters every so often, then this clumsy set of steps is fine. But if you’re trying to move resources around and switching back and forth quickly to check on things, maybe you need something a a bit smarter.

### Some Bash Tab Complete, Simple Version

What really saves you time is not having to type. On the terminal, that usually means using `ctrl+r` to reverse search, or tab completion after typing a few characters.

Many many things support tab completion scripts, including `kubectl config use-context`, [assuming you have it installed](https://medium.com/nerd-for-tech/enable-auto-completion-for-kubectl-in-a-linux-bash-shell-16420d42e3ec). So you can just type

```bash
kubectl config use-context # and then hit tab twice here, 
# and your list of configs will complete and prompt
```

So we’re done right? Isn’t this good enough?

### But “kubectl config use-context” is Too Much to Type

So what’s the simple solution? Placing this in your `~/.bash_profile` or equivalent `$SHELL_profile` file will get you autocomplete with a lot less typing.

```bash
ukc() {
  kubectl config use-context "$@"
}
_ukc_complete() {
  COMP_WORDBREAKS=${COMP_WORDBREAKS//:}
  local prefix="${COMP_WORDS[COMP_CWORD]}"
  local contexts="$(kubectl config get-contexts -oname)"
  COMPREPLY=($(compgen -W "$contexts" -- "$prefix"))
}
complete -F _ukc_complete ukc
```

To unpack the complete function, which is definitely the most interesting, it does a handful of strange looking things.

1. Removes colon `:` from word breaks, since at least my contexts had a lot of colons in them (yay AWS)
2. Gets the current word, i.e. the `prefix` by using bash array indexing
3. Prints out the contexts by name
4. Uses `compgen` to match the prefix to the contexts and fill a special variable, COMPREPLY, which the shell interprets as the list of things to suggest

Using this, you can type `ukc` and after hitting tab you’ll get some completion. Nice huh?

### Last But Not Least, Annoyingly Long Contexts

In the example I showed above, the context names were nice, like `cluster-1` etc. But for projects I’ve worked on the contexts can basically be the same name as the cluster, e.g. in AWS they might look like `arn:aws:eks:us-east-1:X:cluster/cluster-1` .

Tab completion might get annoying when narrowing down regions and accounts… what if you could just do it based on the cluster name.

You can simply [rename your contexts](https://stackoverflow.com/a/59606450) if you don’t want to go through as much tab complete, but I wanted to leave the contexts as they are, since that’s the standard that we have.

Instead, I’ll just pipe my argcomplete and `ukc`through some functions, so I can autocomplete with a friendlier name. Just splitting on the slash and then looking the contexts back up with grep seems to do the trick.

```bash
ukc() {
  context_name=$(kubectl config get-contexts -oname | grep -m1 "$@")
  kubectl config use-context $context_name
}
_ukc_complete() {
  COMP_WORDBREAKS=${COMP_WORDBREAKS//:}
  local prefix="${COMP_WORDS[COMP_CWORD]}"
  local contexts="$(kubectl config get-contexts -oname | cut -d/ -f2)"
  COMPREPLY=($(compgen -W "$contexts" -- "$prefix"))
}
complete -F _ukc_complete ukc
```

The only difference between this and the above is the cut on the slash, which gives us the friendlier cluster name, and the grep to look the context back up by name.

### Use Something Off the Shelf (kubectx) (EDIT)

If you don’t want to throw things into your `*_profile` you can use [kubectx](https://github.com/ahmetb/kubectx), which is a high powered version of the functions I listed above. It can also provide useful namespace switching, as well as the ability to jump back to the previous cluster with `kubectx -` . Pretty nifty!

Let me know if this helps you out. Thanks for reading!
