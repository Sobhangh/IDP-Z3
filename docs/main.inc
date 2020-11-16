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


model_check(theory, structure=None)
    Returns string ``sat``, ``unsat`` or ``unknown``, depending on whether the theory has a model expanding the structure.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.

    For example, ``print(model_check(T, S))`` will print ``sat`` if theory named ``T`` has a model expanding structure named ``S``.


model_expand(theory, structure=None, max=10, complete=False)
    Returns a list of models of the theory that are expansion of the structure.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.
    The result is limited to ``max`` models (10 by default), or unlimited if ``max`` is 0.
    The models can be asked to be complete or partial (i.e., in which "don't care" terms are not specified).

    For example, ``print(model_expand(T, S))`` will print (up to) 10 models of theory named ``T`` expanding structure named ``S``.


model_propagate(theory, structure=None)
    Returns a list of assignments that are true in any expansion of the structure consistent with the theory.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.
    Terms and symbols starting with '_' are ignored.

    For example, ``print(model_propagate(T, S))`` will print the assignments that are true in any expansion of the structure named ``S`` consistent with the theory named ``T``.


print(...)
    Prints the arguments on stdout


Problem class
+++++++++++++

The main block can also use instances of the ``Problem`` class.
This is beneficial when several inferences must be made in a row (e.g., ``Problem(T,S).propagate().simplify().formula()``).
Instances of the ``Problem`` class represent a collection of theory and structure blocks.
The class has the following methods:

__init__(self, \*blocks)
    Creates an instance of ``Problem`` for the list of blocks, e.g., ``Problem(T,S)``

add(self, block)
    Adds a theory or structure block to the problem.

copy(self)
    Returns an independent copy of a problem.

formula(self)
    Returns a python object representing the logic formula equivalent to the problem.
    This object can be converted to a string using ``str()``.

expand(self, max=10, complete=False)
    Returns a list of models of the theory that are expansion of the known assignments.
    The result is limited to ``max`` models (10 by default), or unlimited if ``max`` is 0.
    The models can be asked to be complete or partial (i.e., in which "don't care" terms are not specified).

optimize(self, term, minimize=True, complete=False)
    Returns the problem with its ``assignments`` property updated with values such that the term is minimized (or maximized if ``minimize`` is ``False``)
    ``term`` is a string (e.g. ``"Length(1)"``).
    The models can be asked to be complete or partial (i.e., in which "don't care" terms are not specified).

symbolic_propagate(self)
    Returns the problem with its ``assignments`` property updated with direct consequences of the constraints of the problem.
    This propagation is less complete than ``propagate()``.

propagate(self)
    Returns the problem with its ``assignments`` property updated with values for all terms and atoms that have the same value in every model (i.e., satisfying structure of the problem).
    Terms and propositions starting with '_' are ignored.

simplify(self)
    Returns the problem with a simplified formula of the problem, by substituting terms and atoms by their values specified in a structure or obtained by propagation.