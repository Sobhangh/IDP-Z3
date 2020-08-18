.. index:: display block

Display
-------

The *display block* configures the user interface of the :ref:`Interactive Consultant<Consultant>`.
It consists of a set of *display facts*, i.e., :ref:`predicate<predicate application>` and :ref:`function applications<function application>` terminated by ``.``.

The following predicates and functions are available:

.. _expand:
.. index:: expanded view

expand
    :math:`expand(s_1, .., s_n)` specifies that :ref:`symbols<symbol>` :math:`s_1, .., s_n` are shown expanded, 
    i.e., that all sub-sentences of the theory where they occur are shown on the screen.

    For example, ``expand(`Length).`` will force the Interactive Consultant to show all sub-sentences containing `Length`.

hide
    :math:`hide(s_1, .., s_n)` specifies that symbols :math:`s_1, .., s_n` are not shown on the screen.

    For example, ``hide(`Length).`` will force the Interactive Consultant to not display the box containing `Length` information.

view
    ``view = normal.`` (default) specifies that symbols are displayed in normal mode.

    ``view = expanded.`` specifies that symbols are displayed expand_\ ed.

relevant
    :math:`relevant(s_1, .., s_n)` specifies that symbols :math:`s_1, .., s_n` are relevant, i.e. that they should never be greyed out.

    Irrelevant symbols and sub-sentences, i.e. symbols whose interpretation do not constrain the interpretation of the relevant symbols, are greyed out by the Interactive Consultant.

goal
    :math:`goal(s)` specifies that symbols :math:`s` is a goal, i.e. that it is relevant and shown expanded.

moveSymbols
    When the *display block* contains ``moveSymbols.``, the Interactive Consultant is allowed to change the layout of symbols on the screen, so that relevant symbols come first.

    By default, the symbols do not move.


