---
title: "To Cache or Not to Cache"
subtitle: "Things might be faster, but they also might be wrong!"
date: 2023-04-27
medium_url: "https://medium.com/@mckornfield/to-cache-or-not-to-cache-2bc9fc7e8aeb"
---

Things might be faster, but they also might be wrong!

![Photo by Svetlana Gumerova on Unsplash](/img/to-cache-or-not-to-cache/0_JHwi9gkhUOxF4vSW.jpg)

*Photo by [Svetlana Gumerova](https://unsplash.com/@bananablackcat?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

### Why the term “caching?”

The Americas were settled by a variety of folks, but one you may have heard of are “French Trappers.” These were French or French Canadians that worked with/ fought wit Native Americans to get various pelts they could trade back to Europe.

While roaming around the Americas, these trappers would occasionally hide supplies, so that they didn’t have to carry them all with them but also so they would have supplies spread out in readily accessible areas. They used the term *cache,* from the French *cacher* (to hide) to describe these locations.

### Caching in programming

In programming, instead of supplies, we spread *data* in different locations to help improve the efficiency and quality of our systems.

The main tradeoff is against *correctness*, you can think of this as the fur trappers worrying about food spoiling, if that was the sort of supply that they cached. A rotten piece of food would really ruin the purpose of spreading out their supplies.

### File System Caching

*Why use it?*

Downloading files, especially large ones, can be a time sink for end users. The greatest example of a file system cache is the one your browser uses. It doesn’t download the Google logo, Medium logo, or all the other images you see more than once a page loads, that way page reloads and revisits are snappy.

File system caches are usually for clients talking to systems that return lots of file data, browsers talking to servers being one of the best examples.

*When is it not worth it?*

Generally if the files are very small, or change frequently, then file system caching becomes a bit of a waste. An example might be a JSON file that contains stock information: you wouldn’t want to cache that and then have the webpage show stale information.

Browsers have relatively complicated mechanisms to invalidate cache items [based on headers](https://medium.com/@codebyamir/a-web-developers-guide-to-browser-caching-cc41f3b73e7c), but *cache invalidation* is one of the core reasons that caching can be so difficult. When you cache data, you make a conscious tradeoff between speed/efficiency and freshness of data. Trying to invalidate cached items is one of the trickier parts of working with caches.

### In Memory Caching

*Why use it?*

If you have a single process that sits in front of some system, like AWS or a database, but want to reduce the number of calls you make to that other system, simply caching things in memory can be a good call. Lots of languages offer out of the box utilities to use simple, in memory caches, like `@lru-cache` in Python, or you can [write your own for Java](https://medium.com/@getrohith.sathya/lru-cache-implementation-using-java-22dd5c218502). LRU means “least recently used”, so that entries that don’t get visited eventually get removed from the cache.

*When is it not worth it?*

If you’re working with a distributed system, i.e. multiple versions of one application server, or serverless functions, you’ll need a bit more than an in memory cache (see the next section).

In memory caches are relatively easy to set up but very quickly run into the stale data problem we saw before, and cache invalidation becomes an exercise in understanding where all of the data mutations can come in, and clearing the cache from there.

Also if the data can change outside of your process (i.e. something else can write to the data source you’re caching), then your in memory cache might cause more data consistency errors than it’s worth.

### Distributed Caching

*Why use it?*

Services like redis, memcached or Elasticache offer the ability to cache data in a whole separate service/process that your distributed system can interact with. These represent the holy grail of caching: fast key value stores that are pretty easy to integrate with and work well with scalable distributed systems. If you need to cache data for a distributed system, a distributed cache is what the doctor ordered.

*When is it not worth it?*

Adding a distributed cache is more robust than a simple in memory cache, but now introduces a whole new point of failure and additional complexity to the system.

The data clearing problem as always is still present, but now multiple processes can interact with the cache, meaning you open yourself up to strange edge cases if you don’t use something appropriate like locking.

There is also a dollar cost to running these distributed caches. If you run them within your Kubernetes cluster it can be a simple extra use of memory and CPU, but running them as a standalone service using AWS can cost [a decent amount per month](https://aws.amazon.com/elasticache/pricing/) (although necessary if you want to interact with them from serverless applications).

### In Summary

Caching is a great way to improve the performance of a system or take load off of systems like the database, but consider that caches also add complexity and the possibility of stale/wrong data being presented to consuming users/systems.

Often not caching to start is the way to go, and only adding a cache in once you identify a performance bottleneck, instead of simply caching up front.
