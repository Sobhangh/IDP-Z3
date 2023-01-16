.. _webIDE:

webIDE
-------

The webIDE of IDP-Z3 is accessible `online <https://interactive-consultant.idp-z3.be/IDE>`_, and can be :ref:`run locally <Installation>`.

The webIDE allows you to enter an IDP-Z3 program, with :ref:`FO-dot <FO-dot>` `vocabulary, theory, structure` blocks and a :ref:`main block <main>`, and to run it.

.. _main:
.. index:: main block

Main block
++++++++++

The *main block* consists of python-like statements
to be executed by the :ref:`IDP-Z3 executable<CLI>` or the :ref:`webIDE <webIDE>`,
in the context of the knowledge base.
Below is an example of a main block.

.. code-block:: python

    procedure main() {
        pretty_print(Theory(T, S).propagate())
        duration("End")
    }

Within that block, the following variables, classes and functions are available:

    - variables containing the vocabularies, theories and structures specified in the same IDP-Z3 program.  The variables have the name of the block;
    - the functions exposed by the ``idp_engine``, described :ref:`here <idp_engine>`;
    - the ``Theory`` class, described :ref:`here <Theory>`;
    - Python's `logging <https://docs.python.org/3/library/logging.html>`_ package.



.. _IDP_functions:

``idp_engine`` functions
++++++++++++++++++++++++

.. automodule:: idp_engine.Run
    :members:
    :exclude-members: execute



.. _Theory_class:

Theory class
+++++++++++++

Instances of the ``Theory`` class represent a collection of theory and structure blocks.

Many operations on Theory instances can be chained, e.g., ``Theory(T,S).propagate().simplify().formula()``.

The class has the following methods:

.. autoclass:: idp_engine.Theory.Theory
    :members:

.. _idp_engine:

