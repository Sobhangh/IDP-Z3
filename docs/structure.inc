.. index:: structure

Structure
---------

A *structure* specifies the interpretation of some predicate_\ s and function_\ s.
A structure is a set of enumerations, having one of the following forms:

.. math::

    P = \{~&el_1^1, el_1^2,... el_1^n;

          &el_2^1, el_2^2,... el_2^n; 

          &..

        \}

    F = \{~&el_1^1, el_1^2,... el_1^n, el_1;

          &el_2^1, el_2^2,... el_2^n, el_2; 

          &..

        \}~&else ~el

    Z = el.

where :math:`P` is a predicate of arity :math:`n`, :math:`F` is a function of arity :math:`n`,
and :math:`el_i^j` are constructor_\ s or numeric literals.

The first statement enumerates the tuples of terms that make the predicate :math:`P` true. 

The second statement specifies the value :math:`el_i^n` for the function :math:`F` applied to the tuple of :math:`el_i^j` arguments.
The element after :math:`else` specifies the function value for the non-enumerated tuples of arguments.

The third statement assigns the value :math:`el` to the symbol :math:`Z` (of arity 0).

