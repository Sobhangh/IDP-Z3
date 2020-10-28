
Introduction
============

IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the IDP language and a Z3 SMT solver.

In the Knowledge Base paradigm, the knowledge about a particular problem domain is encoded using a declarative language, and later used to solve particular problems by applying the appropriate type of reasoning, or "inference".
The inferences include:

* model checking: does a particular solution satisfy the laws in the knowledge base ?
* model search: extend a partial solution into a full solution
* model propagation: find the facts that are common to all solutions that extend a partial one

The IDP-Z3 components together enable the creation of these solutions:

.. _Consultant:
.. index:: Interactive Consultant

* the `Interactive Consultant <https://interactive-consultant.ew.r.appspot.com/>`_, which allow a knowledge expert to enter knowledge about a particular problem domain, and an end user to interactively find solutions for particular problem instances;
* :ref:`a program<CLI>` with a command line interface to compute inferences on a knowledge base;
* a `web-based Interactive Development Environment <https://interactive-consultant.ew.r.appspot.com/IDE>`_ (IDE) to create Knowledge bases.

The `source code of IDP-Z3 <https://gitlab.com/krr/IDP-Z3>`_ is publicly available under the GNU LGPL v3 license.

.. warning::
   You may want to verify that you are seeing the documentation relevant for the version of IDP-Z3 you are using.
   On `readthedocs <https://idp-z3.readthedocs.io/>`_, you can see the version under the title (top left corner), and you can change it using the listbox at the bottom left corner.

Installation using poetry
-------------------------

`Poetry <https://python-poetry.org/>`_ is a package manager for python.

* Install `python3 <https://www.python.org/downloads/>`_ on your machine
* Install `poetry <https://python-poetry.org/docs/#installation>`_

    * after that, logout and login if requested, to update :code:`$PATH`
* Use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine
* Open a terminal in that directory 
* If you have several versions of python3, and want to run on a particular one, e.g., 3.9:

    * run :code:`poetry env use 3.9`
    * replace :code:`python3` by :code:`python3.9` in the commands below
* Run :code:`poetry install`

To launch the Interactive Consultant web server:

* open a terminal in that directory and run :code:`poetry run python3 main.py`

After that, you can open 

* the Interactive Consultant at http://127.0.0.1:5000
* the web IDE at http://127.0.0.1:5000/IDE



Installation using pip
----------------------

IDP-Z3 can be installed using the python package ecosystem.

* install `python 3 <https://www.python.org/downloads/>`_, with `pip3 <https://pip.pypa.io/en/stable/installing/>`_, making sure that python3 is in the PATH.
* use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine
* (For Linux and MacOS) open a terminal in that directory and run the following commands.

.. code-block::

   python3 -m venv .
   source bin/activate
   python3 -m pip install -r requirements.txt

* (For Windows) open a terminal in that directory and run the following commands.

.. code-block::

   python3 -m venv .
   .\Scripts\activate
   python3 -m pip install -r requirements.txt

To launch the web server on Linux/MacOS, run

.. code-block::

   source bin/activate
   python3 main.py

On Windows, the commands are:

.. code-block::

   .\Scripts\activate
   python3 main.py


After that, you can open 

* the Interactive Consultant at http://127.0.0.1:5000
* the web IDE at http://127.0.0.1:5000/IDE