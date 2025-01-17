This is an extention of the IDP-Z3 knowledgebase. This extention involves adding syntax for handling history-less dynamic systems in a more elegant way. Additionally some inferences related to such systems is added such as LTL/CTL model checking, progression, simulation, invariant checking, forward chaining, iterative planning. As an example of such modeling, consider the farmer example: There is a farmer with a fox, chicken and grain. The farmer wants to move them to the other side of the river but in each passage only one of these can be taken. Additionally, the pair (fox ,chicken) and the pair (chicken, grain) cannot be left alone together. Here is the modeling of this problem using the extention:


![Screenshot 2024-08-04 at 17-49-08 Extending IDP-Z3 with Linear Time Calculus - KU_Leuven_Computer_Science_Thesis-16 pdf](https://github.com/user-attachments/assets/cfb3ecaf-83c2-4131-b86b-decac2816d91)

![Screenshot 2024-08-04 at 17-50-11 Extending IDP-Z3 with Linear Time Calculus - KU_Leuven_Computer_Science_Thesis-16 pdf](https://github.com/user-attachments/assets/3f148be3-befb-4dc6-8509-d22a726729ef)


For example, following is the transition machine of this problem which can be derived for LTL/CTL checking:

![Screenshot_4-8-2024_175726_](https://github.com/user-attachments/assets/b4bb4fb7-e52d-46d4-9f41-6df5d8ccb19e)

# Introduction

idp-engine is a reasoning engine for knowledge represented using the FO(.) language.
FO(.) (aka FO-dot) is First Order logic, with various extensions to make it more expressive:  types, equality, arithmetic, inductive definitions, aggregates, and intensional objects.
The idp-engine uses the Z3 SMT solver as a back-end.

It is developed by the Knowledge Representation group at KU Leuven in Leuven, Belgium, and made available under the [GNU LGPL v3 License](https://www.gnu.org/licenses/lgpl-3.0.txt).

See more information at [www.IDP-Z3.be](https://www.IDP-Z3.be).

Contributors (alphabetical):  Bram Aerts, Ingmar Dasseville, Jo Devriendt, Marc Denecker, Matthias Van der Hallen, Pierre Carbonnelle, Simon Vandevelde

# Installation

* Install [python3](https://www.python.org/downloads/) on your machine.
* Install [poetry](https://python-poetry.org/docs/#installation):
    * after that, logout and login if requested, to update `$PATH`
* Use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine, e.g., IDP-Z3
* Open a terminal in that IDP-Z3 directory
* If you have several versions of python3, and want to run on a particular one, e.g., 3.10:
    * run `poetry env use 3.10`
    * replace `python3` by `python3.10` in every command below
* Run `poetry install`
    * use `poetry install --no-dev` if you do not plan to contribute to IDP_Z3 development.


# Get started

To launch the Interactive Consultant web server:

* open a terminal in that directory and run `poetry run python3 main.py`
* open your browser at http://127.0.0.1:5000


The Web IDE is at http://127.0.0.1:5000/IDE
In Linux, give probcli execution right by executing the following: chmod +x probcli.sh in the IDP-Z3 folder.
Note that it has not been tested on Mac.
To use the CLI run the command: poetry run python3 idp-engine.py path/to/file.idp
For more information on the CLI check: https://docs.idp-z3.be/en/stable/IDP-Z3.html#command-line-interface
Becuase ProB is used, make sure at least Java 8 is installed.


# Develop

You may want to read about the [technical documentation](http://docs.idp-z3.be/en/latest/code_reference.html) and the [Development and deployment guide](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).

Development on the web client requires additional installation:

* install [nvm](https://github.com/nvm-sh/nvm)
* `cd idp_web_client`
* `nvm install 11`
* `npm ci`

To launch the Interactive Consultant in development mode:

* open a terminal in the IDP-Z3 directory and run `poetry run python3 main.py` to launch the IDP-Z3 server
* `cd idp_web_client`
* `npm start`
* open your browser at http://127.0.0.1:4201


# Documentation

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


# Testing of the Interactive Consultant

We use [Cypress](https://www.cypress.io/) to test the IC.  Installation in top project folder:
~~~~
npm install cypress --save-dev
~~~~
To launch it, start the Interactive Consultant in development mode, then:
~~~~
npx cypress open
~~~~
and choose E2E testing.

# Deploy

See the instructions [here](https://gitlab.com/krr/IDP-Z3/-/wikis/Development-and-deployment-guide).
