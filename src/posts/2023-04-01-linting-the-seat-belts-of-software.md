---
title: "Linting: The Seat Belts of Software"
subtitle: "My personal experience with linting, and why I think it’s worth it"
date: 2023-04-01
medium_url: "https://medium.com/@mckornfield/linting-the-seat-belts-of-software-13e9fdd955f7"
---

My personal experience with linting, and why I think it’s worth it

![Photo by Remy Lovesy on Unsplash](/img/linting-the-seat-belts-of-software/0_xaEPfd7R91BINs2v.jpg)

*Photo by [Remy Lovesy](https://unsplash.com/@lovesyautopics?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

## Seatbelts

Cars these days are pretty adamant about the fact that you should wear a seatbelt. Our family car, a 2008 Prius (they just don’t die, do they?) will beep incessantly if the driver or the passenger aren’t wearing their seatbelts. It’s annoying enough that even if you hate seatbelts, you’ll click it because you don’t want to get beeped at.

But they obviously are beeping for a reason. You can be fined for not wearing them, and [50% of car accident fatalities were for people not wearing seatbelts](https://www.cdc.gov/transportationsafety/calculator/factsheet/increasedfines.html#:~:text=However%2C%20in%202019%2C%20almost%20half,in%20traffic%20crashes%20were%20unrestrained.&text=As%20of%20January%202022%2C%20state,fines%20of%20%2425%20or%20less.).

They can be annoying, uncomfortable, and restraining. But all for a good reason.

Although most drivers and passengers won’t need them *most* of the time, the price for not wearing them in critical moments can be the highest price of them all. 💀

A **minor inconvenience** to forego a **major bit of suffering**.

What does that have to do with linting, well…

## Linting

If you’ve never heard the term, it refers to that [lint trap](https://en.wikipedia.org/wiki/Lint_%28software%29) you have on a drier that stops lint from getting to places that might cause a fire.

It is all over the software space, from warnings and errors at compile time (i.e. before the program can be converted to instructions the computer can read), to errors that are either bad practice, or bad style (i.e. unreadable).

Generally linting errors can be divided into two buckets:

- It’s better generally speaking to do it this way… (Warning)
- The way it is written will break or is completely broken (Error)

You might ask: shouldn’t the language tell me out of the box not to do certain bad things? Yes, those are where those *compiler* errors mentioned before come in, though those are generally speaking more like airbags or another car safety feature.

Programming can get complicated pretty quickly, and layering linting on top of what the language might already offer in terms of memory or type safety is like putting seatbelts in with your airbags.

Linting errors are *usually*

## Some Examples

Let’s dive into a simple Java example of why linting can make a difference.

### Java

I was involved in an incident where an application kept crashing because there was runaway thread creation.

(An aside, threads are a lightweight way to perform extra work by the computer, letting it switch between them within one program).

We knew there had been one recent change to a plugin, for a performance optimization (haha). The optimization involved not recreating the threads in question, but clearly it was doing the opposite of that… so what was the change? The addition of one conditional that looked liked:

```java
if (apiKey == apiKeyStore.getKey(KEY_CONSTANT))
```

Looks harmless, right? Well, what would a linter have to say about it?

```csharp
"==" and "!=" should not be used when "equals" is overridden
```

Essentially this `==` check works *sometimes (*i.e. if the memory addresses are the same for the two Strings), but in other cases it’s very wrong.

And those other cases happened to be what caused the application to keep crashing. And did this plugin have any linting in it? Nope… and not wearing the seatbelt.

The fix (with a built in null check) is simply

```less
if (Objects.equals(apiKey, apikeyStore.getKey(KEY_CONSTANT)))
```

### Python

A Python example, does this function look fine to you?

```python
def append_item_plus_five_to_the_list(item: int, my_list: list = []):
  my_list.append(item + 5)
  return my_list
```

Looks ok? This `= []` is actually a big problem, because of the way Python stores these default values, if you call this a few times in a row, you’re actually changing the *same list,* which can lead to unexpected behavior. This is true for dictionaries as well. Pylint says `Dangerous default value [] as argument` . Dangerous indeed haha.

Fixing it is possible by just assigning the list or other mutable thing INSIDE the function.

```python
def append_item_plus_five_to_the_list(item: int, my_list: list = None):
  if not my_list:
    my_list = []
  my_list.append(item + 5)
  return my_list
```

The real danger of using these mutable defaults is you get into a state where a list you expect to be empty to start has data from previous calls inside of it…

```scss
>>> append_item_plus_five_to_list(1)
[6]
>>> append_item_plus_five_to_list(2)
[6, 7]
>>> append_item_plus_five_to_list(5)
[6, 7, 10]
```

Just calling it multiple times, you’ll see that mutable default is referenced again… not good!

### Golang

A Golang Example, what if I just want to loop over some objects and append them to something, seems simple, right?

```go
for _, v := range versions {
    res := append(res, &v)
    ...

}
```

The golang linter will tell you off though, because your `res` variable is only going to have the last element over and over. `G601: Implicit memory aliasing in for loop. (gosec)`

If you want to [fix it](https://stackoverflow.com/a/68247837), you can use indexing or make v refer to what you would assume it refers to, the current object at that step in the loop.

```go
for _, v := range versions {
    v := v
    res := append(res, &v)
}
// or
for i := range versions {
    res := append(res, &versions[i])
}
```

## How to Do Linting Wrong

Linting should be annoying, but not completely cumbersome/ counterproductive. It should also be fast.

I worked somewhere where folks didn’t know how to solve linter errors ahead of pushing their changes to CI, i.e. to run some tests on a server.

This created a horrible back and forth, where people would push code, it would take minutes to hours to get results back, and when the results finished, whoops, there’d be a FindBugs/CheckStyle error (these are Java specific linters). You’d repeat the process, occassionally adding more errors as you addressed feedback from folks and changed the code.

And for the few folks that *did* know how to run the linter locally, for certain parts of the code it was horribly slow to run, so people just decided to shoot it to CI and wait it out.

That would be like if you didn’t put your seatbelt on, but received a fine in the mail some time later. Sure, it might get you to put your seatbelt on, but it isn’t really correcting the behavior in the moment, and it’s certainly going to piss you off.

## How to Do Linting Right

It should be:

- Right in the IDE, underlined and yelling at you with red and yellow
- Super easy to run it from a terminal command, to print out all known linter errors that you’ve introduced
- Ideally that above step can be put into a .[githook](https://git-scm.com/docs/githooks), so it runs whenever you try to commit/push changes
- That ease should translate to a fast feedback loop from CI, so you get anything you missed in minutes/seconds

Thanks for reading! And wear your seatbelt!
