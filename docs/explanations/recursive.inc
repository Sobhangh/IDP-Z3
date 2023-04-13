.. _recursive_datatypes:

Recursive datatypes
-------------------

A recursive data type is a datatype
whose constructor accepts arguments of the type being declared.
An idiomatic example is a list of Int:

.. code::

    type List := constructed from {nil, cons(car:Int, cdr: List)}

Note that this List only contains Int.
A different type declaration must be used for lists of other types (with different constructors).

A list ``[1, 2, 3]`` can be constructed as follows:

.. code::

    cons(1, cons(2, cons(3, nil)))

The length of the list can be computed using a recursive definition:

.. code::

    len: (List) -> Int // in vocabulary block


    // in definition block
    { (recursive)
      len(nil) = 0.
      ! x in List: len(x) = len(cdr(x))+1 <- is_cons(x).
    }

The ``(recursive)`` keyword is required to avoid non-terminating model search on satisfiable theories.
Model search for an unsatisfiable theory with recursive definitions
usually do not terminate, as the reasoning engine considers ever longer lists.
This prevents the use of recursive datatypes for propagation and explanation problems,
and thus in the Interactive Consultant.

Recursive datatypes and recursive definitions are natively supported
by the Z3 solver that powers the IDP-Z3 reasoning engine.

Here is a definition of ``membership``:

.. code::

    member: Int * List -> Bool // in vocabulary block

    { (recursive)
      ! x in Int, l in List: member(x,l) <- is_cons(l) & car(l)=x.
      ! x in Int, l in List: member(x,l) <- is_cons(l) & member(x, cdr(l)).
    }

A definition can be used to express that the numbers in a list are positive.

.. code::

    positive: List -> Bool
    l: () -> List

    { (recursive)
      ! x in List: positive(x) <- is_nil(x).
      ! x in List: positive(x) <- is_cons(x) & 0 < car(x) & positive(cdr(x)).
    }
    positive(l()).

(At some point, we might provide a generic List type,
with quantification over the list:  ``! x in l(): 0 < x.``.)

Here is a complete code example, to find a list of 2 positive Integers
that are in increasing order, and containing 1 and 2:

.. code::

    vocabulary V {
        type List1 := constructed from {nil1, cons1(car1:Int, cdr1: List1)}
        a: () -> List1
        len1: List1 -> Int
        increasing, positive: List1 -> Bool
        member: Int*List1 -> Bool
    }

    theory T:V {

        { (recursive)
          len1(nil1) = 0.
          ! x in List1: len1(x) = len1(cdr1(x))+1 <- is_cons1(x). }

        // between 1 and 2
        { (recursive)
          ! x in List1: positive(x) <- is_nil1(x).
          ! x in List1: positive(x) <- is_cons1(x) & 0<car1(x)<3 & positive(cdr1(x)).
        }

        { (recursive)
        ! l in List1, x in Int: member(x,l) <- is_cons1(l) & car1(l)=x.
          ! x in Int, l in List1: member(x,l) <- is_cons1(l) & member(x, cdr1(l)).
        }

        { (recursive)
        ! x in List1: increasing(x) <- x = nil1.
        ! x in List1: increasing(x) <- is_cons1(x) & is_nil1(cdr1(x)).
        ! x in List1: increasing(x) <- is_cons1(x) & increasing(cdr1(x))
                & is_cons1(cdr1(x)) & car1(x) < car1(cdr1(x)).}

        len1(a()) = 2.  //a() has 2 elements
        positive(a()).  // the elements in a() are positive
        increasing(a()). // the elements in a() are increasing
        member(1, a()) | member(2, a()).  // 1 and 2 are elements in a()
    }

    procedure main() {
        print(Theory(T).sexpr())
        pretty_print(model_expand(T, max=1, sort=True))
    }

Its output is:

.. code::

    Model 1
    ==========
    a := cons1(1, cons1(2, nil1)).




