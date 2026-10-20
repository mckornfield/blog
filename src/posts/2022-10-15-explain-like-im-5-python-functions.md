---
title: "Explain Like I’m 5: Python Functions"
subtitle: "Even if you can’t write a line of code, I’ll explain it to you."
date: 2022-10-15
medium_url: "https://medium.com/@mckornfield/explain-like-im-5-python-functions-e71bbefdfbb"
---

![Photo by Oleksandr Kuzmin on Unsplash](/img/explain-like-im-5-python-functions/0_yId50Npd8MD5XAoZ.jpg)

*Photo by [Oleksandr Kuzmin](https://unsplash.com/@kriplok?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Even if you can’t write a line of code, I’ll explain it to you.

Recently I was trying to explain functions in Python to someone and I’m not sure I really made much progress. So I thought I’d take a different tack and explain it like I’m talking to a five year old, so maybe I can help get through to them and other folks.

### What’s Python?

Python is a language that lets you tell a computer to do certain tasks. Some whole websites/ apps are run on Python (like [Instagram](https://instagram-engineering.com/tagged/python)) or sometimes Machine Learning scientists use it to do cool things, like [generate images](https://huggingface.co/spaces/stabilityai/stable-diffusion).

### What’s a function?

If you remember from math class, maybe f(x) = mx + b is familiar? A function is something that takes in an input and maps it to some sort of output. Let’s stay away from math and computers and just go with an analogy. How might I compare functions to something outside of a computer?

Imagine Python is comparable to the instructions that you get with a piece of furniture.

When those instructions say something like “screw in four screws”, you perform that instruction **for each** screw and then move onto the next step.

```
1. Screw 4 B screws into the holes as shown
```

The instruction book doesn’t say something like “turn the screw counter clockwise with a Phillips head screwdriver 30 times”. It uses **an alias** for that **specific set of instructions,** which is “put the screw into the furniture**.”**

You could imagine that if you were totally new to furniture, and the instructions were really forgiving, you might see something like:

```
1. Screw 4 B-screws into the holes as shown
```

```
Screw -> Put the screw into the hole
Put the screwdriver into the screw head
Until the screw is flush with the wood, rotate the screwdriver counterclockwise
```

Defining what “screw” is could be considered “defining a function” in the software world.

Let’s write this out in Python, and see if it makes any sense to our 5 year old brain.

```
for screw in screws:
  screw_into_furniture(screw, screwdriver)
```

Don’t worry about where things are “defined”, just understand that this code is calling a *function* on each screw and using the same screwdriver to do so.

The key part of the instruction book is it assumes you know what `screw_into_furniture` means.

The function `screw_into_furniture` is something that you as a screwdriver user has knowledge of. It represents the set of steps to pick up a screw, put it into the screw hole, insert the screwdriver, and spin however many times it takes to get the screw flush. Maybe it looks like:

```
def screw_into_furniture(screw, screwdriver):
  insert_screw_into_hole(screw)
  screwdriver.insert_into_screw_head(screw)
  while screw.is_not_flush():
    screwdriver.rotate_counterclockwise_180_degrees()
```

So there’s different things going on in this function, but hopefully it is readable. You’re deciding to

- put the screw into the hole
- put the screwdriver into the screw,
- while the screw is sticking out (not flush),
- you keep rotating the screwdriver.

The function requires that you tell it which screw you’re inserting, and also what screwdriver you’ll be using, those are passed in as **arguments**. (The holes would matter too, but we can ignore that for now hehe)

The power of a function is twofold.

1. It hides logic away from code so that the code can focus on the problem it needs to solve (building furniture) and not on other problems (like how to turn a screw). Functions let you create proper layers in your program.
2. Functions make it so you don’t have to constantly redefine instructions. Imagine how annoying the furniture instructions would be if instead of saying “screw” they had this block of words.

```
Put the screw into the hole
Put the screwdriver into the screw head
Until the screw is flush with the wood, rotate the screwdriver counterclockwise
```

This allows us to “not repeat ourselves.” Do not Repeat Yourself (DRY) is a core concept of clean coding.

### Another way to think of functions

![Photo by Robin Jonathan Deutsch on Unsplash](/img/explain-like-im-5-python-functions/0_jBi0t82sQtuPJfBq.jpg)

*Photo by [Robin Jonathan Deutsch](https://unsplash.com/@rodeutsch?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Functions can be really complicated, not as simple as turning a screw. They can call all sorts of other functions with their own arguments, like maybe you a function for buying something online.

Functions in the real world might be thought of as a takeout restaurant. You supply a set of requirements on what food you want, maybe with some amendments to the ingredients, and then you also give some money to pay for the food.

```
[ Money, Food Choice, Instructions ] -> [???] -> [ Takeout Items ]
```

Behind the scenes, chefs are busy preparing and making the food, but you have no idea what’s really happening since you can’t see inside.

They might just be putting things in the microwave! But hopefully not…

All you know is that after a few minutes, food appears and you are on your way.

The hidden kitchen, or what we might call a “black box” is another way to think of functions, especially ones that you did not write. You hand off some inputs (what food you wanted, money), wait however long, and then you are rewarded with some outputs (delicious food). Functions are the magic factory between those inputs and outputs.

Thanks for reading! Let me know if anything was confusing in the comments.
