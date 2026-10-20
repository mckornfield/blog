---
title: "Some Weird Things in Rust That Stood Out to Me"
subtitle: "As a total rust noob"
date: 2026-08-10
medium_url: "https://medium.com/@mckornfield/some-weird-things-in-rust-that-stood-out-to-me-5cd7eb5a4606"
---

![Photo by Chandler Cruttenden on Unsplash](/img/some-weird-things-in-rust-that-stood-out-to-me/0_I7mw8xVujC24zwFI.jpg)

*Photo by [Chandler Cruttenden](https://unsplash.com/@chanphoto?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

I recently went through [*rustlings*](https://rustlings.rust-lang.org/?utm_source=substack&utm_medium=email)*,* a koan style set of exercises to learn rust concepts. I would recommend it to you if you’re interesting in being able to understand the language, and even write in it. Also would recommend doing it by hand, and not, you know…

Anyway, here are some things that stood out

### Ownership and the Borrow Checker

Rust has a ton of compilation/language features built around this memory management concept called “borrowing.”

Before explaining it, understand that there’s 2 standard ways memory is managed.

- In languages like C/C++, you manage your own memory, having to allocate and deallocate heap memory (at your own peril)
- In most other languages (Go, Python, Javascript), heap memory is managed by a garbage collector, which… can have its own [set of issues](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)

So Rust presents a third way, which the Rust book calls “[ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)”. The Rust book itself explains it better than I will, but stated shortly, it’s a way to ensure that variables are mutated that’s very clear from the code (using keywords like `move` ,`mut` or `&` ) AND to make it possible to clean up memory from the heap as though it were stack memory.

- Variables on the stack -> ones that appear in function calls and go away
- Variables on the heap -> ones that are placed in a big pile of memory and must be freed/mutated with care

When things go out of scope in rust, the borrow checker determines if memory has no more references to it, and frees it in the moment, instead of relying on *you* to `free` on your own or rely on the garbage collector to come along and do so.

The tradeoff is the language is a lot stricter about what configurations are possible, and requires some [truly strange looking syntax](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html) when there are edge cases.

### The compiler is very nice, but also can be slow

The rust compiler is very good at helping you when you are overwhelmed by the memory/type features of the language. Another example from the rustbook

```rust
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
warning: unused `Result` that must be used
  --> src/main.rs:10:5
   |
10 |     io::stdin().read_line(&mut guess);
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
   = note: this `Result` may be an `Err` variant, which should be handled
   = note: `#[warn(unused_must_use)]` on by default
help: use `let _ = ...` to ignore the resulting value
   |
10 |     let _ = io::stdin().read_line(&mut guess);
   |     +++++++

warning: `guessing_game` (bin "guessing_game") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.59s
```

The compiler is very explicit about errors, as well as providing remediation, unlike some compilers I’ve used (looking at you, javac!)

But downside is there are examples of compilation time being *slow.*

And [comparisons between rust and C++](https://quick-lint-js.com/blog/cpp-vs-rust-build-times/) compilation will find compilation slower. That can be bad if you’re trying to iterate and waiting for rust binaries/libraries to chug through recompiling.

Rust does have incremental compilation, and it’s a known issue (feature?) of the language that it has a slow linker/compiler, but it is also notably [faster on linux](https://users.rust-lang.org/t/macos-performance-issues-much-slower-than-linux-windows/136341) than on MacOS.

### Pointers are still weird, but less footgun-y

Rust has pointers.

*&lt;runs away screaming>*

All languages have pointers, they just don’t let you necessarily interrogate them/manage them the way C++/Rust do. In other languages without direct pointer access, your pointers are “classes” or “arrays” etc., which are “pointers” to data, but the `&` and `*` operators are not used.

I find that rust’s use of pointers is still odd (I swear I never know which reference/address symbols to use) but because of the borrow checker and `mut` keyword (mutable), it’s much clearer (and in the compiler’s case, a compilation error) when you’re creating a scenario that could cause a pointer class of error.

Rust even goes a step further with special “[smart pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html)”, like Box and Rc (reference count), that help with issues like circular types (e.g., `Node(int,Node)) or graph data structures. These types help keep the “ergonomics” of pointers, but allow supporting other use cases.

### Traits, not Interfaces

Rust has Traits. They are kinda like interfaces, but a lot of the generics/binding syntax looks pretty weird.

For example, from the [rustbook page](https://doc.rust-lang.org/book/ch10-02-traits.html) about traits, you can bind to multiple traits like so in a method

```rust
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

I thought “that is cool, but that isn’t what I remember from Java”, which looks like

```java
public class MultiBoundExecutor<T extends Runnable & Serializable> {
```

Very similar, just using a plus and the types are just put together with `+` , instead of the extends weirdness.

The differences don’t end with the syntax, there are a bunch of nuanced differences that make them similar but different, [here’s a better rundown than I’ll do](https://stackoverflow.com/questions/69477460/is-rust-trait-the-same-as-java-interface/69485860#69485860). Just know that it looks close enough to make you think “oh this is familiar” and then the more you read you’ll think “wait this is not how it works in Java/Go etc.”

### Matching syntax, omg so functional

The match syntax is one of the nicer language features of Rust. A good example from the rustlings exercise is the match syntax combined with a range style operator

```rust
fn maybe_ice_cream(hour_of_day: u16) -> Option<u16> {
    match hour_of_day {
        0..=21 => Some(5),
        22..=23 => Some(0),
        24..=u16::MAX => None
    }
}
```

`Some` and `None` are familar to those who have used `Optional` in Java, but `Option` is an indicator to the caller (like Rust’s other type, `Result` ) that a method could return something you weren’t expecting.

Consider this example from rustlings as well, where you can also match on conditional values, and return a different result (which, itself, can be handled with another match construct or `if let` )

```rust
impl PositiveNonzeroInteger {
    fn new(value: i64) -> Result<PositiveNonzeroInteger, CreationError> {
        match value {
            x if x < 0 => Err(CreationError::Negative),
            0 => Err(CreationError::Zero),
            x => Ok(PositiveNonzeroInteger(x as u64)),
        }
    }
}
```

You can match on types and the structure of a variable as well, it’s pretty rad.

Rust has plenty of language features worth checking out, just to understand it better, and hopefully improve your understanding of programs overall, despite how much may or may not be written by AI!

Thanks for reading

### References

<https://discord.com/blog/why-discord-is-switching-from-go-to-rust>

[The Rust Programming Language](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)

<https://doc.rust-lang.org/book/ch15-00-smart-pointers.html>
