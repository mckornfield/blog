---
title: "Who Gets Rich in the AI Gold Rush?"
date: 2024-03-01
medium_url: "https://medium.com/@mckornfield/who-gets-rich-in-the-ai-gold-rush-aab25e92e93e"
---

The people who find the gold, or those who help find it?

![Photo by Wisely Woven on Unsplash](/img/who-gets-rich-in-the-ai-gold-rush/1_zC-kZcktBMqQh9aDH9YL_Q_2x.jpeg.jpg)

*Photo by Wisely Woven on Unsplash*

## The 1848–52 California Gold Rush

In the mid 1800s, news of untold riches drew hundreds of thousands of people to California. [2 billion dollars worth of gold was extracted, but few prospectors made anything](https://www.britannica.com/topic/California-Gold-Rush).

The more reliable source of income was [selling tools to prospectors](https://www.mtroyal.ca/ProgramsCourses/FacultiesSchoolsCentres/Business/Institutes/InstituteInnovationEntrepreneurship/Blog/IIE_BLOG_GOLDRUSH.htm#:~:text=The%20strategy%20is%20rooted%20in,mining%20tools%20%2D%20picks%20and%20shovels.). No matter who you were, if you were coming to find gold, you needed picks, shovels and all sorts of other tools.

The latest California gold rush is more of a *silicon* rush, in particular, to the untold riches promised by Artificial Intelligence. Just like with the 1840s gold rush, plenty of AI prospectors will turn up empty handed.

The more sensible investments might not be in AI directly, but in the vendors of tools that are arming AI prospectors.

Let’s go over them, shall we?

## The Shovels

The “gold” of AI is probably not a tangible thing, like a version of ChatGPT, but a product that you can sell and market. To unearth that product, you’ll need to train and run it somewhere. At a basic level, you’ll need —

### Hardware: Nvidia GPUs mostly

To run a production grade machine learning model, you need to train it and be able to “infer” from inputs (generally text) and produce outputs. Our own brains can do these sorts of things using neurons, using chemical pathways to retrieve and dispense insight.

[Computer Neural Networks are over 80 years old conceptually](https://libguides.aurora.edu/ChatGPT/History-of-AI-and-Neural-Networks#:~:text=The%20first%20step%20toward%20artificial,neurons%20might%20work%20%5B1%5D.), but the tooling necessary to power Deep Learning in a meaningful way has only become available within the last 10 years. And only within the last couple years was [it enough to captivate the world](https://www.reuters.com/technology/chatgpt-sets-record-fastest-growing-user-base-analyst-note-2023-02-01/).

Nvidia’s stock price is probably the best indicator of the takeoff of AI shovels. ChatGPT was demoed right around the end of November 2022.

![Via Apple Stocks (from Yahoo Finance)](/img/who-gets-rich-in-the-ai-gold-rush/1_0hZidzoblcLFX0iU_WYVtQ.png.png)

*Via Apple Stocks (from Yahoo Finance)*

Nvidia is one of really only two companies that can make commercial grade Graphics Cards powerful enough to run AI model training and inference (the other being AMD).

The reality is that Nvidia is many steps ahead of AMD when it comes to being thedefacto chip for running AI models. Top ML training tools like Tensorflow or Pytorch are both built around supporting CUDA (i.e. Nvidia) libraries and tooling, because Nvidia is so dominant. Nvidia’s estimated market share was [70% of the AI market and 92% of data center GPUs](https://www.investing.com/analysis/amd-vs-nvidia-in-2024-which-ai-stock-makes-more-sense-for-your-portfolio-200645798#:~:text=Market%20Share%3A%20Nvidia%20vs%20AMD&text=Market%20research%20firms%20Gartner%20%28NYSE,AMD%27s%20share%20is%20only%203%25.).

Data center GPUs… that brings me to my next point. Where can you rent these $10,000 chips?

### Cloud Compute

**Microsoft**, Apple, Saudi Aramco, Nvidia, **Amazon, Alphabet (Google)**.

[These are the top companies by market capitalization currently](https://companiesmarketcap.com/). They also overlap very strongly with companies that offer cloud compute services.

This list contains one energy company (how are all these servers getting shipped around, right?), our previously mentioned #1 AI chip manufacturer, and four other companies that are essentially the worlds largest cloud providers (OK 3, Apple’s cloud is more for Apple devices than general purpose compute needs… [we all know Apple’s money comes from iPhones](https://fourweekmba.com/apple-revenue-breakdown/)).

Microsoft, Amazon, and Google offer out of the box model training tools (AzureML, Sagemaker and VertexAI respectively), as well as the use of Nvidia’s GPUs on a per hour basis. It can run the gambit for about a dollar an hour to hundreds of dollars an hour for the pricier GPUs.

Running your own datacenter is silly in this day and age. For example: you can buy your own [Nvidia A10 GPU for $12,000](https://www.cdw.com/product/nvidia-a10-gpu-computing-processor-a10-24-gb/7261572), or rent it from [AWS for $1 an hour](https://instances.vantage.sh/aws/ec2/g5.xlarge). You’d have to run that GPU for *500 days straight* to make it equivalent to the AWS cost (and that’s not including power or maintenance).

The big cloud providers make it seem like a no brainer to rent shovels instead of busting out a ton of cash to purchase your own.

Now that we’ve settled on our shovels, let’s review the other side of our analogy, the picks.

## The Picks

If the shovels just let you move dirt around, the picks are going to be the tools that let you get the sort of details you need for your AI product to be *useful.* Let’s start with the most obvious one —

### Data, Real and Synthetic

AI is data hungry. ChatGPT’s first iteration was trained on [300 billion words](https://www.businessinsider.com/google-researchers-openai-chatgpt-to-reveal-its-training-data-study-2023-12#:~:text=The%20AI%20model%20powering%20ChatGPT,or%20570%20GB%2C%20of%20data.) or about half a TB of data. If you want useful insights, you’ll need a lot of data. The same can be said for AI tools that generate images ([DALL-E reportedly was trained on 12 million images](https://techdayhq.com/blog/2023/08/15/the-dall-e-ai#:~:text=Enter%20DALL%2DE%2C%20an%20AI,re%20all%20over%20the%20place.)).

Besides volume, the other important aspect to data is *quality*. Ensuring data is high quality involves a bunch of data science that I’m no expert on, but data can be quantified in various ways.

There are time series data, text data, tabular data, unstructured data and all sorts of PII/Health data that companies and governments would love to have access to, in order to train their models.

The problem with data access is that, in the wake of models trained on scraped data like ChatGPT, [sites are doing their best to protect themselves from being mined for data and losing all their traffic](https://www.reddit.com/r/ChatGPT/comments/15ju114/chatgpt_is_putting_stack_overflow_out_of_business/). The other side of data is *privacy,* which laws like [GDPR](https://gdpr.eu/what-is-gdpr/) are doing their best to make it difficult for companies and governments to access individuals’ data.

These two things leave our AI prospectors in a difficult spot. Either they have to pay or find some way (breaking the law?) to gather the data they need for their hungry models, OR, in an effort to double down on Machine Learning, we can use models trained on data to [produce *synthetic* data](https://moez-62905.medium.com/synthetic-data-is-the-future-of-artificial-intelligence-6fcfd2ce1a14) that we use to train other models; these models can also generate data that is [provably private](https://gretel.ai/blog/differentially-private-synthetic-text-generation-at-scale-part-1), meaning we’re not breaking any laws but are still able to get insights from the original dataset, passed through the sieve of a differentially private model.

Any company that can offer data, real or synthetic, for the right price, will have their own part of the AI gold rush carved out, especially as fences are going up around people’s data.

All that said, even if we have data, and GPUs to run our training on, what are we supposed to do?

### Experienced ML Engineers

While we might consider these folks “pick wielders” in one sense, ML engineers’ focus will be more on solving engineering problems than on what business problems need to be solved.

ML Engineering is so new that finding folks that are experienced in this field might mean we lean more heavily on academics than traditional software engineers. All of the folks I know that have strong Machine Learning backgrounds have at least a Masters, if not a PhD in the field.

The libraries/algorithms they have to use (Transformers, PyTorch, Tensorflow, Stable Diffusion) are not only painful to get started with, but require a good amount of rigor to get anything useful out of them. If you want to have an AI model that does something better than an off the shelf Llama 2 or ChatGPT, you’ll need people who can wield (or be?) the picks for your gold rush.

And because there are so few folks that have the expertise necessary, the ones that can fill the [roles well will be handsomely rewarded](https://www.indeed.com/career/machine-learning-engineer/salaries).

### In Closing

I don’t know what gold there might (or might not!) be at the end of the AI rainbow, but GPUs, Compute, Data and ML Engineers will be integral to reaching the end.
