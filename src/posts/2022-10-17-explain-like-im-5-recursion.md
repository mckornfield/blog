---
title: "Explain like I’m 5: Recursion"
date: 2022-10-17
medium_url: "https://medium.com/@mckornfield/explain-like-im-5-recursion-df66084e69e8"
---

Did you ever wonder why the site is called StackOverflow?

![Photo by Daniele Levis Pelusi on Unsplash](/img/explain-like-im-5-recursion/0_QNsyUnBItX7Zz3KL.jpg)

*Photo by [Daniele Levis Pelusi](https://unsplash.com/@yogidan2012?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I spent some time trying to explain recursion to folks who had seen it for the first time, so I wanted to try my hand at writing out what recursion is, why it’s useful, and why it can also be not so great…

Let’s begin!

### What is recursion?

Recursion is “when a function calls itself.” There that’s all you need to know, just memorize that and your life will significantly improve.

Just kidding, those are just words. I’ll assume you know what a function is (if not, [read here](https://mckornfield.medium.com/explain-like-im-5-python-functions-e71bbefdfbb)) and just continue from that point of understanding.

Functions are a ways to reuse code, and recursion is a way to reuse your function, but with slightly different input. The most common example thrown out is Fibonacci, a sequence of numbers that looks like

```
1 , 1 , 2 , 3 , 5 , 8 , 13
```

If the pattern isn’t that clear, each number is the sum of the previous two numbers. (Sometimes it’s shown with a `0` at the front, but we’ll ignore that for now.) What makes the Fibonacci sequence a great example for recursion is that it has two things going for it:

1. It has a base case (you need those for recursion, and we’ll get to why)
2. Every number in the Fibonacci Sequence can be defined as the result of two other numbers in the sequence

(1) is a requirement for your recursion to end. (2) makes your function a good candidate for recursion.

Another example of recursion is when searching through Trees (a programming structure with nodes and links). Typically programming trees are shown upside down from regular trees, like so:

```
                     ( )           <--- root of the tree
                   /    \
                 ( )    ( )        <--- children of the root
               /    \      \
             (  )  (  )   ( )      <--- grandchildren of the root
```

Moving through this tree where you try to get to the farthest leaf FIRST is called “Depth First Search.” Depth First Search is another great example of recursion, because:

1. You have a base case (a node with no children, i.e. a leaf)
2. Every node can be defined as a child of another node in the tree, except for the root (the initial input)

Trees are a relatively advanced concept, but know that they are extremely useful for storing sorted data, like set of numbers sorted by a max or a min value, called a Heap.

Now that you’ve seen a few examples of recursion, let’s talk about its usefulness.

### Why is it useful?

Recursion’s main power is that it can accomplish difficult tasks with very little code. Take the Fibonacci example. Compare the recursive approach to the iterative approach:

```
# Recursive
def fib(n: int) -> int:
    if n <= 1:
        return 1
    return fib(n - 1) + fib(n - 2)
```

```
# Iterative
def fibonacci(n: int) -> int:
    if n == 1:
        return 1
    prev = 1
    curr = 1
    for _ in range(1, n):
        temp = prev + curr
        prev = curr
        curr = temp
    return curr
```

Clearly the recursive approach looks more elegant, but also is just simpler to read. Reasoning about it might be a bit harder, but let’s step through it.

Consider passing `5` into the recursive fibonacci function. What might that look like?

```
                              fib(5)
                          /             \
                     fib(4)     +         fib(3)
                   /       \            /        \
              fib(3) +      fib(2) +  fib(2) +    fib(1)
           /       \        /   \      /   \               \
       fib(2) + fib(1) + fib(1) + fib(0) + fib(1) + fib(0) + 1
      /     \        \     /     /         /        /        /
     fib(1)  fib(0) + 1 + 1 +   1 +       1 +      1 +      1
     1     +  1     + 1 + 1 +   1 +       1 +      1 +      1
                                  8
```

Interesting how this set of calls looks like a tree doesn’t it? Hmmmmmmmm probably not a coincidence hahaha! Essentially at every step each node is broken into two nodes, unless you hit a base case (0 or 1), in which case the computation resolves, and you do indeed get 8, the 5th number in the Fibonacci sequence.

### Why is it not always so great?

![Photo by Brooke Lark on Unsplash](/img/explain-like-im-5-recursion/0_Dhfje5OPHnRM506R.jpg)

*Photo by [Brooke Lark](https://unsplash.com/@brookelark?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

The main downside of recursion are the ways that it can go wrong or be less performant than alternate approaches. One of the simplest ones is the aforementioned “StackOverflow.” When you call a function in any programming language, what you’re doing is saving your current place by placing that new call on the “call stack.” You then execute the function, and then once it returns, you pop that function off the call stack and continue executing.

Think of this setup like a stack of plates.

If you stack the plates too high (i.e. you call the same function too many times), you can get a `StackOverflow` error in Java. (In Python you’ll see a `RecursionError`). Normally this happens because you have a base case you never hit, or because you hit the limits of what is possible with vanilla recursion.

Before things even overflow, recursion can also take a lot of time doing duplicate work. Consider our example above for Fibonacci… There were an awful lot of nodes that looked the same (i.e. lots of `fib(2)` and `fib(3)` appeared). But the computer still spends time stacking those plates!

You can get around that using a technique called `memoization` , which I won’t get into but you can read about it in detail [here](https://towardsdatascience.com/memoization-in-python-57c0a738179a). This lets you use recursion but with a performance boost for edge cases.

In the examples I showed above, if you call the non-recursive method, `fibonacci(105)` , you’ll get a number pretty quick, but calling the recursive method `fib(105)` caused my Macbook to go into overdrive.

So to summarize:

- Recursion is great for homogeneous/ branching structures
- It makes for a very elegant solution to a difficult problem
- It can be slow or even break a program in more extreme cases, though there are tools to handle it

Thanks for reading!
