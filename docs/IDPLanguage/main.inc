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

__init__(self, \*blocks, extended=False)
    Creates an instance of ``Theory`` for the list of blocks, e.g., ``Theory(T,S)``.

    Use `extended=True` when the truth value of inequalities and quantified formula is of interest (e.g. for the Interactive Consultant).

add(self, \*blocks)
    Adds a list of theory or structure blocks to the problem.

assert_(self, code: str, value: Any)
    Asserts that an expression has a value, e.g. `problem.assert_("p()", True)`.

copy(self)
    Returns an independent copy of a problem.

formula(self)
    Returns a Z3 object representing the logic formula equivalent to the problem.
    This object can be converted to a string using ``str()``.

expand(self, max=10, timeout=10, complete=False)
    Returns a list of models of the theory that are expansion of the known assignments.
    The result is limited to ``max`` models (10 by default), or unlimited if ``max`` is 0.
    The search for new models is stopped when processing exceeds ``timeout`` (in seconds) (unless it is 0).
    The models can be asked to be complete or partial (i.e., in which "don't care" terms are not specified).

optimize(self, term, minimize=True)
    Updates the Theory so that the value of term in the ``assignments`` property is the minimal (or maximal if ``minimize`` is ``False``) value that is compatible with the Theory.
    ``term`` is a string (e.g. ``"Length(1)"``).

symbolic_propagate(self)
    Returns the problem with its ``assignments`` property updated with direct consequences of the constraints of the problem.
    This propagation is less complete than ``propagate()``.

propagate(self)
    Returns the problem with its ``assignments`` property updated with values for all terms and atoms that have the same value in every model (i.e., satisfying structure of the problem).
    Terms and propositions starting with '_' are ignored.

get_range(self, term:str)
    Returns a list of the possible values of the term (as strings).

explain(self, consequence=None)
    Returns the facts and laws to explain a consequence in the Theory.

    The string ``consequence`` must be a key in the ``assignments`` property of the Theory, or ``None``.
    If it is ``None``, and the theory is unsatisfiable, the method returns a minimal set of facts and laws that make it so.
    The facts are a list of Assignment, and the laws are a list of ``Expression``.

simplify(self)
    Returns a simpler copy of the problem, with a simplified formula obtained
    by substituting terms and atoms by their known values.

decision_table(self, goal_string="", timeout=20, max_rows=50, first_hit=True)
    Experimental.  Returns the rows for a decision table that defines ``goal_string``.
    ``goal_string`` must be a predicate application defined in the theory.
    The problem must be created with ``extended=True``.

duration(msg: str)
    Returns the processing time since the last call to `duration()`,
    or since the begining of execution, followed by the msg (possibly an f-string)