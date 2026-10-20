---
title: "A Quick and Scrappy Bazel Autocomplete"
date: 2023-03-20
medium_url: "https://medium.com/@mckornfield/a-quick-and-scrappy-bazel-autocomplete-bd72630d0d3a"
---

A simple autocomplete to find available bazel commands.

![Photo by Lavi Perchik on Unsplash](/img/a-quick-and-scrappy-bazel-autocomplete/0_JGXPoy03hkRQm1br.jpg)

*Photo by [Lavi Perchik](https://unsplash.com/@laviperchik?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

tl;dr, Give it a spin: throw this in your `~/.bash_profile` or whatever prompt you use, and hit tab after typing `bazel` inside your bazel project to get the autocomplete going (first time will be a bit slow loading the targets). You’ll want to `rm /tmp/bazelq.txt` if you edit the set of bazel targets.

```bash
_bazel_complete() {
  cur="${COMP_WORDS[COMP_CWORD]}"
  _get_comp_words_by_ref -n : cur
  if [[ ! -f /tmp/bazelq.txt ]]; then
    bazel query //... | grep "//" >/tmp/bazelq.txt
  fi
  if [[ ${#COMP_WORDS[@]} < 3 ]]; then
    COMPREPLY=($(compgen -W "build query run test" "$cur"))
  elif [[ ${#COMP_WORDS[@]} < 6 ]]; then
    contents_without_colon=$(cat /tmp/bazelq.txt | cut -d: -f1 )
    for i in {3..5}; do
      contents=$(echo "$contents_without_colon" | cut -d/ -f1-${i} | uniq)
      possible_compreply=($(compgen -W "$contents" "$cur"))
      if [[ ${#possible_compreply[@]} > 1 ]]; then
        break
      fi
    done
    if [[ ${#possible_compreply[@]} == 1 || ${#possible_compreply[@]} == 0 ]]; then
      contents=$(cat /tmp/bazelq.txt)
      possible_compreply=($(compgen -W "$contents" "$cur"))
    fi
    COMPREPLY+=(${possible_compreply[@]})
  fi
  __ltrim_colon_completions "$cur"
}
complete -F _bazel_complete bazel
```

### Longer Explanation

Bash autocomplete is a bit of magic in my opinion. Just typing and hitting tab and all sorts of things have to happen to make the suggestions appear. I’ll try and explain what the script is doing and a bit about BASH autosuggestion as well.

Let’s go section by section:

```ini
cur="${COMP_WORDS[COMP_CWORD]}"
```

This just sets a variable `cur` equal to the `COMP_CWORD` indexed element in the `COMP_WORDS` array. These variables are filled by splitting the current terminal command by spaces and other separators (which I’ll get to in the next line).

```bash
_get_comp_words_by_ref -n : cur
```

Here’s a [relevant link](https://github.com/scop/bash-completion/blob/master/bash_completion#L519) for this function (or a variant of it). It basically tells the autocompletion splitting to not treat `:` as a word break, which is important since it’s part of the command, but not space separated. More info from this [StackOverflow](https://stackoverflow.com/a/12495480/10061484) on this and the below \_ltrim…

Next, something that we can use to get our bazel commands from:

```bash
if [[ ! -f /tmp/bazelq.txt ]]; then
    bazel query //... | grep "//" >/tmp/bazelq.txt
fi
```

This is a very simple way to give us a file that has all of our bazel targets in one file.

Next, the first case, where we haven’t typed `bazel run` yet…

```lua
if [[ ${#COMP_WORDS[@]} < 3 ]]; then
    COMPREPLY=($(compgen -W "build query run test" "$cur"))
```

`compgen -W` takes two arguments, the list of words to match against (technically a space separated array) and the word to match it against, which is our variable from before, `$cur` . `$cur` can be any part of the word, and if empty it will just present the whole array.

```bash
elif [[ ${#COMP_WORDS[@]} < 6 ]]; then
    contents_without_colon=$(cat /tmp/bazelq.txt | cut -d: -f1 )
    for i in {3..5}; do
      contents=$(echo "$contents_without_colon" | cut -d/ -f1-${i} | uniq)
      possible_compreply=($(compgen -W "$contents" "$cur"))
      if [[ ${#possible_compreply[@]} > 1 ]]; then
        break
      fi
    done
```

This next section is a bit silly, but essentially it queries that `bazelq.txt` file for commands, using our friend `compgen` again. The reason it uses cut and cuts to a variable number of fields is to simulate moving through a directory path, so we don’t try and suggest all the different paths and/or targets at once.

If the array `possible_compreply` is ever greater than 1, we break and just set it down below.

This last bit is how we query for the targets after the colon

```bash
if [[ ${#possible_compreply[@]} == 1 || ${#possible_compreply[@]} == 0 ]]; then
      contents=$(cat /tmp/bazelq.txt)
      possible_compreply=($(compgen -W "$contents" "$cur"))
    fi
    COMPREPLY+=(${possible_compreply[@]})
```

Essentially we just do the compgen but now with no special handling for the `:` character.

Finally, we append to the COMPRELY variable our possible matches, which will offer the user autosuggestion options just like in the simple case where we match `query,test,` etc.

The last little bit here

```bash
  __ltrim_colon_completion "$cur"
}
```

Is the other bit of special handling for the `:` included in the query.

And to bind our function to bazel as a form of autocomplete, we simply need to call.

```r
complete -F _bazel_complete bazel
```

That’s a wrap! If you have a question or if this was helpful, let me know! Tab completion can really let you move quickly through the terminal, combined with reverse search `ctrl+r` , you’ll be unstoppable.

Thanks for reading!
