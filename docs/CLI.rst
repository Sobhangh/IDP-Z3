.. _CLI:

Command Line Interface
======================

IDP-Z3 can be run through a Command Line Interface.

If you have downloaded IDP-Z3 from the GitLab repo, you may run the CLI using poetry (see :ref:`Installation<Installation>`):

.. code::

    poetry run python3 idp-engine.py path/to/file.idp

where `path/to/file.idp` is the path to the file containing the IDP source file to be run.
This file must contain a :ref:`main block<main>`.

Alternatively, if you installed it via pip, you can run it with the following command:

.. code::

    idp-engine path/to/file.idp

The usage of the CLI is as follows:


.. code-block:: none

   usage: idp-engine.py [-h] [-o OUTPUT] [--full-formula] [--no-timing] FILE

   IDP-Z3

   positional arguments:
     FILE                  path to the .idp file

     optional arguments:
       -h, --help            show this help message and exit
       -o OUTPUT, --output OUTPUT
       name of the output file
       --full-formula        show the full formula
       --no-timing           don't display timing information
