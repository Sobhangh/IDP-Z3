.. _CLI:

Command Line Interface
======================

IDP-Z3 can be run through a Command Line Interface,
using poetry (see :ref:`Installation<Installation>`):

.. code::

    poetry run python3 IDP-Z3.py path/to/file.idp

where path/to/file.idp is a relative path to the file containing the IDP program to be run.
This file must contain a :ref:`main block<main>`.

Alternatively, you can run it using pip-installed packages.

.. code::

    python3 IDP-Z3.py path/to/file.idp
