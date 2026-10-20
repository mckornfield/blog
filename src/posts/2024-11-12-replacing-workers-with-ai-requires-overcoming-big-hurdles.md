---
title: "Replacing Workers with AI Requires Overcoming Big Hurdles"
subtitle: "“Automating Yourself Out of a Job”"
date: 2024-11-12
medium_url: "https://medium.com/@mckornfield/replacing-workers-with-ai-requires-overcoming-big-hurdles-2c5ca8890871"
---

![Photo by Andy Kelly on Unsplash](/img/replacing-workers-with-ai-requires-overcoming-big-hurdles/0_YG3EHxsyLmZ8F--N.jpg)

*Photo by [Andy Kelly](https://unsplash.com/@askkell?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### “Automating Yourself Out of a Job”

There’s an idea that [all sorts of white collar labor will simply be automated](https://www.youtube.com/watch?v=7Pq-S557XQU), from software engineering to lawyers to doctors. The idea is these professions will simply create/train the AI systems that will come to replace them.

Part of the argument against this is that “no one will have jobs” and “what will we do with our time?” There are some dystopic and utopic responses to this (“no more people!” or “we will be able to do whatever we want!”), but I think the premise is flawed.

I remember at one point my old boss (who was all in on AI before ChatGPT) remarked that he was looking forward to the day where he could just use intelligent systems instead of software developers to write code. But the writing code I don’t think is the part where software developers earn their pay, and I’ll detail what they are.

The three hurdles that this premise of “automating yourself out of a job” fail to climb are:

- Accountability
- Judgment
- Legacy

I think AI has no answer or produces more problems within each of these categories. Let’s cover each in kind.

### Accountability

The only self driving cars that I know of that operate are the Waymo vehicles in select cities in American west and southwest. They are completely driverless, but operate in very specific areas, and under specific conditions.

But what happens when things go wrong? [People get involved](https://support.google.com/waymo/answer/9449023?hl=en#:~:text=For%20riders,team%20and%20contact%20emergency%20services.). If you look up and down the autonomous systems that exist in the world, you will find that the fallback is always people.

Accountability can take many forms as well. In the software world, there are tools like Continuous Integration (CI) that run tests and builds off of individual changes. It’s easy to see who’s ultimately *responsible* for a set of changes (using git blame/version control tools), but the accountability lies with the developers who make changes to and run these code changes. CI acts as an accountability tool, as well as other monitoring mechanisms.

If something is failing, it’s either an indication that code isn’t working as it’s supposed to, or the system itself is fragile. Fixing broken things is not something I’ve ever seen an AI system do, only a person (or persons). If AI is to be “in charge” of various things, they will also become accountable to when those things go wrong (or if we’re still relying on people, then whoever controls the AI will be accountable).

Autonomous systems are by design, not systems that work in isolation. They have to have a fallback to *people*, who can do something about issues that the system doesn’t understand (unknowns), or that fall outside normal function (failures). These systems end up using people as [the “moral crumple zones”](https://estsjournal.org/index.php/ests/article/view/260).

Ultimately, systems and tools aren’t accountable, but people *are*. Until we can shift accountability to an AI system or entity, we’ll still have to have humans in the loop.

### Judgment

Can an LLM judge? In a sense, [yes](https://www.iguazio.com/glossary/llm-as-a-judge/), but in another sense, no. They can provide judgments when given specific parameters (e.g., LLM as a judge), but the judgments that they produce are ultimately not ones that will be admissible in court, at least not yet.

Judgment is a powerful tool, probably one of the most powerful that human beings possess (well… ideally possess).

Judgment stops you from going too fast on the road ([or in its absence, doesn’t](https://www.iihs.org/topics/speed)). It also enables you to decide if something is “good” or “good enough.” There are moral judgments, legal judgments, biases, etc., all of which make up a human’s ability to make decisions.

A core problem with an LLM or any state-of-the-art AI model is that its judgment is either by design (i.e., it follows an algorithmic set of instructions) or it is something emergent (i.e., there is a general corpus of knowledge it pulls from that it uses to form its judgment). The former is rote, and so can’t handle new cases very well, but the latter is much harder to decide if its judgment is “worthy.”

Part of what makes someone an experienced person/expert in their field is that their judgment grows in their area of expertise. They’re able to sort the wheat from the chaff, based on experience and mapping multiple levels of judgment down to a “this is good” or “this is bad.” [In the case of pseudo experts, their judgment is ultimately flawed.](https://www.theguardian.com/lifeandstyle/2013/jun/23/wine-tasting-junk-science-analysis)

AI systems are trained on data generated by, among other things, experts. So if we replace the experts, who created the rules of judgment, with artificial systems, then the next set of judgments will be completely artificial.

This is something that is conceivably possible, but I doubt humans will easily trust legal, medical, or other forms of expertise that come purely from artificial intelligence and have no human involvement.

There’s a big leap between “this judgment is based on an AI model trained on expert doctors” and “this judgment is based on an AI model trained on other AI doctor model’s findings.” I don’t think it’s one taken lightly, and one that has consequence of going off the rails ([botshit/hallucinations](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4678265#:~:text=Generative%20chatbots%20do%20this%20work,what%20we%20call%20%27botshit%27.)).

The other side of judgment is trust. If your judgment is untrusted, then it is ultimately worthless, especially if you are acting in the capacity of an expert. [If our trust in these AI systems is low](https://kpmg.com/xx/en/our-insights/ai-and-technology/trust-in-artificial-intelligence.html#accordion-797cc1e444-item-0d719072c9), then ultimately our trust in their judgments will be commensurately low.

### Legacy

The term “legacy” generally means “old” in the realm of software, but for this legacy, I mean “a chain of connected people.”

People are made by other people. Women grow us in their bodies, feed us with their bodies, and women and (hopefully also) men teach us how to be people. We think this stops when we’re 18, or ~20, but this learning and teaching happens until we die. There are always new pieces of information and things to learn, and new things for us to teach.

Replacing a workforce with AI breaks this chain of learning/teaching. If the people running society were trained by other people, and they employ an army of AI as the next “generation” of workers, then who will eventually run these organizations?

If the idea is that these people will pass on their orgs to a shrinking elite, it seems laughable that people, completely untrained by the rigors of *doing* the work, will be able to command an AI workforce. It might be doable with proper tracking, but will probably be increasingly divorced from reality.

If instead, we assume that the AI systems will eventually “self govern”, and that all of our jobs will be replaced, up to CEO and chairman, then what world are we seeking to build? One where humans can go “do art” while AI have all the boring jobs? I doubt this world will exist coherently for very long.

Using AI as a replacement for people means replacing our normal mechanisms of building and training a workforce. In that way, it would break a pretty fundamental cycle: how the next generation replaces the previous. We’ll either need to rethink/recreate our systems for educating people, or accept that the status quo is the only way to move someone from a child to an adult.

### Summary

The AI workforce coming for our jobs has some major hurdles to cross; namely that it is not accountable on its own, that its judgments will be untrusted, and that it will break the normal mechanism by which legacies are created.

I wouldn’t say that our livelihoods are safe, but I think attempting to replace people will, for the most part, not work.

## Cubed

*Thank you for being a part of the community! Before you go:*

- Be sure to **clap** and **follow** the writer ️👏**️️**
- Follow us: [**X**](https://twitter.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
- [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
- Visit our platforms: [**CoFeed**](https://cofeed.app/) | [**In Plain English**](https://plainenglish.io/) | [**Venture**](https://venturemagazine.net/) | [**Cubed**](https://cubed.run/)
