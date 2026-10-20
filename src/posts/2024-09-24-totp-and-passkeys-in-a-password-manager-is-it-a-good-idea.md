---
title: "TOTP and Passkeys in a Password Manager… Is It a Good Idea?"
date: 2024-09-24
medium_url: "https://medium.com/@mckornfield/totp-and-passkeys-in-a-password-manager-is-it-a-good-idea-0aa16ac6c19f"
---

The question is about trust

![Photo by Florian Berger on Unsplash](/img/totp-and-passkeys-in-a-password-manager-is-it-a-good-idea/0_FbOVVyCOACtCI0WS.jpg)

*Photo by [Florian Berger](https://unsplash.com/@bergerteam?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Wait I’m Lost, TOTP?

![Photo by Markus Winkler on Unsplash](/img/totp-and-passkeys-in-a-password-manager-is-it-a-good-idea/0_pdxy7_LcTd6vuZq8.jpg)

*Photo by [Markus Winkler](https://unsplash.com/@markuswinkler?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Time-Based One Time Passwords. Basically if you’ve never heard of or seen it before, a website will give you a QR code you can take a picture of with your phone (using Google Authenticator, Duo, etc.), and then you get an entry for that site where a set of numbers will appear every 30 seconds.

These magic numbers (Time Based One Time Passwords or TOTP) are computed using a code that the QR code represents (you can also manually enter it or copy paste it). The time based part is that, given the time plus the secret key, you can compute a code that the server can check without you passing any other information.

Generally speaking, you store TOTP codes in a personal device like a phone, that way when you sign in, you have to enter your password AND one of these codes. Why should we do something like this?

### A Second Factor

What this gives you is a [second factor](https://mckornfield.github.io/dont-get-hacked/slides.html#/5), i.e. another way to secure your account besides a password. A second factor (i.e. 2FA or Multifactor) is the best way to protect yourself against a compromise of your system.

The analogy I like is an apartment building with a doorman. The doorman only lets people into the building that he knows ([or likes](https://www.youtube.com/watch?v=nsuJhwPQNuQ)); everyone else is turned away. But in addition to getting past the doorman, you also lock the door to your house, meaning you have multiple.

### Oh and Passkeys? (Something about FIDO?)

![Photo by Andy Kennedy on Unsplash](/img/totp-and-passkeys-in-a-password-manager-is-it-a-good-idea/0_dB5EAki7Fu1dWuxg.jpg)

*Photo by [Andy Kennedy](https://unsplash.com/@packetdiscards?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

If you’re familiar with a Yubikey (pictured above), a passkey is a software implementation of this device. FIDO (Fast IDentity Online) is an [open authentication standard](https://en.wikipedia.org/wiki/FIDO_Alliance) that the [Yubikey](https://www.fastcompany.com/90373145/yubicos-tiny-yubikey-has-the-future-of-security-all-locked-up) and [passkey](https://fidoalliance.org/passkeys/) both implement.

This standard allows you to store a cryptographic key on your device (or in your password manager, which we’ll get to) that *replaces* the need for a password.

Let’s compare this with a password; in the password scenario, you need to present a set of letters, numbers, and symbols to a website, which the website compares to a hashed (i.e. stored in a comparable but not retrievable) format. If anyone can figure out your password, they’re in.

For a passkey, you instead have to present a key that would be stored on a device (a computer or phone) or from within a password manager. This is not something that can simply be typed out; it functions similar to a TOTP in that it’s incredibly difficult (nay, impossible) to guess.

### OK Now I’m Caught Up… Now What About the Password Manager?

So TOTP and Passkeys are two things that are normally stored on a specific device (i.e. a phone or laptop). But, if you want to be able to take these technologies between your devices without setting them up on each one (or in the event that you lose a device), you’d most likely want to store them in a cloud based password manager.

Cloud based password managers come in many flavors; I used to use LastPass but [it had security issues](https://www.cybersecuritydive.com/news/lastpass-cyberattack-timeline/643958/#:~:text=How%20the%20cyberattack%20at%20LastPass%20unfolded&text=A%20threat%20actor%20compromised%20a,the%20company%27s%20internal%20system%20secrets.), as well as usability issues, namely [not supporting passkeys](https://support.lastpass.com/s/question/0D5TP000009bPS60AM/when-will-lastpass-support-passkeys?language=en_US), and [TOTP only for LastPass business users](https://support.lastpass.com/s/document-item?language=en_US&bundleId=lastpass&topicId=LastPass/create-totp-vault.html&_LANG=enus).

After doing a bit of reading I was between Bitwarden and 1Password, but finally settled on Bitwarden (kept hearing [it had decent autofill](https://www.reddit.com/r/Bitwarden/comments/15ssebq/comment/jwgfg5f/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button), which has been true for me so far). It’s also cheaper than LastPass for a family plan, so it was a no brainer to switch (and it took only a minute to export/import everything).

I started storing TOTP and Passkeys in the password manager instead of my phone, feeling supercharged. It even copies the TOTP code for me if the page prompts for it. Super nice

![The Bitwarden icons for the page link, username, password, and TOTP code respectively](/img/totp-and-passkeys-in-a-password-manager-is-it-a-good-idea/1_Dryv0V2NLR-0_ULBnUo5Dw.png.png)

*The Bitwarden icons for the page link, username, password, and TOTP code respectively*

Then I thought… well, should I?

### Do You Trust Your Password Manager?

Or rather, do you trust the technology and how well you’ve secured your password manager?

I’d say that storing passkeys and TOTP for most accounts in a password manager *that you trust* is definitely a **yes**. But trust comes in a few forms:

1. You have strongly secured the Password Manager itself (Strong Master Password, Strong Multifactor like a Yubikey). If you store multiple factors in the password manager, then it becomes a single point of failure
2. You have read enough about the Password Manager company to know they aren’t getting [compromised or screwing you](https://www.theverge.com/2024/5/1/24146205/lastpass-independent-company-security-breaches)

If you don’t trust your password manager, by all means, keep things on your personal devices and only use it for passwords, or switch to a [self hosted option](https://github.com/dani-garcia/vaultwarden) if you’re feeling brave. (Though since a passkey is mostly a replacement for a password manager, it makes little sense to keep them out of the password manager.)

But I like to think of the password manager as your walled garden. Within the garden, plants are free to grow how they like, kept safe from slugs and deer trying to gnaw them down to stubs.

While making a password manager a single point of failure can be thought of as bad, conversely, it makes sharing MFA secured accounts much easier, which is something important to do if you have a [family](https://bitwarden.com/learning/getting-started-as-a-family-member/) or [if you’re ever incapacitated](https://bitwarden.com/help/emergency-access/).

If you store your 2FA/Passkey on your device, then the family member might be completely cut off from accessing your accounts (unless you’re like my friend who has a vault with instructions and a Yubikey, absolute mad-lad.)

So in my opinion, you should store your TOTP and Passkeys in a trusted, well secured password manager. But do your research first!
