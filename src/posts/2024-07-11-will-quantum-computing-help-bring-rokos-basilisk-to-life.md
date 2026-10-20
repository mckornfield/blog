---
title: "Will Quantum Computing Help Bring Roko’s Basilisk to Life?"
date: 2024-07-11
medium_url: "https://medium.com/@mckornfield/will-quantum-computing-help-bring-rokos-basilisk-to-life-41d45da7e2c0"
---

And is there anything we can do to prepare for it?

![Photo by Olli Hackenberg on Unsplash](/img/will-quantum-computing-help-bring-rokos-basilisk-to-life/0_tTWcG7EdInrxbyzj.jpg)

*Photo by [Olli Hackenberg](https://unsplash.com/@hckbrg?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

This analogy is a bit of a stretch, so I’ll lay out some ground work. Be warned, if you believe that knowledge in itself is dangerous, you might want to skip the first section, and just know that some guy Roko pissed some people off online

### Who is Roko? And Why Does He Have a Pet Basilisk?

[A forum post in 2010 by a user Roko](https://web.archive.org/web/20221022172820/https://basilisk.neocities.org/) argued that a superintelligent AI would punish those who tried to stop it from coming into existence.

> So a post-singularity world may be a world of fun and plenty for the people who are currently ignoring the problem, whilst being a living hell for a significant fraction of current existential risk reducers (say, the least generous half).

The people who are trying to stop the SIAI (super intelligent AI) from existing are are the “existential risk reducers.”

To put this in more plain terms, imagine if you were working with a peer and treated them poorly, maybe because they were incompetent or maybe because you’re not a nice person (hey, no judgments in this hypothetical).

You do your best to sabotage this person’s promotion, giving them horrible peer feedback reviews and doing everything you can to stop them from climbing the company ranks.

Now imagine that your peer steps up to be your boss, despite your best efforts. They could get revenge in a manner of ways:

- Getting you fired
- Giving you crummy work
- Making your job as hellish as he can.

In short, they would “torture” you.

There is a reference in the post to [“Langford’s Basilisk”](https://en.wikipedia.org/wiki/BLIT_%28short_story%29), which is a short story about images that, upon viewing, cause human beings to die (similar to how a [basilisk kills you with a look](https://en.wikipedia.org/wiki/Basilisk)).

So the basilisk aspect is the fact that, if you understand the theory in the article, you are now privy to something that a super intelligent AI could punish you for. Darn.

### And What Does that Have to Do With Quantum Computing?

![An enigma machine.](/img/will-quantum-computing-help-bring-rokos-basilisk-to-life/0_t_SeDpQ_x01Msm__.jpg.jpg)

*An enigma machine.*

Modern cryptography relies on functions that work easily one way, but are hard to solve the other direction. [RSA being one of the most common](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29), relies on rely large prime numbers and their factors.

*tl;dr* Complicated math is what keeps software systems safe from attackers and spooks.

*BUT* only safe for so long.

As an example, take the **Enigma machine**, the German encryption machine used in World War II. It was famously broken (well, famous after the fact, not at the time), by [a set of codebreakers at Bletchley Park](https://bletchleypark.org.uk/).

By “broken”, we mean to say that all communications that this machine distributed could be decrypted, assuming they were intercepted, i.e., anyone with the code-breaking technology could decrypt these messages.

The tool that broke the code the Enigma machine was “the Bombe”, an ancestor of the modern computer, but a state of the art machine at the time.

So in our modern times, a Quantum Computer will be “the Bombe” to all of our end to end encrypted chats (think Signal, Texts, Emails, Whatsapp, etc.)

Hopefully now we have the pieces to get back to —

### Roko’s Quantum Computer

Imagine you are an aspiring despot, maybe one running for president in 2024 (ahem).

Anyway, politics aside, let’s imagine you come into power at a time when top scientists have finally gotten a quantum computer to break the most sophisticated state-of-the-art encryption.

There are all sorts of things you could do with this device, now that you can put your ear to many closed channels, but for our focus, you could find all of your *detractors*.

I don’t mean people who post publicly on Twitter about how much they hate you (those people you can find right now), but this could be anyone who shared private messages about how much they dislike you.

If you hadn’t already, [you could start saving up a large amount of internet traffic and not telling anyone](https://en.wikipedia.org/wiki/Harvest_now,_decrypt_later), feeding the results of quantum computer driven decryption into a system that identifies all of your *detractors* and gives you a list of people to sideline in your quest to root out all opponents.

To name some of the larger governments most capable of developing this tech: China, Russia, even a despotic USA, could all benefit from this codebreaker, and those most harmed would be anyone who spoke out against their leaders, even in private fora. It could be something that puts folks in [labor camps](https://www.state.gov/wp-content/uploads/2019/03/Prisons-of-North-Korea-English.pdf) or simply [messes with their social credit score](https://www.technologyreview.com/2022/11/22/1063605/china-announced-a-new-social-credit-law-what-does-it-mean/).

### How to Save Ourselves From Retribution from Our (Possible) Future Evil Overlords

This is unfortunately advice that a good person who doesn’t want retribution could avoid as well as a bad person, but I think it’s worth talking through (I guess this is like an anti-basilisk? Bad if the bad person sees it because it helps them?)

If you don’t want the information you send to be decrypted by a quantum computer, you either need to:

1. Go retro
2. Go more futuristic

**Go Retro**

What tools can’t a quantum computer break? How about

- paper records that you burn after reading
- carrier pigeon messages
- latte foam art?

Some of these are in jest… but more seriously, messages that don’t pass through the normal sieve of intelligence won’t be ones that can be archived and decrypted later on. Sometimes the best form of security is to not play the game.

If you are totally out of cereal box ciphers though, maybe you want to —

**Go More Futuristic**

The state of the art will be [“Post Quantum Cryptograpy” or PQC](https://en.wikipedia.org/wiki/Post-quantum_cryptography#:~:text=isogeny%2Dbased%20constructions.-,Symmetric%20key%20quantum%20resistance,attack%20by%20a%20quantum%20computer.). The day that these algorithms will become necessary is known as Y2Q, or Q-Day.

Some of the algorithms we use (Public Key Algorithms, like our friend above, RSA) will be totally bunk in the face of Quantum Cryptography, whereas other algorithms will just require larger factors to be secure.

Most of this cryptographic information is even fancier math than what we have, and not something within the reach of a layperson to just “update” their computer. But supporting [NIST](https://csrc.nist.gov/projects/post-quantum-cryptography) and any open source projects that purport to save us from Y2Q and its negative outcomes are the best ways we can go futuristic.

### Maybe Quantum Computing is Just One of Roko’s Basilisk’s Tools?

To bring it full circle, imagine that the government (or “entity” if we’re including companies/extragovernmental organizations) employees an AI or AI system along with its Quantum Computer to sift through the decrypted data.

One would imagine just based on the volume of data, its analysis will HAVE to be machine based, in order to find *detractors*. And if that analysis mechanism happens to be done by a super intelligent AI, then it won’t be Putin who’s doling out justice…

Thanks for reading!
