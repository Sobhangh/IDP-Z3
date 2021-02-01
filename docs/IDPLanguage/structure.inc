.. index:: structure

.. _structure:

Structure
---------
.. code::

    structure S:V {
        // here comes the structure named S, for vocabulary named V
    }

A *structure* specifies the interpretation of some predicate_\ s and function_\ s, by enumeration.
If the names are omitted, the structure is named S, for vocabulary V.

A structure is a set of enumerations, having one of the following forms:

.. math::

    P = \{~&(el_1^1, el_1^2,... el_1^n),

          &(el_2^1, el_2^2,... el_2^n),

          &..

        \}

    F = \{~&(el_1^1, el_1^2,... el_1^n) → el_1,

          &e(l_2^1, el_2^2,... el_2^n) -> el_2,

          &..

        \}~&else ~el

    Z = el.

where :math:`P` is a predicate of arity :math:`n`, :math:`F` is a function of arity :math:`n`,
and :math:`el_i^j` are constructor_\ s or numeric literals.

The first statement enumerates the tuples of terms that make the predicate :math:`P` true.
Parentheses can be omitted when the arity is 1.

The second statement specifies the value :math:`el_i^n` for the function :math:`F` applied to the tuple of :math:`el_i^j` arguments.
The element after :math:`else` specifies the function value for the non-enumerated tuples of arguments.
This default value is optional; when omitted, the value of the function for the non-enumerated tuples, if any, is unspecified.

The third statement assigns the value :math:`el` to the symbol :math:`Z` (of arity 0).

