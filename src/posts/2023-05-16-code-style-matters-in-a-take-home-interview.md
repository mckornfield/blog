---
title: "Code Style Matters in a Take-Home Interview"
subtitle: "What you produce in a vacuum is reflective of how you build and your level of effort"
date: 2023-05-16
medium_url: "https://medium.com/@mckornfield/why-code-style-matters-in-a-take-home-interview-problem-c53623e4d2a2"
---

![Photo by Valeriia Miller on Unsplash (such stylish, square bags!)](/img/code-style-matters-in-a-take-home-interview/0_vqM-DgjXjtMEI8GM.jpg)

*Photo by [Valeriia Miller](https://unsplash.com/de/@iyamiphotography?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral) (such stylish, square bags!)*

## To Start: Software Engineering Interviews Are Flawed

Let’s get this out of the way to start: probably not just software engineering interviews, but all interviews are in some way flawed.

They can overemphasize unimportant aspects during the job and underemphasize aspects that are very important on the job but might be harder to capture in an interview.

The task is a bit of an impossible one: given a few hours, measure if a candidate will be capable of performing a job for a minimum of 40 hours a week, for 50 weeks a year. You’re supposed to gauge someone’s future performance with what amounts to less than one percent of the time they’d work for you for a year.

The best interviews are like internships, where you can gauge how someone would perform on the job. But not everyone wants an internship (or is offering one).

So, given that these interviews are flawed, are they at all defensible? Yes, we have to try and hire people somehow instead of just inviting friends and family to work for us.

## Take Home Problems

I think take-home problems are much more representative than live coding interviews of the sort of work you’d actually do on the job. I have rarely (or never?) had to code an algorithm from scratch while someone I worked with watched me and filled out a scorecard. Generally, you get some time to figure things out and look things up.

That being said, if you’re given a take-home problem, be careful about everything that you do in the problem, as it will be heavily scrutinized.

- Why did you decide to use a function instead of a lambda?
- Why did you pull in (or not?) a third-party dependency?
- Why is your code style so strange in this part?

That third bullet you might take issue with. “Matt,” you’d say, “why does code style matter? Isn’t that just something you’d fix in a code review?”

Well, let’s talk about code style.

## What is Code Style?

Essentially, it’s how you write a program specific to a language.

As an example, I’ve seen heavy use of lambdas (or “Fat Arrow Functions”) in TypeScript/JavaScript, to the point where if I’m looking at a coding snippet that uses them heavily, I’d assume the developer is pretty familiar with TypeScript.

Conversely, these lambdas are not nearly as common in Python (instead, people usually prefer list/set/dictionary comprehensions or just inline `def`), or are uncommon in languages with preferred styles, like Go.

Where you place your curly braces can be the difference [between a Java developer and a C# developer](https://softwareengineering.stackexchange.com/a/237007). There’s a lot to tell from someone’s code style.

## So, Why Does Code Style Matter for a Take-Home Problem?

### **Code style as a proxy for experience/proficiency**

When I look at someone’s code in a language I know decently well (really just Python or Java), I can usually tell within 5–10 lines whether they’re experienced or not.

In both languages, indications that something off comes in the form of:

- They use \* imports, which is generally not great
- Imports themselves are not organized
- The code is formatted in such a way that an auto-formatter would change a lot of the file
- If I open it in my IDE (IntelliJ for Java or PyCharm/VSCode for Python), I see lots of linter errors
- Print statements instead of logger statements
- (Python specifically) Not using type hints

Some things, especially for a take-home, don’t matter. The way you decide to implement a solution to drive a taxicab or put out fires in a grid doesn’t make a bit of difference in the real world. But how you write your code indicates plenty of things.

Consider the first three bullets I listed. When I look at code like this, it indicates that the person doesn’t use an IDE to its full capabilities. They’re not sorting/ organizing imports or auto-formatting their code, thereby dodging lengthy discussions that might come from code review.

For the linter errors piece, this means either A) you don’t care about linter errors (shame) or B) you aren’t using a tool that reveals them (more shame). IDEs come with them built in, and there are ones you can run on the command line. Not using these tools isn’t a sign of excellence/superiority to me; it’s a sign that you don’t use them.

Print statements vs. logging might be controversial, but I always think that print statements are just for checking if things are working. Logging lets you check things without altering the program, a key advantage. They also show how much the user should care (i.e., error logs vs. debug logs), whereas print statements don’t tell me much.

Type Hints are probably my favorite code style example for Python only: yes, Python doesn’t require types. But that’s part of what stinks about Python; it’s pretty dang hard to know what objects are, even if they’re named super well unless some type information is added on. Using type hints makes the IDE more helpful and helps the reader of the code as well.

### **Code style as a proxy for effort**

Unfortunately, I also see a lack of good code style as a lack of effort. All this information (on how to be more “Pythonic” or more correctly follow the language style) is available online and through linters/tools like the IDE.

If you aren’t using a good code style, it might be because you’re inexperienced (as the above indicates), but it also means you aren’t trying to learn. And in a take-home interview, we don’t have time to code review your question in a feedback-driven way. It’s more like grading a paper, and a professor or teacher sees grammar/ formatting as just as important as the paper's content.

We’re seeing if your submission reflects what an experienced programmer would produce. If we don’t think that your answer reflects that, it’s either

- You don’t have the experience we want
- You aren’t putting the effort out to demonstrate you *do* have that experience

Either way, the reviewer sees confusing/bad code style as an indication that the candidate is not worth the time for the next round of review.

## Summary

Code style matters; although interviewing can be flawed, code style is one of the objective things a reviewer can consider when looking at a submission. Linters can even [give scores](https://pylint.readthedocs.io/en/latest/user_guide/usage/output.html#score-section) based on the code in question, putting a number to what is otherwise a much more subjective assessment (i.e., “Is this good code?”).

Think of it like this: if someone spoke to you in English with an accent so thick that it was hard to understand them, you most likely wouldn’t hire them for a job where communicating in English was one of the most important skills.

Code style fills that space in programming. Very poor code style makes a program hard to understand and annoying for other developers to work with.
