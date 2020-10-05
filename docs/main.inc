.. _main:
.. index:: main block

Main block
----------

The *main block* consists of python-like statements to be executed by the :ref:`IDP-Z3 executable<CLI>` or the Web IDE, in the context of the knowledge base.
It takes the following form:

.. code-block::

    procedure main() {
        // here comes the python-like code to be executed
    }

The vocabularies, theories and structures defined in other blocks of the IDP program are available through variables of the same name.

The following functions are available:

print(...)
    Prints the arguments on stdout

model_expand(theory, structure=None, max=10)
    Returns a list of models of the theory that are expansion of the structure.

    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.
    The result is limited to ``max`` elements (10 by default), or unlimited if ``max`` is 0.

    For example, ``print(model_expand(T, S))`` will print (up to) 10 models of theory named ``T`` expanding structure named ``S``.


