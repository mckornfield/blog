---
title: "My Stupid Expense Capturing Thingy"
subtitle: "You too, can process receipts with AI"
date: 2026-10-09
medium_url: "https://medium.com/@mckornfield/my-stupid-expense-capturing-thingy-1635cda8b337"
---

![Photo by Camilo Rueda Lopez on Unsplash](/img/my-stupid-expense-capturing-thingy/0_GoQg8bKAYF5hwXgT.jpg)

*Photo by [Camilo Rueda Lopez](https://unsplash.com/@kozumel?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Some Context

I looked into what folks use when capturing expenses for tax purposes and stumbled upon all sorts of apps with varying costs and levels of integration.

But I am a simple man and love Google Drive, so my workflow was just:

1. Use the Drive scan/upload feature
2. Add an entry by hand to a Google Sheet

It was simple and basic, and worked, but I thought: could I make it so the receipt somehow “landed” in the Sheet, without having to hand enter things.

So I asked Claude to help me out (as folks do these days).

### The Script

Google App Scripts are a personal favorite of mine, along with Chrome Extensions. I think GSuite and Chrome + extensions are probably my favorite things about Google as a company, though I know Search and Ads are where the $$ are.

Anyway, here’s a [link to the script](https://gist.github.com/mckornfield/8d6b37734d9ab33d1da195e4739af0cb), which if you want to try playing with it, you just have to make an App Script in Google Drive, fill in the “bracketed” parts below, and make sure you set an API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).

```csharp
const CONFIG = {
  INBOX_FOLDER_ID: '<folder_id_from_drive>',        // These are in the URL when you open the folder
  DONE_FOLDER_ID: '<processed_folder_id_from_drive>',
  SHEET_ID: '<sheet to write things>',
  SHEET_NAME: 'Expenses',
  MODEL: 'gemini-3.5-flash-lite',
  PROPERTY: '<address>',        // default property tag; model can't know this
};
```

Notably it’s only about 4 things to fill in, and PROPERTY is arguably only important if you have more than one to take expenses for, assuming it’s a rental/business, but I just inject it into the sheet, since none of the receipts will have this info.

This script doesn’t do a whole lot, it:

1. Reads from an “inbox” folder, which represents new expenses
2. Takes each PDF/image and sends it to Gemini along with a prompt asking for specific info to be extracted (I used a free model that gives decent results, depending on when you read this you might need to use another model)
3. Add a line to a spreadsheet (SHEET\_ID) with the expense, categorization, and a link to the expense doc
4. Move the PDF/image to the “done” folder

When setting it up, you also run the “setup” function, so that it runs on a trigger every hour.

### Where the Script Shines

It’s really good at extracting the total and categorizing. I haven’t really seen it go wrong there. It also can do it pretty dang fast, faster than I could hand enter it or categorize it in the sheet.

It also makes me feel cool: omg I’m using AI to automate menial things!

### Where it Doesn’t

You’ll notice that in the script I have this weird date extraction thing

```javascript
function dateFromName_(name) {
  // matches 2026_08_06, 2026-08-06, 2026.08.06, or 20260806
  const m = name.match(/(20\d{2})[_\-.]?(0[1-9]|1[0-2])[_\-.]?(0[1-9]|[12]\d|3[01])/);
  return m ? `${m[1]}-${m[2]}-${m[3]}` : null;
}
```

That is because I name my files `amazon_2026_08_06.pdf` or whatever I use for the invoice. If I have more than one on a day that can be `amazon_2026_08_06_01.pdf` , but the regex just grabs the dates like it shows in that code example.

Every 5th or so date extraction would just be *wrong*. And my receipt dates could be different than my upload dates, so I couldn’t just go off of that. I found that entering it into the name of the file helped also finding things bookkeeping-wise, and made it so the script could just pop the date off from there, instead of trying to read it off of some (arguably very blurry) receipts.

### What’s Next?

Personally I think the workflow doesn’t need to change much. Taking a picture of a receipt, putting it in the right folder, giving it a name that has the business and a date in the title so I get things right, is about 30s of my time, and gets a good result once processed.

I noticed there were some duplicates (probably from me testing/race conditions on processing), and I found them just by having Claude audit the final sheet, though I suppose a “duplicate checker” would have worked as well. So still manually reviewing things is good (especially so that I don’t hand it to an accountant and they think *wtf is this*).

Anyway, hopefully this helps inspire you to automate something basic in Drive, with Claude’s help or with Gemini too (or heck, your own brain).

Thanks for reading.
