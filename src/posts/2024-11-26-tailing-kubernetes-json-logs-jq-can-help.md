---
title: "Tailing Kubernetes JSON Logs? jq can help"
subtitle: "A bit of JSON parsing goes a long way"
date: 2024-11-26
medium_url: "https://medium.com/@mckornfield/tailing-kubernetes-json-logs-jq-can-help-2ce6fbe7bd21"
---

A bit of JSON parsing goes a long way

![Photo by Robert Larsson on Unsplash](/img/tailing-kubernetes-json-logs-jq-can-help/0_KguqbCdp8l_CByaw.jpg)

*Photo by [Robert Larsson](https://unsplash.com/@squareddesign?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### The Problem

Do you have logs that look like this? Maybe you’re just tailing logs from a Kubernetes pod, such as `kubectl logs -f my-pod-12345` and you see something like the following:

```json
{"timestamp": "21031", "level":"warn", "message": "something go brr", "user_context":"1234"}
{"timestamp": "21031", "level": "info", "message": "something else go brr", "user_context": "1234"}
```

Or maybe if they’re logs with so many fields that they wrap, so that you can barely tell what’s happening.

What can we do to handle these annoying log streams? Why didn’t we just use [logfmt](https://www.cloudbees.com/blog/logfmt-a-log-format-thats-easy-to-read-and-write)?!

Fear not! I have a simple solution: `jq`

### The Solution

This is a relatively complex jq function, since it handles the case when the line isn’t valid JSON, but behold!

```bash
kubectl logs -f my-pod-123 |
 jq -Rr '. as $line | try (fromjson | [.timestamp, .level, .message] | @tsv ) catch $line'
```

To break this down specifically:

`'. as $line | try (fromjson | [.timestamp, .level, .message] | @tsv ) catch $line'`

1. the `. as $line` sets the text to a variable, `$line`, which is what’s being read from the STDIN pipe
2. the next section attempts (`try` ) to read the string in as JSON, pull out these three fields `timestamp` , `level` and `message` , and then put them into a tab-separated values (`@tsv`)
3. In the event that the line is invalid JSON, we simply print the line as is `catch $line`

If your JSON format has different fields, you could use `.ts` `.lvl` or `.msg` as example replacements, if those were the keys being used

```json
{"timestamp": "21031", "level":"warn", "message": "something go brr", "user_context":"1234"}
{"timestamp": "21031", "level": "info", "message": "something else go brr", "user_context": "1234"}
```

Then becomes

```go
21031   warn    something go brr
21031   info    something else go brr
```

Ahhh… much better.

If this helps you let me know, or let me know if you have any other tricks for tailing JSON logs!

Thanks for reading.
