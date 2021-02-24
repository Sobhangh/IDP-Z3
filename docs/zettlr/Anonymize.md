–-
title: Anonymize
tags: #hosting
Date: 20200901104252
–-
Steps to push on heroku:
* git checkout main
* git merge -s ours Anonymous
* git checkout Anonymous
* git merge main
* git push heroku Anonymous


Steps to release an anonymized version of the code:
* delete autconfigz3/bin, /lib, /lib64, _pycache_
* in web-IDP-Z3/src/app/app.component.html
    * remove KUL logo
    * remove footerContainer with Flemish Impuls program
* in web-IDP-Z3/src/app/header/header.component.ts
    * remove Help / Tutorial entry
    * link for reference: `AppSettings.ORIGIN+'/docs/_build/html/index.html'`
* in IDP-Z3/README.md: adapt as necessary
* in IDP-Z3/docs/conf.py : adapt copyright, authors
* generate [[Sphynx]] documentation: sphinx-autobuild docs docs/_build/html
* replace copyright text in all source code (see below)
* remove unnecessary code in deploy.sh
* run ./deploy.sh without deployment to GAE, Heroku
* in IDP-Z3/idp_server/static/assets/
    * delete KU Leuven Logo.png
    * delete Interactive_Consultant.mp4
* copy IDP-Z3 to anon
* delete
    * anon/.git
    * anon/docs/zetllr


"""
    Copyright 2020 Anonymous
 This file is distributed for the sole purpose of an article review.  It cannot be used for any other purpose.
"""