---
title: "Keep it Structured Stupid! (KISS)"
subtitle: "Save yourself from squinting at log output later on"
date: 2023-09-25
medium_url: "https://medium.com/@mckornfield/keep-it-structured-stupid-kiss-5fec73f9497e"
---

![Photo by Etienne Girardet on Unsplash](/img/keep-it-structured-stupid-kiss/0_WS9opfI61QS5XSWc.jpg)

*Photo by [Etienne Girardet](https://unsplash.com/@etiennegirardet?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Why Logging Matters

There are many ways to tell if software isn’t working, but the one that everyone that’s taken a programming class knows how to do is to print something.

```kotlin
print("did this work?")
# did this work
System.out.println("How about this?");
// How about this?
fmt.Println("Or this?")
// Or this?
console.log("Hello from the frontend");
// Hello from the frontend
```

Printing is the most basic tool for debugging in a programmer’s arsenal. It has a few major flaws though, namely:

1. You don’t have different levels of severity
2. You can’t modulate what’s printed (either all things are printed or nothing)
3. The default printing functionality in programs is pretty lame (stdout or stderr? what about files?)

So if you’re on any software project that is worth its salt, it probably uses LOGGING. Essentially a fancy, much more usable wrapper around our friendly prints above:

```bash
logger.info("This is important")
# 2023-09-24 - INFO - This is important

logger.debug("This is not that important")
# 2023-09-24 - DEBUG - This is not that important

if bad_thing:
  logger.error("Uh oh")
  # 2023-09-24 - ERROR - Uh oh
```

You can set the log levels of a program on startup, or change them as it’s running, if you want to see some of those debug statements.

Logging is so rad!

### So We’re Done, Right?

There’s cooler things for monitoring like traces and metrics, but as far as logs go, putting a logger in and configuring a nice message format is a pretty good start.

But consider where your logs are going to go. If you’re just going to tail the logs of a container or something written to a file, then a standard log format is *fine*.

If your logs are going to some centralized logging mechanism, like Cloudwatch, Datadog, Loki, Splunk etc. then these simple log lines are not great.

The reason they’re not great is that these downstream tools have to do a fair amount of *parsing* to get useful information out of the logs. And if you have something like an Exception stacktrace printed, the tool has to be told to handle those multi-line logs (and at best, it’s just guessing).

So what’s the solution?

### What’s the Title of This Article?

**Keep it Structured Stupid!** *Structured* Logging is simply when the logs follow a machine interpretable format. Compare:

```
2023-09-24 - INFO - This is a log
{"timestamp": "2023-09-24", "level": "INFO", "msg": "This is a log"}
```

The first one might be a bit more human readable if looking at the logs directly, but the second one is *way* better for a log aggregation tool to ingest. So why again is structured logging better?

1. It will guarantee that you know the right counts of logs at different levels
2. Multiline exceptions will be easily parsable, both by you (the log viewer) and by the aggregator
3. The log aggregator will still just show that last `msg` piece carved out, so the readability will be the same or BETTER in the final destination, with any additional fields like request\_ids easily derivable by the log aggregation tools

### How Do I Keep It Structured?

There are all sorts of options for different languages, I’ll list some examples here:

**Python**

The most heavyweight option is [structlog](https://www.structlog.org/en/stable/standard-library.html). It’s quite a lot to set up, but can help if you want really rich logs (i.e. that have trace ids and all sorts of information, like which line of code emitted the log). If you want to do something more basic, [python-json-logger](https://pypi.org/project/python-json-logger/) will do the trick, just set it as your log formatter.

**Go**

The two options I’ve used for Go are [logrus](https://github.com/sirupsen/logrus) and [zap](https://github.com/uber-go/zap). I feel like zap is the winner as far as being actively maintained, but both present the option to enable JSON formatted logs. Zap’s logs are structured by default:

```go
// Logrus
import "github.com/sirupsen/logrus"

logrus.SetFormatter(&logrus.JSONFormatter{})
logrus.Info("Structured logger ready to go!")

// Zap
import "go.uber.org/zap"

logger, _ := zap.NewProduction()
logger.Info("This will be structured!")
```

**Java**

I don’t have much experience with structured logging in Java, but there’s a [logstash logback encoder](https://github.com/logfellow/logstash-logback-encoder#event-specific-custom-fields) if you want to give that a spin.

### Summary

If you’re using a log aggregator, keep things structured! You’ll be glad you did.
