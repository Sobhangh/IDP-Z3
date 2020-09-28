–-
title: Anomymize
tags: 
Date: 20200901104252
–-

Steps to release an anonymized version of the code:
* delete autconfigz3/bin, /lib, /lib64, _pycache_
* in autoconfig3/src/app/app.component.html
    * remove KUL logo
    * remove footerContainer with Flemish Impuls program
* in autoconfig3/src/app/header/header.component.ts
    * remove Help / Tutorial entry
    * link for reference: `AppSettings.ORIGIN+'/docs/_build/html/index.html'`
* in autoconfigz3/README.md: adapt as necessary
* in autoconfigz3/docs/conf.py : adapt copyright, authors
* generate [[Sphynx]] documentation: sphinx-autobuild docs docs/_build/html
* replace copyright text in all source code (see below)
* remove unnecessary code in deploy.sh
* run ./deploy.sh without deployment to GAE, Heroku
* in autoconfigz3/consultant/static/assets/
    * delete KU Leuven Logo.png
    * delete Interactive_Consultant.mp4
* copy autoconfigz3 to anon
* delete 
    * anon/.git
    * anon/docs/zetllr


"""
    Copyright 2020 Anonymous
 This file is distributed for the sole purpose of an article review.  It cannot be used for any other purpose.
"""