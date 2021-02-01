The IDP-Z3 tools implement a knowledge base system combining the Microsoft Z3 solver and a grounder developed in-house, supporting the IDP language.  See the presentation at [www.IDP-Z3.be](https://www.IDP-Z3.be).

It is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).


# Installation

* Install [python3](https://www.python.org/downloads/) on your machine.
* Install [poetry](https://python-poetry.org/docs/#installation):
    * after that, logout and login if requested, to update `$PATH`
* Use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine
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

You may want to read about the [technical documentation](http://docs.idp-z3.be/en/latest/code_reference.html) and the [Development and deployment guide](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).

The user manual is in the `/docs` folder and can be locally generated as follows:
~~~~
poetry run sphinx-autobuild docs docs/_build/html
~~~~
To view it, open `http://127.0.0.1:8000`

The [documentation](https://docs.IDP-Z3.be) on [readthedocs](https://readthedocs.org/projects/idp-z3/) is automatically updated from the main branch of the GitLab repository.

The [home page](https://www.IDP-Z3.be) is in the `/homepage` folder and can be locally generated as follows:
~~~~
poetry run sphinx-autobuild homepage homepage/_build/html
~~~~
To view it, open `http://127.0.0.1:8000`.  The website is also automatically updated from the main branch of the GitLab repository.


# Testing

To generate the tests, from the top directory run `poetry run python3 test.py` or `poetry run python3 test.py generate`.
After this, you can manually check what has changed using git.

There is also a testing pipeline available, which can be used by running `poetry run python3 test.py pipeline`.


# Deploy

See the instructions [here](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).
