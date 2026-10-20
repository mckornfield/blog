---
title: "Bad Monitoring Systems are like Car Alarms"
date: 2023-02-23
medium_url: "https://medium.com/@mckornfield/bad-monitoring-systems-are-like-car-alarms-f1b175ff0aec"
---

At least the boy who cried “wolf” stayed by his sheep

![Photo by Raphael Lopes on Unsplash](/img/bad-monitoring-systems-are-like-car-alarms/0_WSQISMk4lZREJNr-.jpg)

*Photo by [Raphael Lopes](https://unsplash.com/@raph_lopes?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Imagine you’re in your house, and outside the window, someone’s car alarm is going off.

You rush over to the window (oh no someone’s being robbed! grand theft auto!) and you look out at the street. You see a car, with no one around, blinking and sputtering its annoying alarm. You turn away frustrated and go back to whatever you’re doing, possibly putting on headphones to tune it out.

The next time it happens, you maybe look out the window eventually, but once again, no robbers.

Eventually, the car alarms are just annoyances; it turns out that people just don’t park very well and when cars shoot by them, it rocks the car and sets off the alarm.

If someone *actually* were having their car stolen, at this point (many false alarms later) you wouldn’t care. The boy who cried wolf, but with an automated system instead of a bored shepherd. This is in many ways what we could liken to:

### Bad Monitoring Systems

There are really two modes for bad monitoring systems. There’s either:

1. Everything is broken but the monitoring system is silent
2. Nothing is broken but the monitoring system won’t shut up

The first one is bad, but also fairly harmless. You’d almost prefer a monitoring system that tells you nothing to one that sends you a bunch of false positives.

The second option is definitely worse: you’re going to eventually ignore the alerting, even while your stuff is totally broken. It trains you to ignore a system you probably have invested a decent amount of time in.

Software monitoring systems generally send you messages or pages. That means that you are reacting to emails, slack messages, or some sort of page directly to your phone. What makes noisy software monitoring systems like car alarms is that:

1. The person who set up the alerting is not necessarily the person who deals with it (i.e. you at home hear the car alarm, but the person who parked the car is probably off somewhere else)
2. Car alarms are sensitive and noisy, as are noisy software alarms. They produce a lot of false positives and can unnecessarily stress people out.
3. These systems desensitize the listener/receiver, to the point that they wished the alarms didn’t exist/ try to block them out

### How to Remedy a Noisy Monitoring System

There are a handful of techniques, but the most important one is to *treat all alerts as some sort of incident*. That means that if you receive a message, you deal with it as though something is wrong.

What can confuse people is that sometimes, the fact that you received a message *in the first place* is what is wrong. The car alarm went off when it should have stayed silent.

Adjusting your monitoring system to not blast you with unnecessary messages is as important as making it send you messages when things break.

Here are a few other remedies besides treating everything like an incident:

1. Make sure to deduplicate similar alert messages
2. Create tickets for known but not urgent issues, then silence alerts until the ticket is fixed
3. Only send the alarms on some sort of cadence (i.e. every hour, every 15 minutes) if they aren’t urgent

### In Closing

There’s probably no hope for car alarms besides ear plugs, but there’s plenty you can do to make your monitoring system not resemble a set of noisy car alarms. Good luck!
