–-
title: Google App Engine cost
tags: #hosting
   ID: 20200527072846
–-

Cost drivers:
* [instance class](https://cloud.google.com/appengine/docs/standard): F4 costs 4 times F1 (1 hour of use is billed 4 hours)
* number of instances (visible in console):
    * max_concurrent_requests
    * static files at initial load ?
    * duration of request (e.g. abstract, check-code)

Options:
- [ ] delay loading of main.js to avoid conflict with other static files
- [ ] increase max_concurrent_requests
- [ ] reduce instance class ?  → slow !
- [ ] use [Cloud Storage](https://cloud.google.com/appengine/docs/standard/python3/serving-static-files) ?