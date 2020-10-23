Interactive Consultant is an interactive consultant based on logic theory. It is hosted at https://interactive-consultant.ew.r.appspot.com/
Here is a [video tutorial](https://drive.google.com/open?id=1hZswGXjEK_mIyQVK5NeRhusmWkRFUo90), and a [short paper describing it](https://drive.google.com/file/d/1RLCZq-6c0b4ymNvK5C3XpFp9uE4JdmtJ/view?usp=sharing).

It uses the Z3 SMT solver.  It is made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).  


# Installation

* Install [python3](https://www.python.org/downloads/) on your machine.
* Install [poetry](https://python-poetry.org/docs/#installation):
    * after that, logout and login if requested, to update `$PATH`
* Use git to clone https://gitlab.com/krr/autoconfigz3 to a directory on your machine
* Open a terminal in that directory 
* If you have several versions of python3, and want to run on a particular one, e.g., 3.9:
    * run `poetry env use 3.9`
    * replace `python3` by `python3.9` in every command below
* Run `poetry install`


# Get started

To launch the Interactive Consultant web server:

* open a terminal in that directory and run `poetry run python3 main.py`
* open your browser at http://127.0.0.1:5000


# Develop

You may want to read about the [technical architecture](https://gitlab.com/krr/autoconfigz3/-/wikis/Architecture).

The user manual is in the `/docs` folder and can be locally generated as follows:
~~~~
sphinx-autobuild docs docs/_build/html
~~~~
To view it, open `http://127.0.0.1:8000`

The [documentation on readthedocs](https://readthedocs.org/projects/idp-z3/) is automatically updated from the gitlab repository.

To deploy on [Google App Engine](https://gitlab.com/krr/autoconfigz3/-/blob/master/docs/zettlr/Google%20App%20Engine.md):
* make sure that you are on branch master without pending git changes
* run `python3 deploy.py`

# Testing

To generate the tests, from the top directory run `poetry run python3 test.py` or `poetry run python3 test.py generate`.
After this, you can manually check what has changed.

There is also a testing pipeline available, which can be used by running `poetry run python3 test.py pipeline`.
