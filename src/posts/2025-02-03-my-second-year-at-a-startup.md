---
title: "My Second Year at a Startup"
date: 2025-02-03
medium_url: "https://medium.com/@mckornfield/my-second-year-at-a-startup-6286b4fb53ff"
---

It’s been over *two* years? Jeez

![AMD, what, not Nvidia? (Photo by the Author)](/img/my-second-year-at-a-startup/1_B_25J_H4MY4XlkaYYO1F5Q.jpeg.jpg)

*AMD, what, not Nvidia? (Photo by the Author)*

### A Rush, but also, a Lifetime

This last year at my job I got to work with a whole set of technologies that I didn’t know much about beforehand:

- [TGI](https://huggingface.co/docs/text-generation-inference/en/index) (Text Generation Interface)
- [vLLM](https://github.com/vllm-project/vllm) (Another thing like TGI)
- [Azure’s Model as a Service](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-models-as-a-service-maas) (MaaS)
- [Azure Open AI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

Basically an AI word salad. I’ve got to get more breadth than I would elsewhere, but also a better understanding of the game that startups are engaged in around the shifting AI landscape. Let me explain.

### Large AI Companies Benefit from Economies of Scale

To rent a single GPU that can run a decent size LLM from Amazon is about $1 an hour on-demand. But for the GPUs that can perform training or run the largest models, it’s more like [$30 an hour](https://aws.amazon.com/ec2/instance-types/p4/), and they’re not really available unless you’re willing to commit to yearly pricing.

Azure and GCP have similar pricing and scarcity issues around these instances.

As a startup, running even a small number of these expensive GPU instances can quickly rack up massive costs that dwarf running the rest of your infrastructure.

But cloud computing companies (Microsoft, Amazon or Google) or the newer AI companies (Mistral, OpenAI and Deepseek) don’t have these same cost issues; when they host an LLM, it’s not in the ones or tens, but hundreds or thousands (or more).

They do it for good reason: if you make a request to ChatGPT, you don’t want to have to wait for OpenAI to spin up more compute; they need these GPU instances ready and waiting (and in my experience, even in a well optimized, pre-cached setup, scaling up and down LLMs is not fast).

The other side of these economies of scale is that, the *variety* is rather limited, i.e., while there are many different kinds of LLMs and SLMs making their way to the market, you can’t just hit a Bedrock or Azure MaaS endpoint for any of the slightly less popular ones, you have to stand them up yourself (and of course, pay the compute cost).

We’re learning that it’s difficult to get variety without paying for it, so it becomes a major consideration in our new business model, which comes to —

### Big Companies are Beholden to Cash, Startups Chase Future Dollars

![The World’s Richest Chip Maker, but also a pillow (Photo by the Author)](/img/my-second-year-at-a-startup/1__Yoa93XCGjEG4q8conc57g.jpeg.jpg)

*The World’s Richest Chip Maker, but also a pillow (Photo by the Author)*

Where I work (and at most startups, I’d imagine), our goal is *future* customers that help us build out a better product.

We’re not trying to squeeze who we have like companies that have total market control (ala the [Magnificent Seven](https://www.investopedia.com/magnificent-seven-stocks-8402262)), because we’re not living and dying by shareholder value or company supremacy. We’re still carving our path, which I think is ultimately a good thing: it makes our line of work that much more interesting.

Nvidia has enough money to sponsor a whole section of Microsoft Build and throw their names on pillows, but our company got timeshare at one booth there.

Many people I talked with there mistook my startup’s logo for [another company’s that looks suspiciously similar](https://www.investopedia.com/magnificent-seven-stocks-8402262) (*blurple* is very in).

At the same time, it’s pretty sweet to be able to engage with such a cutting edge community and other startups, vs. counting dollars selling another business SaaS product. In short: it’s fun.

I wrote about the difference between big companies and startups [the last time](https://www.investopedia.com/magnificent-seven-stocks-8402262), but there’s no difference this year than last year (in fact, there might be *more* concentration at the top*).*

We’re still trying to build something that will capture value in the future, not upsell our current clients.

We have to build the road before we can drive on it. That means understanding how we can get the variety we need without burning money to run the system. That brings me to —

### AI Systems + Cheaper LLMs are important, Not Smarter LLMs

A big pivot at our company over the last few years has been leaning more into using Generative AI to power our products, but understanding that it has limitations. We worked on releasing products to the Azure MaaS and AWS Bedrock marketplaces that are a bit more than an LLM, i.e., an “AI system.”

If you’ve never heard the term, it describes a system where LLMs are used as components, but aren’t relied upon directly. This isn’t just because of things like hallucinations, but because we need to return structured formats that meet user specifications, and we want to prompt the LLMs for the user to do so.

As different LLMs might be better poised to solve different problems; instead of running one LLM with a huge amount of parameters, it might be more economical to run [a suite of LLMs](https://www.investopedia.com/magnificent-seven-stocks-8402262), each with their own expertise, and utilizing them as part of a compound AI system.

[The DeepSeek reveal](https://www.cbsnews.com/news/what-is-deepseek-ai-china-stock-nvidia-nvda-asml/) from this last week reaffirms another important axis, which is instead of pursuing smarter (and therefore, more expensive) LLMs, is there a path to achieve the same result with a cheaper to produce and cheaper to run LLM? DeepSeek seems to think so, and part of I think any disrupter’s goal should be to challenge the supremacy of the Mag7 to control the AI narrative of “bigger (i.e., more expensive) and better” LLMs.

### To Summarize

The AI/LLM/MLOps space is evolving so quickly that I’m sure my knowledge will be obsolete in a manner of months or years. Our company still has to build its road to drive on, but I have faith we’ll get something decent together. And I think we have the right idea on what path to go down.

Thanks for reading!

## Thank you for being a part of the community

*Before you go:*

- Be sure to **clap** and **follow** the writer ️👏**️️**
- Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
- [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
- [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
- [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
- For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)
