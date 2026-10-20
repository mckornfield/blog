---
title: "The Time Intensive Parts of Game Development"
subtitle: "It’s not where I thought it was"
date: 2024-02-17
medium_url: "https://medium.com/@mckornfield/the-time-intensive-parts-of-game-development-4ac14debb4b4"
---

![Photo by Duygu Güngör on Unsplash](/img/the-time-intensive-parts-of-game-development/0_DZmpd2VxZFuLP9ku.jpg)

*Photo by [Duygu Güngör](https://unsplash.com/@duygug?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

**Programming is hard, but easily scalable**

Recently I’ve been dabbling in programming with Roblox or Unity. Both have been **fun and doable** with my programming experience, while my friend and nephew have been taking more of the art/design side upfront.

(An aside: the most difficult programming challenges are already solved if a game engine exists. Figuring out how to do complex lighting or physics simulations is the job of the folks that maintain Unreal Engine and the like, but game programmers that work on top of that are operating in a much less complicated space.)

What tends to be the most difficult programming challenge is trying to solve a novel problem you can’t just copy paste from online or watch a tutorial for. But once you have enough tools and know the landscape of the gaming tool/engine, you start to realize that programming is hard but scalable, i.e. the script you use to make one enemy move can just be copied to the next one, or referred to from one place.

There is an immediate reuse element to programming so that it takes an hour or more to make the first enemy move, and then seconds for the next one (a simple copy paste/ import statement).

What I started to realize is the bottleneck quickly becomes what to do about art. Art is a core component of most games, difficult to do well, AND not scalable. Let me explain.

**Animating a 2D character**

Let’s go with a really simple character, say a stick figure that can move in 2D. You think, oh, if we want to move him, we just program his limbs to change direction, right?

Well… if you had to program his individual arm and leg movements, it might look OK, but essentially you’re just using a computer to redraw him, instead of just drawing the character in different poses. It’s probably not going to be any easier to write the code than it is to draw. But think of a basic stick figure, just to move in 2d you need:

1. Animations for walking forward and back
2. Animations for walking up and down (ie towards and away from the camera, if climbing)
3. An idle animation
4. Any attack animations
5. Jumping animations
6. Any animations for getting hurt, dying

All of these essentially are flipbooks of a handful of different poses you compose into a sprite sheet. Then you can stitch them together into an animation.

The difficult part is not just all the sprites you need, but what if you want another stick figure, with different proportions, or different details. You need to now redraw everything or copy the sheet and add to the existing sprite. Either way, time intensive and not scalable.

**Animating a 3D character**

There are lots of tools for making 3D models, but from what I’ve seen, they are extremely time intensive, just to have a grey silhouette of a figure. My friend says it’s three separate skillsets:

- Modeling
- Animating
- Drawing (for textures)

Having to grow those different skillsets is not something I think you can easily pick up in your spare time; you have to give yourself a lot of time getting good at each independently.

And the problem with 3D motion (in my outsiders’ view), is that we have a lot of good examples of what 3D motion/lighting *should* look like (i.e. our world), so getting it right is a requirement for it to be good.

### Art vs. Programming

Comparing this to programming; there doesn’t seem to be that much variety in the skillsets required to write a program to do something like make an enemy move and attack. A short list might be:

1. See if a library/tool already exists
2. Follow a short tutorial and use the code as is/ with amendments
3. Refer to the code in multiple places once it’s tested/functional

This set of steps is essentially how you implement *anything* from a programmer’s perspective. Eventually the list gets shorter once you are reusing things you already know how to do, and you can essentially retool something you’ve written from (1).

For example, I was writing a script to make a weapon fire six times in a row instead of once. I simply:

1. Moved the “fire” mechanic into a function
2. When the new button was pressed: call the function in a loop that ran 6 times

Artists don’t have those luxuries. Even if there’s a full physics system that has 3D models that are rigged to animate in a specific way, it quickly becomes soulless. “Oh, just design your character and they all run exactly the same way.” Adding new skins to characters can be cheaper time-wise, but will quickly become boring.

And I’ve only talked about characters, but maps and assets in those maps are all much more demanding on artists than programmers. Drawing grass that moves requires drawing the frames in 2D or animating a model of grass in 3D.

People want and expect characters to be unique and well done, which includes details like variations in how they move and interact with the world.

If a bunch of enemies use the same code to attack and move, it seems logical, but if every enemy is just the exact same art model, it looks lazy.

Just take the NES *Super Mario Bros.* If all the enemies were Goombas (just bigger or smaller), it wouldn’t be nearly as interesting as having Koopas, or Piranha Plants, or Bullet Bills be enemies you face off against. Sameness is boring to your brain.

In some ways, programming itself can be an “art” (code design, patterns, etc.) but it operates much more invisibly, like the engine of a car, than the body and color of the car.

So I must give credit to video game artists, they have their work cut out for them hahaha.
