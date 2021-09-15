.. index:: display block

Display
-------

The *display block* configures the user interface of the :ref:`Interactive Consultant<Consultant>`.
It consists of a set of *display facts*, i.e., :ref:`predicate<predicate application>` and :ref:`function applications<function application>` terminated by ``.``.

The following predicates and functions are available:

.. _expand:
.. index:: expanded view

expand
    ``expand(s1, .., sn)`` specifies that :ref:`symbols<symbol>` ``s1, .., sn`` are shown expanded,
    i.e., that all sub-sentences of the theory where they occur are shown on the screen.

    For example, ``expand(`Length).`` will force the Interactive Consultant to show all sub-sentences containing `Length`.

hide
    ``hide(s1, .., sn)`` specifies that symbols ``s1, .., sn`` are not shown on the screen.

    For example, ``hide(`Length).`` will force the Interactive Consultant to not display the box containing `Length` information.

view()
    ``view() = normal.`` (default) specifies that symbols are displayed in normal mode.

    ``view() = expanded.`` specifies that symbols are displayed expand_\ ed.

relevant
    ``relevant(s1, .., sn)`` specifies that symbols ``s1, .., sn`` are relevant, i.e. that they should never be greyed out.

    Irrelevant symbols and sub-sentences, i.e. symbols whose interpretation do not constrain the interpretation of the relevant symbols, are greyed out by the Interactive Consultant.

goal
    ``goal(s)`` specifies that symbols ``s`` is a goal, i.e. that it is relevant and shown expanded.

moveSymbols
    When the *display block* contains ``moveSymbols()``, the Interactive Consultant is allowed to change the layout of symbols on the screen, so that relevant symbols come first.

    By default, the symbols do not move.

optionalPropagation
    When the *display block* contains ``optionalPropagation()``, a toggle button will be available in the interface which allows toggling immediate propagation on and off.

    By default, this button is not present.

manualPropagation
    If ``manualPropagation()`` is present in the *display block*, automatic propagation will be disabled in the interface. Instead, a button will be added to the header that computes propagation when clicked.

optionalRelevance
    When the *display block* contains ``optionalRelevance()``, a toggle button will be available in the interface which allows toggling immediate computation of relevance on and off.

    By default, this button is not present.

manualRelevance
    If ``manualRelevance()`` is present in the *display block*, automatic computation of relevant questions will be disabled in the interface. Instead, a button will be added to the header that computes relevance when clicked.

unit
    ``unit('unitstr', s1, ..., sn)`` specifies the unit of one or more symbols.
    This unit will then show up in the symbol's header in the Interactive Consultant.
    ``unitstr`` may not be a symbol declared in the vocabulary.

    For example: ``unit('m', length, perimeter).``

heading
    Experimental: this feature is likely to change in the future.

    ``heading('label', `p1, ..., `pn)`` will force the display of the ```p1, ..., `pn`` symbols under a heading called ``label``.
    ``label`` may not be a symbol declared in the vocabulary.
