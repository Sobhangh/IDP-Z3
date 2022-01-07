.. _main:
.. index:: main block

Main block
----------

The *main block* consists of python-like statements to be executed by the :ref:`IDP-Z3 executable<CLI>` or the Web IDE, in the context of the knowledge base.
It takes the following form:

.. code::

    procedure main() {
        // here comes the python-like code to be executed
    }

Within that block, the vocabularies, theories and structures defined in other blocks of the IDP-Z3 program are available through variables of the same name.


.. automodule:: idp_engine.Run
    :members:
    :noindex:



Theory class
+++++++++++++

The main block can also use instances of the ``Theory`` class.
This is beneficial when several inferences must be made in a row (e.g., ``Theory(T,S).propagate().simplify().formula()``).
Instances of the ``Theory`` class represent a collection of theory and structure blocks.
The class has the following methods:

.. autoclass:: idp_engine.Problem.Theory
    :members:
    :noindex:
