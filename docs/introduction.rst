
.. role:: raw-html(raw)
   :format: html

Introduction
============


IDP-Z3 is a software collection implementing the Knowledge Base paradigm using the FO[:raw-html:`&#183`] language.
FO[:raw-html:`&#183`] (aka FO-dot) is First Order logic, extended with definitions, types, arithmetic, aggregates and intensional objects.
In the Knowledge Base paradigm, the knowledge about a particular problem domain is encoded using a declarative language,
and later used to solve particular problems by applying the appropriate type of reasoning, or "inference".
The inferences include:

* model checking: does a particular solution satisfy the laws in the knowledge base ?
* model search: extend a partial solution into a full solution
* model propagation: find the facts that are common to all solutions that extend a partial one

The :ref:`IDP-Z3 engine<API>` enables the creation of these solutions:

.. _Consultant:
.. index:: Interactive Consultant

* the `Interactive Consultant <https://interactive-consultant.idp-z3.be/>`_, which allow a knowledge expert to enter knowledge about a particular problem domain, and an end user to interactively find solutions for particular problem instances;
* :ref:`a program<CLI>` with a command line interface to compute inferences on a knowledge base;
* a `web-based Interactive Development Environment <https://interactive-consultant.idp-z3.be/IDE>`_ (IDE) to create Knowledge bases.

.. warning::
   You may want to verify that you are seeing the documentation relevant for the version of IDP-Z3 you are using.
   On `readthedocs <https://docs.idp-z3.be/>`_, you can see the version under the title (top left corner), and you can change it using the listbox at the bottom left corner.


.. _Installation:
.. index:: Installation

Installation using poetry
-------------------------

`Poetry <https://python-poetry.org/>`_ is a package manager for python.

* `Install python3 <https://www.python.org/downloads/>`_ on your machine
* `Install poetry <https://python-poetry.org/docs/#installation>`_

    * after that, logout and login if requested, to update :code:`$PATH`
* Use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine
* Open a terminal in that directory
* If you have several versions of python3, and want to run on a particular one, e.g., 3.9:

    * run :code:`poetry env use 3.9`
    * replace :code:`python3` by :code:`python3.9` in the commands below
* Run :code:`poetry install`
   * Run :code:`poetry install --no-dev` if you do not plan to contribute to IDP-Z3 development

To launch the Interactive Consultant web server:

* open a terminal in that directory and run :code:`poetry run python3 main.py`

After that, you can open

* the Interactive Consultant at http://127.0.0.1:5000
* the webIDE at http://127.0.0.1:5000/IDE



Installation using pip
----------------------

IDP-Z3 can be installed using the python package ecosystem.

* install `python 3 <https://www.python.org/downloads/>`_, with `pip3 <https://pip.pypa.io/en/stable/installing/>`_, making sure that python3 is in the PATH.
* use git to clone https://gitlab.com/krr/IDP-Z3 to a directory on your machine
* (For Linux and MacOS) open a terminal in that directory and run the following commands.

.. code::

   python3 -m venv .
   source bin/activate
   python3 -m pip install -r requirements.txt

* (For Windows) open a terminal in that directory and run the following commands.

.. code::

   python3 -m venv .
   .\Scripts\activate
   python3 -m pip install -r requirements.txt

To launch the web server on Linux/MacOS, run

.. code::

   source bin/activate
   python3 main.py

On Windows, the commands are:

.. code::

   .\Scripts\activate
   python3 main.py


After that, you can open

* the Interactive Consultant at http://127.0.0.1:5000
* the webIDE at http://127.0.0.1:5000/IDE

Installation of idp_engine module
---------------------------------

The idp_engine module is available for installation through the official Python package repository.
This comes with a command line program, :code:`idp_engine` that functions as described in :ref:`CLI`.

To install the module via poetry, the following commands can be used to add the module, and then install it.

.. code::

   poetry add idp_engine
   poetry install

Installing the module via pip can be done as such:

.. code::

   pip3 install idp_engine
