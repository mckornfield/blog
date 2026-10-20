---
title: "Correlating Logrus Logs and Trace IDs in Datadog"
date: 2023-05-03
medium_url: "https://medium.com/@mckornfield/correlating-logrus-logs-and-trace-ids-in-datadog-a31c4bac92c"
---

Because their docs are just so lame right now

![Photo by Matthew Henry on Unsplash](/img/correlating-logrus-logs-and-trace-ids-in-datadog/0_8ncj4ZrVcJvg7VlI.jpg)

*Photo by [Matthew Henry](https://unsplash.com/@matthewhenry?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Recently I went to the Datadog docs to see how I could get my logs and traces nicely lined up. We use logrus, so I thought it’d be really easy to get set up, but the [docs are just so dang sparse](https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces/go/).

It’s basically “manually print the span into your log message.” Yeah no that totally sucks.

I thought I’d engineer something fancy, but as with most things, someone else already added something fancy for me.

First off: if you’re just using plain logging in Go, you should switch to [Logrus](https://github.com/sirupsen/logrus/tree/master). It does structured logging (which is where Datadog’s indexing really shines), and it’s super easy to use as a drop in replacement for the regular log library.

Next: assuming you have logrus installed and the datadog tracing libraries installed,

```bash
go get github.com/sirupsen/logrus
go get gopkg.in/DataDog/dd-trace-go.v1/ddtrace
```

and you’ve got your tracer started in your main function

```go
import (
"gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func main() {
 tracer.Start(tracer.WithAgentAddr("host:port"))
 defer tracer.Stop()
 ...
}
```

you’ll just need to make sure logrus is initialized with this [fancy hook that is not very well documented](https://pkg.go.dev/gopkg.in/DataDog/dd-trace-go.v1@v1.50.0/contrib/sirupsen/logrus)

```scss
import (
 "github.com/sirupsen/logrus"
 dd_logrus "gopkg.in/DataDog/dd-trace-go.v1/contrib/sirupsen/logrus"
)

...
func Init() {
 logrus.SetFormatter(&logrus.JSONFormatter{}) // Datadog ingests JSON easily
 logrus.AddHook(&dd_logrus.DDContextLogHook{}) // This'll do it! And it's included from the install
}
```

Which will automatically inject the trace id to your logs as long as you log information using `logrus.WithContext` , e.g.

```go
log.WithContext(ctx).Info("hello datadog!")
```

As long as a [span has been started](https://docs.datadoghq.com/tracing/trace_collection/custom_instrumentation/go/) (`tracer.StartSpanFromContext` ) and the context passed into your functions, the hook you set up will grab the span info from the context, and your logs will be nicely correlated within Datadog.

So there you have it… just add the context hook, and make sure you start the span/ pass the context around.

Thanks for reading! Hopefully this helps you.
