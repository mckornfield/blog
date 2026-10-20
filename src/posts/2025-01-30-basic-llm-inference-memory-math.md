---
title: "Basic LLM Inference Memory Math"
subtitle: "Explaining why these LLMs need so much VRAM"
date: 2025-01-30
medium_url: "https://medium.com/@mckornfield/basic-llm-inference-memory-math-e81a3dfac5e6"
---

Explaining why these LLMs need so much VRAM

![Photo by Andrey Matveev on Unsplash](/img/basic-llm-inference-memory-math/0_tRtAQR0SXqA7NaYS.jpg)

*Photo by [Andrey Matveev](https://unsplash.com/@zelebb?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Download More RAM? Nah, Download More VRAM!

Unfortunately, downloading more RAM won’t save you with Large Language Models, you’ll need GPU RAM (also called VRAM) that can fit them.

If you’re renting them from AWS, Azure, or GCP, you can expect to spend $1 at the minimum *per hour* to rent them. If you want to buy an A10 or higher graphics card, it can set you back ~$3000, and even more for an A100 or H100 GPU.

But wait, why do you need these ultra expensive graphics cards? Can’t you just use your regular graphics card to do some inference?

Well, unfortunately if you want a smarter model, math is not on your side.

### The Math, at a Back of the Envelope Calculation

tl;dr *Multiply the number of params by 2, add another 2 GB for overhead*

Many LLMs if you’ve ever seen them written out come with a number of “parameters” in their name. For example:

- [Mistral-7B](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/blob/main/config.json#L21)
- [Falcon-11B](https://huggingface.co/tiiuae/falcon-11B/blob/main/config.json#L38)
- [Llama-3.1–8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/blob/main/config.json#L34)

While there are [many mechanisms to estimate](https://medium.com/@lmpo/a-guide-to-estimating-vram-for-llms-637a7568d0ea#:~:text=To%20perform%20large%20language%20model,Precision%20%2F%208%29%20%C3%97%201.2.) the memory required, I’m going to give you the back of the envelope one.

The models all above have 16 bytes for each parameter (the links are to the relevant torch config), so we can divide 16 by 8 (8 bits -> 1 byte) to get a factor of “2” for each parameter, converted to bytes.

Tools for hosting these LLMs like TGI and vLLM also require other components to run within the VRAM (CUDA overhead, activations and outputs), but their footprint is tiny, adding only 1–2GB more at the max.

nₚ ⋅ 2 + 2GB

Will give us the VRAM required just to load up the parameters. That’s 16 GB of VRAM for Mistral-7B as an example (yes… multiplying by 2 and adding 2 is not that hard, haha).

![Mistral-7B Inference, Source](/img/basic-llm-inference-memory-math/1_whGTkmqogmVPqBBQJBOoQg.png.png)

*Mistral-7B Inference, [Source](https://vram.asmirnov.xyz/)*

### Training?

It’s a whole ‘nother ball game… I’d recommend the estimators for those, since the parameters are not the whole picture.

It suffices to say that it’s around an order of magnitude more than inference (the estimator for Mistral-7B for example, will show around 80GB at the lowest, and 140GB at the highest).

![Mistral 7B training, lowest cost combination, Source](/img/basic-llm-inference-memory-math/1_wYIbHLJDuNmmyYDwz066_A.png.png)

*Mistral 7B training, lowest cost combination, [Source](https://vram.asmirnov.xyz/)*

### What are Our Options?

The list of [Nvidia GPUs is relatively simple](https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units), at least looking at it from the needs of our LLM VRAM requirements. It comes down to:

- H100 -> 80GB
- A100 -> 40 GB or 80 GB
- L40 -> 48 GB
- A40 -> 48 GB
- A10 -> 24 GB
- L4 -> 24 GB
- T4 -> 16 GB

There are many others in between, and many other differences besides the amount of VRAM, but these are the ones I’ve seen available in Azure/AWS.

You’ll notice that for inference, most of these will work (minus the T4, which is too close even for Mistral), whereas for training, most of them do *not* work.

For the larger training types (like for Mistral to be trained on a 100GB+ instance), I believe multiple GPUs on one node is the only solution.

Also the higher the memory, you can bet the higher the cost.

Thanks for reading!
