---
title: "I Wrote a Wordscapes Bot in Python, And Became a Screenshot Hoarder"
date: 2022-10-25
medium_url: "https://medium.com/@mckornfield/i-wrote-a-wordscapes-bot-to-swipe-for-me-3b4cac9f60f4"
---

Hey, bots want to have fun too!

![Photo by Daniel Klein on Unsplash](/img/i-wrote-a-wordscapes-bot-in-python-and-became-a-screenshot-h/0_pb55YxP9vgUlmLKp.jpg)

*Photo by [Daniel Klein](https://unsplash.com/@danielklein?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I wrote [an article](https://mckornfield.medium.com/cheating-at-wordscapes-with-python-40b3ec3f453b) explaining how I built a simple anagram solver for [Wordscapes](https://apps.facebook.com/wordscapes). But then I got stupidly obsessed with how I could take my cheating to the next level. I didn’t want to swipe anymore! But what could I use to swipe the screen for my lazy behind?

Enter `pyautogui`

It’s a Python library that lets you, among other things, screenshot and click around a screen on different platforms. There are faster platform specific options but for my needs this was more than sufficient.

If a pictures worth a thousand words, then a gif is worth 1000s of words yeah?

![Yes I have a tab open for how to screen record. OBS ftw!](/img/i-wrote-a-wordscapes-bot-in-python-and-became-a-screenshot-h/1_ncRE2I8hSIZalY570BxKtw.gif.gif)

*Yes I have a tab open for how to screen record. OBS ftw!*

How does it work? Let me break it down for you. (All the code is [here](https://github.com/mckornfield/wordscapes-cheat).)

### A Dumb Solver

The [very first version](https://github.com/mckornfield/wordscapes-cheat/blob/master/wordscape_player/dumb_solver.py#L7) of this used a set of points that were fixed on the screen and permuted through them. The code is:

```
from itertools import permutations
```

```
import pyautogui as pg
from typing import List, Tuple
from pyscreeze import Point
```

```
LEFT_CHAR_POS = Point(360, 820)
TOP_CHAR_POS = Point(480, 695)
RIGHT_CHAR_POS = Point(605, 814)
BOTTOM_CHAR_POS = Point(483, 945)
```

```
def _gen_permutation(n: int):
    return _gen_permutation_for_list(
        [LEFT_CHAR_POS, RIGHT_CHAR_POS, TOP_CHAR_POS, BOTTOM_CHAR_POS], n)
```

```
def _gen_permutation_for_list(positions: List[Point[int]], n: int):
    return permutations(positions, n)
```

```
def _move_through_permutation(permutation: List[Tuple[str]]):
    for i, pos in enumerate(permutation):
        duration = 0.001
        pg.moveTo(x=pos[0], y=pos[1], duration=duration)
        if i == 0:
            pg.mouseDown()
    pg.mouseUp()
```

```
def position_based_permute_solver(positions: List[Point[int]]):
    for i in range(3, len(positions)+1):
        for permutation in _gen_permutation_for_list(positions, i):
            _move_through_permutation(permutation)
```

```
def four_char_permute_solver():
    for permutation in _gen_permutation(3):
        _move_through_permutation(permutation)
    for permutation in _gen_permutation(4):
        _move_through_permutation(permutation)
```

This would just swipe all the permutations for 3 and 4 positions, hard coded to the exact pixel placement I got by running `pyautogui.mouseInfo()` and seeing what the number was for my cursor. While fun and pretty stupid, this approach fell apart as soon as a fifth and sixth character were introduced. Instead of just adding more pixel positions and permutations, I decided to try and be smarter.

### The Pitfalls of Trying to Be Smarter

If you want to pick letters on the screen, you find that the first thing you need to do is have a screenshot of those letters to “find” them. This is a chicken and egg problem that is solved by me:

1. Pausing the solver
2. Screenshotting a picture of each letter
3. Adding them to a folder and labelling each with the corresponding letter (e.g. `a.png` )
4. Restarting the solver and seeing if it’s smart enough to find the letter

![The price of being smart is knowing what the letter “C” looks like](/img/i-wrote-a-wordscapes-bot-in-python-and-became-a-screenshot-h/1_67pcbhiLm6bnBd9TSNb37w.png.png)

*The price of being smart is knowing what the letter “C” looks like*

`Pyautogui` wraps a handful of other image libraries like `opencv` and `Pillow` , but basically I just played around with how I could set the confidence when matching, and found that for certain letters like O and Q I needed to [up the similarity](https://github.com/mckornfield/wordscapes-cheat/blob/master/wordscape_player/letter_finder.py#L19). I then needed to deduplicate all the matches found right around the letter, since lowering the confidence meant that you got a lot of clustered duplicates. Also I kept finding I’s inside H’s, so annoying.

Being smart is annoying!

Anyway having played around with that a ton, I also realized I had to highlight the letters to start (that’s the [initial sweep](https://github.com/mckornfield/wordscapes-cheat/blob/master/wordscape_player/highlighter.py#L26) in the gif above). I just hard coded some relative pixel positions to the back arrow at the top (more screenshots!)

### Putting it all together

Eventually my solver got pretty fancy, with multiple letters to match in case the background color changed, and I incorporated the anagram solver from the other video to give me my “guesses.”

The last bit of swiping that was kind of fancy was mapping those guesses to the identified letters and their positions. That looks like:

```
from collections import defaultdict
from typing import Dict, List
```

```
import pyscreeze
import pyautogui as pg
```

```
def guess_to_movement(guess: str, letter_points: Dict[str, List[pyscreeze.Point]]) -> None:
    letter_indices = defaultdict(lambda: 0)
    for i, letter in enumerate(guess):
        duration = 0.001
        point_index = letter_indices[letter]
        pos = letter_points[letter][point_index]
        letter_indices[letter] += 1
        pg.moveTo(x=pos[0], y=pos[1], duration=duration)
        if i == 0:
            pg.mouseDown()
    pg.mouseUp()
```

The data we’re dealing with looks like `{"e": [Point(1,2), Point(3,4)], "b": [Point(5,6)]}`

So if we had a guess like `Bee` we’d

1. go to the point corresponding to B
2. roll B’s index forward in case there was another B again
3. put the mouse down since it’s the first index
4. (Looping around) now go to the first E point, and incrementing the index corresponding to E
5. (Looping around) now go to the second E point, and increment the index, though we won’t need it
6. Pick up the mouse

And there you have it, something that can find letters on a page, translate those letters to guesses, and translate those guesses back to swiping.

After doing this for a while it can be satisfying to watch, but mostly I just became a screenshot hoarder. Still haven’t found my letter Z yet :(

Thanks for reading! Feel free to try out the code if you want to sit back and watch the swiping.

![https://chatbotslife.com/](/img/i-wrote-a-wordscapes-bot-in-python-and-became-a-screenshot-h/1_SoWs0APz9Sb2p1RKBD5BFg.png.png)

*<https://chatbotslife.com/>*
