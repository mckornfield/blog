---
title: "Installing Python on a Mac and Changing The Shell… I Done Goofed"
subtitle: "It’s all about the PATH-fu"
date: 2022-11-10
medium_url: "https://medium.com/@mckornfield/installing-python-on-a-mac-is-annoying-4247eb5920c"
---

It’s all about the PATH-fu

![(This is a rattlesnake not a python, but they’re meaner) Photo by Meg Jerrard on Unsplash](/img/installing-python-on-a-mac-and-changing-the-shell-i-done-goo/0_U1GhV9BuJ-tj1qM2.jpg)

*(This is a rattlesnake not a python, but they’re meaner) Photo by [Meg Jerrard](https://unsplash.com/@mappingmegantravel?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Wait, I need to install Python, don’t I already have it?

If you happen to get a new M1 Mac, you’ll notice that you already have python installed (and yay it’s actually python3).

But the version installed, at least on the one I just set up, was `Python 3.8.9` . That version came out in April, get with the *times!*

So easy, I just need to install python, reach for my handy dandy `brew`.

This mac is BRAND new, so I head to [brew.sh](https://brew.sh/) and then copy their install command into my terminal, and I’m cooking.

It also asks me to run these lines, which I did do… but then I ended up switching away from zsh to bash:

```
echo '# Set PATH, MANPATH, etc., for Homebrew.' >> /Users/mckornfield/.zsh
```

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/mckornfield/.zsh
```

```
eval "$(/opt/homebrew/bin/brew shellenv)"
```

This basically throws two lines in your `~/.zsh` file that will set up your PATH variable so the brew paths go first.

I then installed my new python, easy.

```
brew install python3
```

Now of course, doing this and then switching to `bash`

```
brew install bash
echo /opt/homebrew/bin/bash | sudo tee -a /etc/shells
chsh -s /opt/homebrew/bin/bash 
```

shouldn’t be a big problem, should it?

### It was a problem

When I went back to bash and ran `python3 --version` I saw the same dang `3.8.9` pop out. 🙃

Well well, turns out my PATH looked like this:

```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

(An aside on your PATH, it’s the list of directories that the terminal/CLI looks for programs to run. If you’re trying to run a program without a reference to the path (i.e. `./my_script.sh` ) then the terminal looks in your path, starting from the first of the `:` separated folders. Missing programs, programs on the wrong version, or “command not found” errors are usually a sign that your PATH ain’t right.)

I needed to add those special shellenv lines to my `~/.bash_profile` . Then after opening a new terminal/sourcing I got something more helpful for my PATH.

```
/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

And `python3 --version` gave me `Python 3.10.8` , something that came out in October, yay.
