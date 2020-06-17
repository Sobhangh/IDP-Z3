–-
title: Timeout
tags: #hosting
Date: 20200617131438
–-

Options:
- [ ] [gunicorn timeout](https://docs.gunicorn.org/en/stable/settings.html#timeout)
    - [ ] [on Google App Engine](https://stackoverflow.com/questions/58477029/google-app-engine-gunicorn-worker-timeout-in-flask-app-when-loading-a-large-pick)
    - [x] [in app.yaml](https://stackoverflow.com/questions/10855197/gunicorn-worker-timeout-error?rq=1)
- [ ] use signal ([Source](https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/))
        * problem: ValueError: signal only works in main thread

test: www…./test