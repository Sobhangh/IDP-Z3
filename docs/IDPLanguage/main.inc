.. _main:
.. index:: main block

Main block
++++++++++

The *main block* consists of python-like statements
to be executed by the :ref:`IDP-Z3 executable<CLI>` or the :ref:`webIDE <webIDE>`,
in the context of the knowledge base.
It takes the following form:

.. code::

    procedure main() {
        // here comes the python-like code to be executed
    }

Within that block, the following variables, classes and functions are available:

    - variables containing the vocabularies, theories and structures specified in the same IDP-Z3 program.  The variables have the name of the block.
    - the ``Theory`` class, described :ref:`here <Theory>`;
    - the functions exposed by the ``idp_engine``, described :ref:`here <idp_engine>`.

Below is an example of a main block.

.. code-block:: python

    procedure main() {
        pretty_print(Theory(T, S).propagate())
        duration("End")
    }

