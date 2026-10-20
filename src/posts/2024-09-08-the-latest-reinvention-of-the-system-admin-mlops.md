---
title: "The Latest Reinvention of the System Admin: MLOps"
subtitle: "One does not simply “run a model”"
date: 2024-09-08
medium_url: "https://medium.com/@mckornfield/the-latest-reinvention-of-the-system-admin-mlops-d73abdbba29b"
---

One does not simply “run a model”

![Photo by BoliviaInteligente on Unsplash](/img/the-latest-reinvention-of-the-system-admin-mlops/0_QIuyTRyp1CECvJeP.jpg)

*Photo by [BoliviaInteligente](https://unsplash.com/@boliviainteligente?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I haven’t been in the IT industry long enough to see the transition from traditional system admins to DevOps engineers, but I’m living through the next step, going from DevOps to MLOps.

The need for taking care of individual servers was replaced by a set of practices where traditional “ops” work was combined with more recognizable coding style activities, and Infastructure as Code. The next step is going to be wrangling the brave new world of Machine Learning. Let’s see what that means.

### Data Engineering, Data Science and ML Engineering

To set some context, there’s a handful of disciplines that have sprung up over the last few years which I believe ML Ops serves to support. Each are slightly different, so I think it’s worth going over them and how they relate to ML Ops.

*Data Engineering* is more focused around the mechanics of moving data between systems, as well as being able to access data “efficiently”, which can depend on the use case. Because large amounts of data are required for ML training, data engineering is integral to getting started, be it some form of [ETL on a large set of relational data](https://www.databricks.com/discover/etl), or [web scraping](https://oxylabs.io/blog/web-scraping-for-machine-learning); these datasets are the inputs to our ML models.

*Data Science* is more of an umbrella term, but in my experience, the folks that work within it are part of the theoretical and prototypical phase of Machine Learning development. This means figuring out the difficult math problems and [writing papers](https://datascience.codata.org/), as well as producing cutting edge models. A lot of the tradeoffs with data science usually come at the cost of “production readiness”, i.e., their work can’t always just be put into a container and shipped to production.

*Machine Learning (ML) Engineering* is the step after data engineering and data science have run their course. This is where the MLOps piece comes into play, as well as any other software aspect that goes beyond what a Data Scientist or Data Engineer have created. This can include things like:

- Securing production-grade hardware to run models
- Building and pushing containers for a model and/or agentic system
- Managing autoscaling and rate limiting for requests
- Monitoring/observing ML systems

### What Makes MLOps Different

Some of the pieces listed above for MLOps/MLEngineering sound pretty similar to DevOps, but there are differences that are worth considering.

**The Hardware is a Pain to Work With**

Nvidia is making all the money, but if you’ve ever had to get `tensorflow` or `pytorch` working for the first time, you’ll probably run into some very strange C++ errors and driver incompatibilities. If you want to run these services in a Kubernetes setup, you’ll also find you need to install these extra bits like the [device plugin](https://github.com/NVIDIA/k8s-device-plugin) or the [GPU operator](https://github.com/NVIDIA/gpu-operator).

These parts are annoying, but not nearly as troublesome as getting access to the raw machines.

In my experience, certain instance types are extremely difficult to come by on AWS/GCP/Azure. I’m talking about hardware nodes that have the larger Nvidia GPUs attached to them, like one or more [A100s](https://www.nvidia.com/en-us/data-center/a100/) (80 GB of GPU memory). Some of these nodes are so hard to get that you’ll run into “[we’re sorry we’re out of this node type in this region](https://www.reddit.com/r/aws/comments/12defor/anyone_else_fighting_with_constant_lack_of_vms_in/)”, even if you have quota marked out for it.

And why do we need these enormous, outrageously expensive pieces of hardware? Is it to help Nvidia’s stock price? No it’s because —

**Models are BIG**

If you try to run certain models, like Llama3, or a decent size Mistral model, you’ll need at least an A10 GPU (24GB) to fit the model into memory. And this also comes with ~15GB worth of weights. And these aren’t even the largest OS models that can be run.

So being heavy on disk, and heavy on GPU memory, slinging these models around becomes a two pronged problem.

The GPU size means you have to acquire the aforementioned difficult and expensive hardware, and figure out a scaling strategy if you don’t want to burn cash keeping these instances running.

But the disk size means that scaling up and down is not just “pull down the weights on a new node,” since even with decent internet speed it can still be on the order of minutes. That means things like [pre-pulling images](https://betterprogramming.pub/eks-node-autoscaling-with-large-container-images-and-a-warm-pool-a-tragedy-in-three-parts-ed3400995ce0) or reusing instances to get the speed you need.

And beyond being large on two dimensions, there’s another concept we have to deal with —

**Models are a Licensing/Privacy Nightmare**

Models require the data mentioned above, slurped up and provided by Data Engineers and Data Scientists. That means that, if you take a model and use it, the inferences it generates are in some way informed by that training data.

This leads to a pretty confusing set of licenses that are associated with the OS models, and a more confusing set of terms of use for closed sourced models (like ChatGPT).

One does not simply grab Llama 3.1 and throw it into your system and call it good; [you have to clearly designate that you’re using it,](https://llama.meta.com/llama3_1/license/#:~:text=prominently%20display%20%E2%80%9CBuilt%20with%20Llama%E2%80%9D%20on%20a%20related%20website) otherwise you could be in some legal trouble.

The last bit, especially if you’re creating custom or fine tuned models, is how to answer the privacy question. There are a handful of options, including [synthetic data](https://medium.com/@mauryaanoop3/synthetic-data-generation-using-gretel-a-comprehensive-guide-part-1-aebbba06a7eb) or [de-identification](https://www.umassmed.edu/it/security/research-and-clinical-data-access/data-de-identification/#:~:text=De%2Didentification%20is%20a%20tool,and%20share%20with%20other%20organizations.), but privacy is a hot button topic, especially as governments ramp up on data protections.

Moving away from the model madness, there’s also the tooling that supports them.

**The Tooling is Bleeding Edge… and Not Always Great**

One funny anecdote who I got from a coworker, a true MLOps whiz, is how crummy a library he was using to work with these LLMs were. Something to the effect of “an enormous pile of if statements” were what he ended up scanning through.

Part of the difficulty with a lot of the ML space is, because things are new/ prototyped, the code is not nearly as battle tested as a more mature OS project.

But what makes this space so full of opportunity is that even getting something have decent produced in the ML world means getting your hands dirty with the tooling (yes, my coworker had to make at least one contribution to the upstream repository).

### What Skills MLOps Engineers Need

So with the list of differences above, there comes the standard things that all DevOps folks should carry with them, i.e.

- [SRE best practices](https://mckornfield.medium.com/explain-like-im-5-sre-c3aa483e8dae) (avoiding toil + automating)
- Observability strategies
- CloudOps Excellence
- Some Python/Go skills (or \*gasp\* Java)
- Infrastructure As Code skills

Beyond that though, MLOps folks need to familiarize themselves with all the weirdness that comes with LLMs and the hardware they run on. A few that jump to mind:

- Some AI basics, like [this free course from the University of Helsinki](https://www.elementsofai.com/)
- An understanding of the different hardware options (GPUs, TPUs, and even good ol’ CPU) for running models, and how we can (or can’t) observe them
- Understanding some of the libraries that help wrangle LLMs in an agentic system, like [langchain](https://python.langchain.com/v0.1/docs/modules/agents/)
- Knowing what drivers/ libraries exist to run and train models, like [pytorch](https://pytorch.org/) or [tensorflow](https://www.tensorflow.org/)
- Understanding the various LLM offerings (token based or self hosting), as well as the OS or weirdly-licensed-but-still-available models
- Understanding inference LLM based services, like [vllm](https://github.com/vllm-project/vllm) or [tgi](https://huggingface.co/docs/text-generation-inference/en/index)
- Seeing how models are shared, like [Huggingface](https://huggingface.co/)

### Looking Forward

As more and more companies try to onboard AI, the DevOps engineers will quickly find themselves in the weeds of slinging models around, transforming themselves into MLOps engineers. Taking the expertise we have with regular CPU driven workloads, it’ll be interesting.

Stay tuned for more tips, I plan to follow up with an article on how to avoid an “MLOops”, from my own personal experiences.
