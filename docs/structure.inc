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

where :math:`P` is a predicate of arity :math:`n`, :math:`F` is a function of arity :math:`n`,
and :math:`el_i^j` are constructor_\ s or numeric literals.
For function :math:`F`, :math:`el_i^n` specify the values of the function for the preceding tuple of :math:`el_i^j` arguments, 
and the element after :math:`else` specifies the value of the function for non-enumerated tuples of arguments.

