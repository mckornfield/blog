---
title: "Scratching your nose… using AWS IAM"
date: 2022-10-07
medium_url: "https://medium.com/@mckornfield/scratching-your-nose-using-aws-iam-1e86231d99ba"
---

![Photo by Braydon Anderson on Unsplash](/img/scratching-your-nose-using-aws-iam/0_6hQIto-8kSbaSaje.jpg)

*Photo by [Braydon Anderson](https://unsplash.com/@braydona?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I thought I’d write something silly explaining how to use [AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) (Identity and Access Management) permissions with something really concrete… scratching your nose. Maybe this will help you understand IAM a bit better or at least make you chuckle 😆.

## Your whole hand scratches your whole nose

Let’s say tomorrow the AWS team gained control of your body and employed their security model to your hands and your nose. Your brain tells you that your nose is itchy, let’s say your brain has `AdministratorAccess` on your body so it can easily see a CloudWatch alert was triggered:

```
Nose scratchiness has exceeded annoyance threshold of 0.95/ 1.0. Scratch it now!
```

Your brain is more than equipped to handle this; because it has Admin on the account, it makes a call to the HandService and fires off the `Scratch` API on the `Nose` resource.

Your brain is baffled when, with a jerk of your arm, nothing happens. It reads the output from the call it just made.

```
An error occurred while calling Scratch on target Nose. "RightHand" does not have the permission to perform the action "Scratch".
```

Unbelievable!

You can’t scratch your own nose with your own hand. AWS be darned!

You pull up the role associated with your RightHand and notice that the JSON policy is blank. Great. You find an example online that looks similar enough and come up with this for your `RightHandRolePolicy`:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LetMeScratch",
      "Effect": "Allow",
      "Action": [
        "PerformScratch",
      ],
      "Resource": [
        "RightHand"
      ]
    }
}
```

You apply the policy updates and send the command again. Your hand jerks up to your face but nothing happens. Of course another error message is waiting for you.

```
An error occurred (AccessDenied) while calling Scratch on target Nose.
```

You are seriously confused now. Didn’t you just give it permission? You look online and find that, funnily enough, *you have to allow your nose to receive scratches*.

You’re following best practices/ principle of least privilege so you limit the security down to just your Nose, so you don’t scratch anywhere else accidentally. Of course you need to give `ReceiveScratch` to your Nose.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LetMyHandScratchMyNose",
      "Effect": "Allow",
      "Action": [
        "ReceiveScratch",
      ],
      "Resource": [
        "Nose:*"
      ]
    }
}
```

You send the `Scratch` command again, and huzzah! You scratch your nose… but you do it by kind of rubbing the palm of your hand on your nose. Not the greatest experience. You stand there rubbing your hand across your face and come up with a new plan.

## Scratching your nose with your finger

You realize the `Scratch` API can take in some additional arguments. So you decide to fire `Scratch` off but this time using `RightHand:indexFinger` . You’re 90% sure it will fail and sure enough…

```
An error occurred while calling Scratch on target Nose. "RightHand:IndexFinger" does not have the permission to perform the action "Scratch".
```

You know what’s going to happen again so you pull open the policy document and just throw in a simple `:*` after RightHand, in case you want to use ANOTHER finger, so you get something like

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LetMeScratch",
      "Effect": "Allow",
      "Action": [
        "PerformScratch",
      ],
      "Resource": [
       "RightHand",
       "RightHand:*"
      ]
    }
}
```

You fire off the scratch command again with the `indexFinger` parameter and hooray, you scratch your nose! You even add a call to `middleFinger` to scratch it and you’ve got a wonderful two finger scratch going.

After scratching your nose furiously for a while you realize something awful. You can’t stop scratching. You fire off a `scratchingStop` command but of course you get some error message. You know what to do!

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LetMeScratch",
      "Effect": "Allow",
      "Action": [
        "PerformScratch",
        "StopScratch"
      ],
      "Resource": [
       "RightHand",
       "RightHand:*"
      ]
    }
}
```

Once that’s updated you can thankfully stop scratching your nose.

### Rate Limits

You wake up the next day with a bug bite on your nose. You’re thankful you have all this scratching figured out and you fire off the API, going to town on your nose.

But around lunchtime you spontaneously stop scratching, your hand useless in front of your face. You look at the error message:

```
Rate exceeded (Service: RightHand)
```

Your RightHand is tired! What can you do? Besides waiting a bit, you can also use your LeftHand of course. You fire off the call to use your LeftHand to Scratch but…

You don’t even have to look at the error; you just go to your LeftHand’s policy document and sure enough, it’s blank.

You know what you have to do… but you decide to pick up a backscratcher with your LeftHand and bypass the AWS security over your body by using a 3rd party tool instead. Ahhhhhh feels nice.

Until you poke yourself in the eye with it (Ow). Darn 3rd party tools and their lack of security.

Thanks, hopefully it was fun for you!.
