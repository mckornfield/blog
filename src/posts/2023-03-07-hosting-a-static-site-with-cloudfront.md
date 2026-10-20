---
title: "Hosting a Static Site with Cloudfront"
date: 2023-03-07
medium_url: "https://medium.com/@mckornfield/hosting-a-static-site-with-cloudfront-55fcc57341dd"
---

A simple tutorial with some pictures

![Photo by Davies Designs Studio on Unsplash](/img/hosting-a-static-site-with-cloudfront/0_f1icIvN7R2fCjb1o.jpg)

*Photo by [Davies Designs Studio](https://unsplash.com/@davies_designs?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### What is Cloudfront?

Cloudfront is Amazon’s Cloud Distribution Network (CDN) that they offer as a service to customers. It basically means that it’s a way to store (cache) resources close to where users might request them from.

It can stand in front of an Elastic Load Balancer (ELB), which would itself be in front of some sort of application, or it can stand in front of Amazon’s serverless storage mechanism, S3. (It can also front MediaStore, but we won’t go there…)

The way Cloudfront caches things for you, depending on your setup, is:

1. A user makes a request to a Cloudfront resource, let’s say the static website
2. The Cloudfront URL resolves to an IP address/ data center near the user, but the files are not cached
3. The Cloudfront service makes a call to the origin (for example, an S3 bucket in another region), pulls the resource, caches it in the nearest data center
4. Cloudfront returns the resource

Now if you or another user make the request again from the same geographic region, Cloudfront won’t have to go to the origin (unless the cache is invalidated), but can instead serve you content it has stored locally.

### OK, Just Show Me How to Host a Website Now

Alright, you’ve got your [AWS account set up to play around in](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/). Here’s what you need to do, with some pictures after. We’re going to create an S3 Bucket and connect it to Cloudfront, then upload a very simple website file

[1. Create a public S3 bucket](https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1&region=us-east-1). S3 bucket names must be globally unique, so something like `my-website-MYSTREET-test` will probably be fine. If not, add whatever you need to the bucket name to allow you to create it. For the region, feel free to use us-east-1, but if you want to experiment, make it a region [that’s not geographically close to you](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/), so you can see Cloudfront do its magic later.

![](/img/hosting-a-static-site-with-cloudfront/1_ijRLuMU2buarulLTdClpbw.png.png)

2. To make your bucket public, uncheck the box that says `Block all public access` . If you want to store private files, you’ll definitely want to keep that box checked and use Access Controls, presigned URLs, etc. But for our website, we want to **uncheck** it! And check the box below the warning to acknowledge.

![Uncheck everything except that acknowledgement box](/img/hosting-a-static-site-with-cloudfront/1_7Ol9l5iRBNMx0FQJzs6jdg.png.png)

*Uncheck everything except that acknowledgement box*

3. Leave everything else default and click “Create Bucket” at the bottom right.

4. Click into your bucket. Click `Upload` . Make a file on your computer named `index.html` with the content below, and upload it to your bucket at the root.

```xml
<!DOCTYPE html>
<html>
  <body>
    <h1>Welcome to my site!</h1>
  </body>
</html>
```

5. Go to Permissions, scroll down to Bucket Policy, and edit it so it looks like the below, but with your bucket name instead of `my-website-ward-test` . This will *really* make your website public.

```json
{
 "Version": "2008-10-17",
 "Statement": [
  {
   "Sid": "",
   "Effect": "Allow",
   "Principal": {
    "AWS": "*"
   },
   "Action": "s3:GetObject",
   "Resource": "arn:aws:s3:::my-website-ward-test/*"
  }
 ]
}
```

At this point, technically you already have a static site! You can click Open

![Click the open button!](/img/hosting-a-static-site-with-cloudfront/1_fpCevPQ4_c6bA8d2aa0PIQ.png.png)

*Click the open button!*

and you should see a page like this:

![Websites like it’s 1999](/img/hosting-a-static-site-with-cloudfront/1_nTxl7ttfyVNbGpmtzvJEJA.png.png)

*Websites like it’s 1999*

Even without the query parameters (everything after the `?`) your website should still be visible, meaning it’s truly public!

Let’s keep going to hook this up to Cloudfront.

[6. Go to Cloudfront to create a new distribution](https://us-east-1.console.aws.amazon.com/cloudfront/v3/home?region=us-east-1#/welcome).

7. Select your S3 bucket from the “Origin Domain” box.

![](/img/hosting-a-static-site-with-cloudfront/1_-mlB0cVvkfz_wgE7vSoXIA.png.png)

8. Scroll all the way down and keep everything the default (though feel free to click “Use only North America and Europe” for the price class), click “Create Distribution.”

Wait a bit for Cloudfront to deploy (you’ll see a “deploying” status going).

![I want it now!](/img/hosting-a-static-site-with-cloudfront/1_0mVs_hyXrXEJ_Z9V_O_T4w.png.png)

*I want it now!*

Once it’s done deploying, you’ll be able to copy the URL from the screen, and with `/index.html` at the end, you’ll see the same website as before, but this time distributed using Cloudfront instead of S3 :)

### Verifying the Geolocation Behavior

If you want to verify that things are actually different, you can see the IP addresses and look for certain headers in the browser console, like `x-amz-cf-pop` or the IP address from the response.

![](/img/hosting-a-static-site-with-cloudfront/1_AeJZlUI_jYniZPnAU3AN7A.png.png)

That [ID maps to the cloudfront location](https://www.feitsui.com/en/article/3) that I accessed (one in LA).

### Cleanup

- Delete the `index.html` file and your S3 bucket
- Disable the Cloudfront distribution, then once that’s done deploying, you’ll be able to delete it

Thanks for reading, hopefully you learned something.
