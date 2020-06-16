–-
title: Nim
tags: 
Date: 20200510185453
–-

Rewrite in [Nim](https://nim-lang.org/) ?
* compiled → faster
* strict typing → error catching
* can run on web client
* C/C++ interoperability
* concurrency
* solve performance issues such as [[Slow copy]]

But:
* poor debugger → need to use logs instead
* Google App Engine ?  use [nimporter](https://github.com/Pebaz/nimporter): makes it easy to distribute modules written in nim = alternative to [[Cython]] 


Options:
* rewrite Idp module: send string to analyzer written in Nim, and get a messagepack in return