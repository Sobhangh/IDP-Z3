
Introduction
============

IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the IDP language and a Z3 SMT solver.

These components together enable the creation of these solutions:

.. _Consultant:
.. index:: Interactive Consultant

* the Interactive Consultant, which allow a knowledge expert to enter knowledge about a particular problem domain, and an end user to interactively find solutions for particular problem instances;
* :ref:`a program<CLI>` with a command line interface to compute inferences on a knowledge base;
* (to be developed) a web-based Interactive Development Environment (IDE) to create Knowledge bases.

The source code of IDP-Z3 is publicly available under the GNU Affero General Public License.

Installation
------------

IDP-Z3 is installed using the python package ecosystem, which supports Unix, Windows and MacOS.

* install `python 3 <https://www.python.org/downloads/>`_, with `pip3 <https://pip.pypa.io/en/stable/installing/>`_, making sure that python3 is in the PATH.
* optional: create a `virtual environment <https://pypi.org/project/virtualenv/>`_
* use git to clone https://gitlab.com/krr/autoconfigz3 to a directory on your machine
* open a terminal (or command prompt) in that directory and run the following commands to launch the Interactive Consultant locally.

.. code-block::

   python3 -m pip install -r requirements.txt
   python3 main.py

* open http://127.0.0.1:5000/ in your favorite browser to start the Interactive Consultant.


