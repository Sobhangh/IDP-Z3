.. index:: display block

Display block
-------------

The *display block* configures the user interface of the :ref:`Interactive Consultant<Consultant>`.
It consists of a set of *display facts*, i.e., :ref:`predicate<predicate application>` and :ref:`function applications<function application>` terminated by ``.``.

The following predicates and functions are available:

.. _expand:
.. index:: expanded view

expand
    ``expand(`s1, .., `sn)`` specifies that :ref:`symbols<symbol>` ``s1, .., sn`` are shown expanded,
    i.e., that all sub-sentences of the theory where they occur are shown on the screen.

    For example, ``expand(`length).`` will force the Interactive Consultant to show all sub-sentences containing `length`.

hide
    ``hide(`s1, .., `sn)`` specifies that symbols ``s1, .., sn`` are not shown on the screen.

    For example, ``hide(`length).`` will force the Interactive Consultant to not display the box containing `length` information.

view()
    ``view() = normal.`` (default) specifies that symbols are displayed in normal mode.

    ``view() = expanded.`` specifies that symbols are displayed expanded.

goal_symbol
    ``goal_symbol := {`s1, .., `sn}`` specifies that symbols ``s1, .., sn`` are always relevant, i.e. that they should never be greyed out.
    ``goal_symbol`` can only be used in an enumeration.

    Irrelevant symbols and questions, i.e. expressions whose interpretation do not constrain the interpretation of the relevant symbols,
    are greyed out by the Interactive Consultant.

moveSymbols
    When the *display block* contains ``moveSymbols()``, the Interactive Consultant is allowed to change the layout of symbols on the screen, so that relevant symbols come first.

    By default, the symbols do not move.

optionalPropagation
    When the *display block* contains ``optionalPropagation()``, a toggle button is shown next to the menu to allow toggling immediate propagation on and off.

    By default, this button is not present.

manualPropagation
    When ``manualPropagation()`` is present in the *display block*, automatic propagation is disabled in the interface. Instead, a button is added to the menu that computes propagation when clicked.

optionalRelevance
    When the *display block* contains ``optionalRelevance()``, a toggle button is shown next to the menu to allow toggling immediate computation of relevance on and off.

    By default, this button is not present.

manualRelevance
    When ``manualRelevance()`` is present in the *display block*, automatic computation of relevant questions is disabled in the interface. Instead, a menu option is available in the "Reasoning" menu that computes relevance when selected.

unit
    ``unit('unitstr', `s1, ..., `sn)`` specifies the unit of one or more symbols.
    This unit will then show up in the symbol's header in the Interactive Consultant.
    ``unitstr`` may not be a symbol declared in the vocabulary.

    For example: ``unit('m', `length, `perimeter).``

heading
    Experimental: this feature is likely to change in the future.

    ``heading('label', `p1, ..., `pn)`` will force the display of the ``p1, ..., pn`` symbols under a heading called ``label``.
    ``label`` may not be a symbol declared in the vocabulary.

noOptimization
    ``noOptimization(`s1, .., `sn)`` specifies that no optimization buttons appear in the Interactive Consultant for symbols ``s1, .., sn``.

    For example, ``noOptimization(`angle).`` will hide the arrow up and arrow down buttons next to the input fields for `angle`.
