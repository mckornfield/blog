---
title: "“I Need Some Advice on Learning MLOps Practically”"
subtitle: "Well… here’s a few answers"
date: 2026-05-09
medium_url: "https://medium.com/@mckornfield/i-need-some-advice-on-learning-mlops-practically-d12ac98e3eb7"
---

![Photo by Navy Medicine on Unsplash (Not that kind of Ops…)](/img/i-need-some-advice-on-learning-mlops-practically/0_n3u1TYceVuS6fuh3.jpg)

*Photo by [Navy Medicine](https://unsplash.com/@navymedicine?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (Not that kind of Ops…)*

I got a cold DM with those exact words, and I wanted to share the ways I’ve learned and hopefully you can learn as well. (I wrote about this a [few years ago as well](https://levelup.gitconnected.com/the-latest-reinvention-of-the-system-admin-mlops-d73abdbba29b)).

I think there’s two angles to have at it: as a consumer and a producer. You’ll need both to be anything decent in the real world. Let’s begin.

## Consumer

### Learn from the Best

There are really a small cadre of folks that are leading the AI train. It’s good to know who they are and to consume what they put out (as well as question/turn it over). A short list might look like:

- Folks from the top labs (OpenAI, Anthropic, Google)
- Andrej Karpathy (got some very good tweets)
- Steve Yegge (prominent vibe coder)
- Folks who appear on Dwarkesh (and Dwarkesh himself)
- Folks who appear on the Pragmatic Engineer (and Gergely himself)

I consider anyone who’s in the thick of AI research to be worth paying attention to, as well as people who are working on vibe coding tools like Peter Steinberger (Openclaw) or Mario Zechner (Pi).

### Read Read Read

There’s no substitute for learning, and I find reading to be the first pass worth undertaking.

Using AI to learn is a double edged sword. While it can quickly grab and summarize information, I know I have a tendency to skim its contents when I’m in a rush for “nuggets” of information.

In contrast, when I read longer form blogs or books, I find that even though I might scan, I take my time to read and re-read sections I don’t really understand. I think personally if you want to be an MLOps expert, there’s no substitute for reading through some decent texts/blogs on the subject. This one is more of a pointer so take it for what it is hahaha

If you imagine MLOps like a layer cake, there’s some things that are very familiar to System Admins, and then at the outer edges, some pieces that are relatively new to the industry. These might look like:

- Hardware (which GPUs, within which clouds)
- Hosting options (Cloud, on premise)
- Runtimes (Container orchestration, kubernetes, inference/gpu shared environments)
- Model lifecycle management (training, RLHF, SFT, Fine tuning a frontier model, managing weights via Hugging Face)
- Evaluations (model performance, failure conditions, creating evals)

There are some great blogs and books that cover some or all of these. I like “[AI Engineering](https://www.amazon.com/AI-Engineering-Building-Applications-Foundation/dp/1098166302)” by Chip Huyen as a first pass at these, but for the blogs I’d rely on the groups mentioned above, as well as academic papers the labs and universities put out.

For hardware, hosting and runtimes, I think you can use more classic materials, like an AWS/Azure/GCP certification and course.

If you really care about Ops specifically, there are some pretty foundational texts like the [Google SRE book](https://sre.google/) or [the Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0988262592) and [Unicorn Project](https://www.amazon.com/The-Unicorn-Project-Gene-Kim-audiobook/dp/B0812C82T9/ref=sr_1_1?crid=3FM9I1D00AYYJ&dib=eyJ2IjoiMSJ9.0Gj2O6yNzs3pLf8TR-xuVM-WMtlHRrBDcMRx09gFtkLbwlZhEiJa6wtzYhfBjw9Oxpt7izazpfnxyj4DaO1K8OoQQPJ2oP9keKmQhX5LERLFNO6rSP_iqWT-_F9shLskP68n2jWTtXt6spvkqsw3YVyhCZosq464CdA7xcmQgNu_gRJQ3zg5-u4D0cnGNpWJMD5oZQ__yxErKhVUyLnXdpewFBoYfqaWc1WxPEk7ZW8.dJMivVGnzs1xscIRZV45v4T1cCzvLqBXB3GERIezM8M&dib_tag=se&keywords=unicorn+project&qid=1778329415&s=books&sprefix=unicorn+projec%2Cstripbooks%2C133&sr=1-1) (which are novels but convey Ops concepts very well).

All that being said, I think blogs/papers are good ways to stay relevant but the base layer needs to be composed of decent books, which the best are either putting out or will recommend.

### Programming

In this day and age, programming is being swept away by vibe coding/agentic coding. While maybe the future involves no writing of programs, I think it’s folly to think you can cede ALL of your coding knowledge to a machine. I don’t consider myself a very good programmer, but I do think that trying to keep agents from churning out thousands of lines of unreviewed code is good if you want to learn, and instead moving incrementally and having the agents explain what they want to do.

On the flip side, be a “trad coder”, which means doing silly algorithmic puzzles like LeetCode/HackerRank as much as reading books like Clean Code (or reading other books that tell you Clean Code is bunk haha). I think having an opinon on written code will continue to be important, as being able to differentiate “yeah the agent did good” from “yeah that is total slop” is a skill worth having.

A guy I used to work with analogized agentic programming to chainsaws, and I think that’s accurate. While chainsaws have their purpose, often times if I’m changing configuration files, or tweaking existing code (agentic or traditional), I just use NeoVim/Cursor/VSCode. And I think it’s both a benefit in not burning tokens on updating a string or a number AND it lets me see what the frick is going on. Use a screwdriver or a handsaw when it serves you, not a chainsaw.

Another writer brought up a point about “tourism”, if you are using AI to drive your work, you’re not necessarily going to become an “expert” in that field, instead you’ll be a tourist. You have to walk before you can run (or fly?)

### Know the usual suspects

It’s good to know what the below are, you can look them up yourself (and this list is by no means exhaustive)

- Transformers
- Hugging Face
- vLLM
- CUDA
- Pytorch
- Tensorflow (maybe?)
- LangChain
- Weights and Biases

And many, many other ML libraries that might slot into your space.

The main labs (obviously)

- OpenAI -> GPT-x.x
- Anthropic -> Claude
- Google -> Gemini
- Microsoft/GitHub -> the 7 (70) Copilots
- xAI -> Grok

## Producer

All that being said, I think MLOps is a discipline that is as much about *doing* things as it is about learning them. A healthy information diet is a good first step, but no one is going to hire you/give you a shot because you read some books.

### Rule number 1: Solve a real problem

If you have an idea for an AI/ML application, don’t make some “pie in the sky, million users in a month” app that no one knows about. Or if you do get a million users, then don’t take my advice, you already know what you’re doing!

Instead, find a person (maybe it’s yourself!) and solve their problem. My case in point is my very silly workout app. I “trad coded” it back in the day using vanilla JS, but wanted some bulk edit/dark mode features. This workout app just says the name of the exercise and counts down. What I really like about being able to use agentic coding is that it let me churn out those features quickly and solve some problems I had.

If you want to be an MLOps person, deploy something that solve a problem using ML. Another app I worked on was to detect spam from text messages/emails on iOS. It let me get a sense of what the limitations were with the on-device model, as well as consider real cases of spam messages I’d received or my sibling had received.

You can also build something for a place you work at, or if you’re not employed, then doing it as a volunteer effort or for your friends can be a great way to both make something valuable AND employ the skills you’ve been trying to ingest above.

### Rule number 2: Know what you built

If you made something by vibe coding your hours away, it’s going to be hard to demo it authoritatively if you didn’t spend time introspecting the decisions you or the agents made along the way.

If you build something that solves a problem, but you have no idea how it works, you’ll find that people are going to be largely unimpressed. What puts you in the driver’s seat is

### Rule number 3: Keep trying new things, as the industry is shifting a bunch

A year or two ago, AI coding was pretty lame. Tab complete wasn’t all that great except for CRUD apps, and agents effectively didn’t exist (as far as tool calls, MCP, editing files, running BASH). It’s hard to say where things will be in a year or two, but I don’t suspect they’ll be very static. Software and software operations are probably the most likely to be displaced by AI in the short term, mostly because (and this is not to be pejorative) a lot of software is very boring and no one cares what it looks like as long as it works. Don’t ask me how many times I’ve reviewed code this is essentially

```python

```python
@dataclass
class SomeData:
  property_one: str
  property_two: int
def send(data: SomeData):
  …
def receive(data: SomeData):
  …
```

And that at least used a `dataclass`. I’ve seen a lot of `my_dict ={}` and `Map&lt;String,Object>` in my short stint in software.

The point being: keeping up with these tools and their limitations is important, not because you should fear your replacement, but because you should figure out *where you are valuable.* In the MLOps space, that’s going to be by being ready/first in line to try out what researchers and applied scientists have been working on, to see if it’s bunk or the new hotness. And maybe making some contributions or work of your own!

Hopefully those are some good places to get started. If you have better ideas or are interested, in learning something more specific, please reach out!
