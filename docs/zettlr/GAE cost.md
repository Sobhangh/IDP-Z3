–-
title: Google App Engine cost
tags: #hosting
Date: 20200527072846
–-

Cost drivers:
* [instance class](https://cloud.google.com/appengine/docs/standard): F4 costs 4 times F1 (1 hour of use is billed 4 hours)
* number of instances (visible in console):
    * max_concurrent_requests
    * static files at initial load ?
    * duration of request (e.g. abstract, check-code)
    * concurrent load of /meta and Monaco editor

Objective: 1 instance if only 1 (new) user

## Options:
- [x] use [Cloud Storage](https://cloud.google.com/appengine/docs/standard/python3/serving-static-files)
    - problem with version history ?
        - Each evolving file has an ID → OK
        - editor has no ID, but is served by static dir (see below) → OK
- [x] [app.yaml scaling elements](https://cloud.google.com/appengine/docs/standard/python3/config/appref#scaling_elements)
    - [x] increase min_pending_latency in app.yaml (from 30 ms default to 300 ms)
    - [x] [use static dir](https://cloud.google.com/appengine/docs/standard/python3/serving-static-files#configuring_your_static_file_handlers)  → not subject to number of concurrent requests ?
    X reduce instance class ?  → slow !
    X increase max_concurrent_requests → not safe !
- [x] add timeout in abstract inference
- [ ] add general [[Timeout]] : accepted by GAE ?
- [ ] [get Monaco editor from CDN](https://stackoverflow.com/questions/51484076/angular-include-cdn-in-component-usage/51534969), not local: not easy (see [here](https://www.ngdevelop.tech/loading-external-libraries-from-cdn-in-angular-application/) and [here](https://medium.com/lacolaco-blog/use-ionic-components-as-web-components-in-angular-2eee2178d5be).  [Impossible for components ?](https://www.reddit.com/r/angularjs/comments/507c9f/including_angular_2_components_from_a_cdn/))
X reduce the number of request from client, e.g. combine .js files
X use 2 machines with different max_concurrent_requests: one for static, the other for Z3
- [ ] delay loading of main.js to avoid conflict with other static files
- [ ] move Z3Lock down in call stack, e.g. when computing model

## Max concurrent request:
* there is a z3lock anyway
    * but a long /eval may block other /eval.  How to force the creation of a new instance ?
    * if Z3 is busy, CPU is busy (?) → GAE will start another instance anyway ?
* is Z3 threadsafe ? [No](https://stackoverflow.com/questions/28558180/is-z3-python-interface-threadsafe), except [if each thread has its own context](https://stackoverflow.com/questions/25542200/multi-threaded-z3)
* [test rest locally](https://flask.palletsprojects.com/en/1.1.x/testing/)  and [under load](https://locust.io/)

## Cloud storage
* create deploy.sh
* [create bucket](https://cloud.google.com/appengine/docs/standard/python3/serving-static-files)
    * `gsutil mb gs://interactive-consultant`
    * `gsutil defacl set public-read gs://interactive-consultant`
- use [--deploy-url in ng guild](https://stackoverflow.com/questions/46613816/how-to-deploy-angular-4-front-end-to-cdn)
* sync bucket ? `gsutil -m rsync -r ./idp_server/static gs://interactive-consultant/`
* [font CORS issue](https://stackoverflow.com/questions/33242062/google-cloud-storage-fonts-cors-issue)
    * use http instead of https ? no fix
    * cors-config.json ?  OK   `gsutil cors set cors-config.json gs://interactive-consultant\`

## B8 not responding
[in this version](https://20200617t153532-dot-interactive-consultant.ew.r.appspot.com/) of server:
* Etat = Arrêtée ? → select it and click start
* /meta does not respond
* backend instances are [addressable by name](https://stackoverflow.com/questions/11886915/google-app-engine-backend-vs-frontend-instances), so you need [a load balancer](https://cloud.google.com/compute/docs/instance-groups/adding-an-instance-group-to-a-load-balancer) or [backend service](https://cloud.google.com/load-balancing/docs/backend-service) to run them