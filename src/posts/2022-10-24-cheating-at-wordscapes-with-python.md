---
title: "Cheating at Wordscapes, with Python"
subtitle: "Why know words when you can look for them in a text file?"
date: 2022-10-24
medium_url: "https://medium.com/@mckornfield/cheating-at-wordscapes-with-python-40b3ec3f453b"
---

Why know words when you can look for them in a text file?

![Photo by Jeremy Allouche on Unsplash](/img/cheating-at-wordscapes-with-python/0_d_Rsotuj2dn0Y5It.jpg)

*Photo by [Jeremy Allouche](https://unsplash.com/@jerroams?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

If you haven’t heard of [Wordscapes](https://apps.facebook.com/wordscapes), it’s a game where you swipe letters to fill in a crossword puzzle. If you know a lot of English words, it’s pretty simple! But sometimes the words can be a bit more obscure.

In this article I’ll go over my approach for how I cheated at Wordscapes (yes there’s sites like [this](https://wordscapes.yourdictionary.com/) but I wanted to cheat *my way).*

Tl;dr I wrote a [Python script](https://replit.com/@mckornfield/Wordscapes#main.py) that looks like the below. I’ll do my best to explain it to you

```
from collections import Counter
  
def is_match(word: str, guess_set: set, guess_counter: Counter):
    return set(word).issubset(guess_set) and not Counter(word) - guess_counter
```

```
while True:
  letters = input("Enter six or more letters: ")
```

```
guess_letters = set(letters)
  guess_counter = Counter(letters)
  answers = []
  with open('words_short.txt') as f:
    for line in f.read().splitlines():
      if is_match(line, guess_letters, guess_counter):
        answers.append(line)
```

```
for size in range(3,len(letters)+1):
    print(f"\n== {size}  letter words ==")
    i = 0
    for answer in answers:
      if len(answer) == size:
        print(answer, end='  ')
        i += 1
      if i == 3:
        print("")
        i = 0
  print("")
```

Not the most beautiful code in the world, but it prints out something like this, given an input of `cdusea`

```
Enter six or more letters: cdusea
== 3  letter words ==
ace  adc  ade  
ads  aes  ase  
aud  aus  cad  
cud  cue  dae  
das  dau  dca  
dea  dec  des  
duc  due  ead  
eau  ecu  eds  
esc  esd  esu  
sac  sad  sae  
sau  sea  sec  
sed  sud  sue  
uca  uds  usa  
use  
== 4  letter words ==
aced  aces  acus  
aesc  cade  cads  
case  caus  cuda  
cuds  cued  cues  
dace  dase  deas  
desc  deus  duce  
ducs  dues  ecad  
ecus  educ  esau  
esca  euda  sade  
scad  scud  sude  
sued  used  
== 5  letter words ==
cades  cadus  cased  
cause  daces  dacus  
decus  duces  sauce  
suade  
== 6  letter words ==
caused  sauced
```

Now you can swipe your answers into Wordscapes and move through the levels no problem. It can be a good assist if you get stuck!

## The Script

The Python script can be broken down into three parts.

### Matching

```
def is_match(word: str, guess_set: set, guess_counter: Counter):
      return set(word).issubset(guess_set) and not Counter(word) - guess_counter
```

This section basically checks if the word is a subset of the letters passed in (the guess set) and then uses a `Counter` to decide if the counts of the letters are the same. These two combined are a relatively quick way to check if a word is an anagram of the `guess_set`. You could also use a dictionary with counts, but that’s what our handy dandy `Counter` does for us. We negate the subtraction, because if `Counter(word) - guess_counter` returns anything but an empty `Counter`, we know that something is unaccounted for.

The reason to check the set part first is that it is a much faster operation than the `Counter` calculation and difference is.

### Reading from our dictionary

I started with a Python library `english-words` but it wasn’t enough, so I found a decent sized txt file with lots of English words in it, and just read that in line by line to see if any of the lines match. We also pre-calculate the `Counter` and `set` for the guess letters, so we don’t do it every time.

```
letters = input("Enter six or more letters: ")
```

```
  guess_letters = set(letters)
  guess_counter = Counter(letters)
  answers = []
  with open('words_short.txt') as f:
    for line in f.read().splitlines():
      if is_match(line, guess_letters, guess_counter):
        answers.append(line)
```

If we find any match, we just append it. Simple!

### Some nice looking formatting

One of the anagram solver sites I saw formatted things nicely in a three column format. So I have a not very optimized loop (it’s ok there’s never more than 50–100 answers) to print them in that three column format

```
for size in range(3,len(letters)+1):
    print(f"\n== {size}  letter words ==")
    i = 0
    for answer in answers:
      if len(answer) == size:
        print(answer, end='  ')
        i += 1
      if i == 3:
        print("")
        i = 0
  print("")
```

I use an internal `i` to keep track of the column length, and add a newline if we get to our third column. Big brain code right here.

That’s all I’ve got!

Stay tuned; I’ll share the next step of my cheating, where I used pyautogui to swipe the letters for me :)
