---
title: "I’ll Teach You the Python Basics in Under 10 Minutes"
subtitle: "But it will take you years to understand!"
date: 2022-11-02
medium_url: "https://medium.com/@mckornfield/ill-teach-you-the-python-basics-in-under-10-minutes-4ca4a94a7d68"
---

![Photo by Towfiqu barbhuiya on Unsplash](/img/ill-teach-you-the-python-basics-in-under-10-minutes/0_8TzZ5M05uxNtnHpQ.jpg)

*Photo by [Towfiqu barbhuiya](https://unsplash.com/@towfiqu999999?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

But it will take you years to understand!

I recently got some questions from someone on Python and I thought I’d just blow through them and see if things stick.

## Functions, Lists and Tuples, Oh my!

### What’s a function?

A reusable piece of code that you can call to do something. You can define them yourself, use built-in functions, or call someone else’s code via a library.

```
import requests # 3rd party library
```

```
print("hello my fellow person") # <--- built-in function
```

```
def add_two(a: int) -> int:
  return a + 2
```

```
print(add_two(3)) # <--- calling my own function
```

```
print(requests.get("https://httpbin.org/get")) # <--- Calling a 3rd party library function
```

If you want a longer explanation of functions, see [here](https://mckornfield.medium.com/explain-like-im-5-python-functions-e71bbefdfbb).

### What’s a list?

It’s the most common type of `Iterable` , i.e. something you can count or move over. Think of it like any list, maybe a short shopping list:

```
items_to_buy = ['Peanut Butter','Chocolate']
```

Lists can be empty or REALLY long, for example, here is an empty list or a list of all numbers up to one million (range isn’t inclusive hehe).

```
empty_list = []
all_numbers_to_one_million = [i for i in range(1,1000001)]
```

Iterables are great because you can *iterate* over them, for example

```
for item in items_to_buy:
  print(item)
```

The above is a lot easier than indexing into each item and printing it.

### What is a tuple?

A tuple is another kind of `Iterable` but it has a very nice property we call “immutability.” Think of a list like a group of cut out letters that you can rearrange and add more to, but a tuple is like a stone carving. If you want to change the stone carving, you have to throw it away and start over.

```
my_shopping_list = ("Peanut Butter", "Chocolate")
# my_shopping_list.append("Apples") # This line will not work!
my_shopping_list = my_shopping_list + ("Apples",) # This is really the only way to change it, making a new one
```

Tuples are awesome for things that aren’t supposed to grow in size (like maybe you want to know someone’s age and height, you could use `person_data = (20,60)` and refer to each piece later on.

### Are there built-in functions for tuples?

Yes, all the functions that act on [Iterables](https://docs.python.org/3/library/functions.html) work for tuples. Things like `max` , `min` , `len` , for loops, `sum` , and many more!

### What is the difference between functions, lists and tuples?

`Functions` -> Optionally take inputs, optionally perform some action, and optionally `return` outputs. The fact that these are all optional is confusing haha, but this is a valid function:

```
def my_func():
  pass
```

Useless! Unless you like the no-op pattern… but maybe wait to look that up

`Lists`-> Mutable (changeable) data structures that represent an ordered collection (i.e. there’s a 0th item, a 1st item… a sequence)

`Tuple` -> Immutable (unchangeable) data structures that represent an ordered collection (sequence)

I might as well also mention another good one to know

`Sets`-> Mutable (changeable) data structure that represents an unordered collection of unique items

```
my_set = set()
my_set.add("a")
my_set.add("a")
print(len(my_set)) # this will be one! the items have to be unique
```

## Miscellaneous questions

### Show me some basic Python Code

```
my_sum = 1 + 1
if my_sum > 3:
  print("never gonna happen")
else:
  for i in range(0, my_sum):
     print(i)
```

This code adds two numbers, makes an if check that will always fall through to the else, then prints out all the numbers from 0 to 2 (not inclusive), which is just 0 and 1. Super basic.

### Show me some advanced code

[I wrote a bot for Wordscapes](https://chatbotslife.com/i-wrote-a-wordscapes-bot-to-swipe-for-me-3b4cac9f60f4), that’s relatively advanced.

### When I see >>> inside IDLE, what does it mean?

`>>>` Is the python way of saying “please write me some valid Python code and I will execute it.” This is the standard beginning for a REPL (Read Evaluate Print Loop) in Python.

You will also see this if you just run `python` in a terminal program. The `>>>` signify to you as the Python programmer that your statement has to be valid Python, otherwise the Python Interpretter will flip out.

If you see `…` after you start a function or a loop, that means you are inside a control structure of some sort. You can think of it like a margin. You’ll have to hit enter twice once you are done, and make sure your tabbing is appropriate.

```
>>> def my_func(a,b):
...   return a + b
...
```

### What will this code produce: `>>> a = [‘foo’, ‘bar’, ‘baz’, ‘qux’, ‘quux’, ‘corge’]` ?

This makes a list (named `a` ) that has six items in it. It works this way because the list syntax is basically

```
[ # start of list
1,2,3,4 # any number of objects separate by commas, of any type
] # end of list
```

### What is the expression that returns “z” in “baz” from the below? How would I know?

![](/img/ill-teach-you-the-python-basics-in-under-10-minutes/1_Frll3mDkI-dXw8AlMZ2bBw.png.png)

This diagram is saying that x is a list, whose second element is also a list, and of that second list, the third element is also a list. In Python this would be:

```
x = [10, [3.141, 20, [30, 'baz', 2.718]], 'foo']
# we want the 2nd element of the first list, the 3rd element of the second list, 
# the 2nd element of the third list, 
# and the 3rd element of the word 'baz'. 
# You know this by following where the arrows go. Also everything is 0 indexed, so the 2nd element is really the 1st index
x[1][2][1][2] # this gives us "z"
```

### What is a nested list and how do I write one?

See right above, or for a simpler example…

```
my_nested_list = [1,2,[3,4,5]] # the [3,4,5] is the nested list
```

### How many ways can I append to a list?

I can think of three:

```
my_list = [1]
```

```
my_list.append(2) # the most common way
my_list = my_list + 3 # less common but also used
my_list.extend([4,5,6]) # this way only works for other lists/collections
```

### Help me write a statement to fill in `a = [1, 2, 7, 8]` so it has the missing numbers up to 8.

There’s more than one way, but [slice assignment](https://stackoverflow.com/a/39541404/10061484) is pretty cool

```
# slice assignment
a = [1,2,7,8]
a[2:2] = [3,4,5,6]
print(a)
```

```
# or using insert
a = [1,2,7,8]
for i in range(6,2,-1):
  a.insert(2,i)
print(a)
```

### How can I change this tuple to replace the second element?

`t = (‘foo’, ‘bar’, ‘baz’)` to replace the second element `(‘bar’)` with the string `‘qux’` from the tuple `(‘qux','quux')`?

```
t = ('foo', 'bar', 'baz')
t2 = (‘qux','quux')
t3 = (t[0], t2[0], t[2]) # this is the dumb way
print(t3)
t3 = list(t) # lists are mutable unlike tuples!
t3[1] = t2[0]
t3 = tuple(t3)
print(t3)
```

### What is the file extension for Python?

`.py`

## Bonus: Javascript questions

### What is the difference between Javascript and Python?

While both are interpreted, they have very different interpreters. Both are relatively slow languages since they are interpreted, and they are weakly typed (neither have requirements on objects being typed as you code them).

Javscript is mainly a web browser technology that has spread to be also server and device side (you’ll see it everywhere now). But it is still the king of web page design.

Python was primarily a scripting language that was taken and run with by data scientists and machine learning folks. It can be used for websites etc. but its greatest strength is as a robust scripting tool and code that helps glue together high performance C code.

### What’s the Javascript file extension?

`*.js` , and if you use React, you might see `*.jsx`

### Show me some easy JS code

```
const sum = 1 + 1
if (sum > 3) {
  console.log("never!")
} else {
  for(let i = 0; i < sum; i++){
    console.log(i)
  }
```

```
}
```

This code works the same as the above Python code but now it’s in Javascript :)

### Show me some advanced JS code

I wrote some code to filter my family cookbook website. [Here’s the code](https://github.com/mckornfield/goodman-cookbook/blob/master/assets/js/search.js#L1). A snippet of it looks like:

```
function filterElements(searchVal) {
  let elements = document.getElementsByTagName('li');
  if(searchVal){
    const lowerCaseSearchVal = searchVal.toLowerCase();
    for (let element of elements){
      let lowerCaseText = element.outerText.toLowerCase();
      if(lowerCaseText.includes(lowerCaseSearchVal)){
          element.style.display = "";
      } else {
          element.style.display = "none";
      }
```

```
}
  }  else {
    for (let element of elements) {
      element.style.display = "";
    }
  }
}
```
