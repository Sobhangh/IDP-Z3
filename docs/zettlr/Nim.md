–-
title: Nim
tags: 
   ID: 20200510185453
–-

Rewrite in [Nim](https://nim-lang.org/) ?
* compiled → faster
* strict typing → error catching
* can run on web client
* C/C++ interoperability
* concurrency
* solve performance issues such as [[20200513173351]] slow copy

But:
* poor debugger → need to use logs instead
* build parser at run-time (to parse English) ??  via a C library ?

[nimporter](https://github.com/Pebaz/nimporter): makes it easy to distribute modules written in nim = alternative to Cython 