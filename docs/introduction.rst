
Introduction
============

IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the IDP language and a Z3 SMT solver.

These components together enable the creation of these solutions:

.. _Consultant:
.. index:: Interactive Consultant

* the `Interactive Consultant <https://interactive-consultant.ew.r.appspot.com/>`_, which allow a knowledge expert to enter knowledge about a particular problem domain, and an end user to interactively find solutions for particular problem instances;
* :ref:`a program<CLI>` with a command line interface to compute inferences on a knowledge base;
* a `web-based Interactive Development Environment <https://interactive-consultant.ew.r.appspot.com/IDE/>`_ (IDE) to create Knowledge bases.

The source code of IDP-Z3 is publicly available under the GNU Affero General Public License.

Installation
------------

IDP-Z3 is installed using the python package ecosystem, which supports Unix, Windows and MacOS.

* install `python 3 <https://www.python.org/downloads/>`_, with `pip3 <https://pip.pypa.io/en/stable/installing/>`_, making sure that python3 is in the PATH.
* use git to clone https://gitlab.com/krr/autoconfigz3 to a directory on your machine
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

Get started
------------

To launch the web server on Linux/MacOS, run

.. code-block::

   source bin/activate
   python3 main.py

On Windows, the commands are:

.. code-block::

   .\Scripts\activate
   python3 main.py


After that, you can open the 

* Interactive Consultant at http://127.0.0.1:5000
* web IDE at http://127.0.0.1:5000/IDE