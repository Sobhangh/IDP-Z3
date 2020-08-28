–-
title: Sphinx
tags: #documentation
ID: 20200629120249
–-

using [restructuredText](https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html)

Done, following [this tutorial](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html):
* python3.8 -m pip install sphinx
    * version 3.1
* python3.8 -m pip install sphinx-rtd-theme
    * version 0.5.0
* sphinx-quickstart
    * → creates files
* edit index.rst, introduction.rst
* make html

Read-the-docs:
* create an account using gitLab authorization for pierre.carbonnelle
* show list of GitLab projects → Import autoconfig.z3
* error due to sphinx 1.8.5 → add doc/requirements.txt
* [view doc online](https://idp-z3.readthedocs.io/en/latest/?)
* [use .inc file extension](https://stackoverflow.com/a/35541748/474491) for vocabulary
* python3.8 -m pip install [sphinx-autobuild](https://pypi.org/project/sphinx-autobuild/)
* sphinx-autobuild docs docs/_build/html
* open browser at http://127.0.0.1:8000


For thesis ?
* [template](https://github.com/jaantollander/Sphinx-Thesis-Template)
* [latex customisation of sphinx](https://www.sphinx-doc.org/en/master/latex.html)
* [bibtex](https://sphinxcontrib-bibtex.readthedocs.io/en/latest/)