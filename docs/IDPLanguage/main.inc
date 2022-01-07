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

The following functions are also available:


model_check(theory, structure=None)
    Returns string ``sat``, ``unsat`` or ``unknown``, depending on whether the theory has a model expanding the structure.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.

    For example, ``print(model_check(T, S))`` will print ``sat`` if theory named ``T`` has a model expanding structure named ``S``.


model_expand(theory, structure=None, max=10, timeout=10, complete=False)
    Returns a (possibly empty) list of models of the theory that are expansion of the structure, possibly followed by a string message.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.
    The result is limited to ``max`` models (10 by default), or unlimited if ``max`` is 0.
    The search for new models is stopped when processing exceeds ``timeout`` (in seconds) (unless it is 0).
    The models can be asked to be complete or partial (i.e., in which "don't care" terms are not specified).

    The string message can be one of the following:

    - ``No models.``

    - ``More models may be available.  Change the max argument to see them.``

    - ``More models may be available.  Change the timeout argument to see them.``

    - ``More models may be available.  Change the max and timeout arguments to see them.``

    For example, ``print(model_expand(T, S))`` will print (up to) 10 models of theory named ``T`` expanding structure named ``S``.


model_propagate(theory, structure=None)
    Returns a list of assignments that are true in any expansion of the structure consistent with the theory.
    ``theory`` and ``structure`` can be lists, in which case their elements are merged.
    The structure is optional.
    Terms and symbols starting with '_' are ignored.

    For example, ``print(model_propagate(T, S))`` will print the assignments that are true in any expansion of the structure named ``S`` consistent with the theory named ``T``.

decision_table(theories, structures=None, goal_string="", timeout=20, max_rows=50, first_hit=True)
    Experimental.  Returns the rows for a decision table that defines ``goal_string``.
    ``goal_string`` must be a predicate application defined in the theory.

pretty_print(...)
    Prints its argument on stdout, in a readable form.


Theory class
+++++++++++++

The main block can also use instances of the ``Theory`` class.
This is beneficial when several inferences must be made in a row (e.g., ``Theory(T,S).propagate().simplify().formula()``).
Instances of the ``Theory`` class represent a collection of theory and structure blocks.
The class has the following methods:

.. autoclass:: idp_engine.Problem.Theory
    :members:
    :noindex:
