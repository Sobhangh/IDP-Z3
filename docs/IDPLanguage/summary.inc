

Syntax summary
--------------

The following code illustrates the syntax of IDP.
T denotes a type, c a constructor, p a proposition or predicate, f a constant or function.
The equivalent ASCII-only encoding is shown on the right.

.. code::

    vocabulary V {
        type T constructed from {c1, c2}
        type T = {1;2;3}
        type T = {1..3}
        // built-in types: 𝔹, ℤ, ℝ, `Symbols      Bool, Int, Real, `Symbols

        p : ()
        p1, p2 : (T)
        f: (T) → T                                f: (T) -> T
        f1, f2: (T) → T                           f1, f2: (T) -> T

        [this is the intended meaning of p]
        p : ()

        extern vocabulary W
    }

    theory T:V {
        (¬p1∧p2 ∨ p3 ⇒ p4 ⇔ p5) ⇐ p6.             (~p1&p2 | p3 => p4 <=> p5) <= p6.
        p(f1(f2())).
        f1() < f2() ≤ f3() = f4() ≥ f5() > f6().  f1() < f2() =< f3() = f4() >= f5() > f6().
        f() ≠ c.                                  f() ~= c.
        ∀x[T]: p(x).                              !x[T]: p(x).
        ∃x: p(x).                                 ?x: p(x).

        f() in {1;2;3}.
        f() = #{x[T]: p(x)}.
        f() = sum{x[T]: p(x): f(x)}.
        if p1 then p2 else p3.
        f1() = if p then f2() else f3().

        p = {1;2;3}
        p(1) is enumerated.
        p(5) is not enumerated.

        { p(1).
          ∀x[T]: p1(x) ← p2(x).                   !x[T]: p1(x) <- p2(x).
          f(1)=1.
          ∀x: f(x)=1 ← p(x).                      !x: f(x)=1 <- p(x).
        }

        [this is the intended meaning of the rule]
        (p).
    }

    structure S:V {
        p := false
        p := {1,2,3}
        p := {1,2), (3,4)}
        p := {
        1 2
        3 4
        }

        f := 1
        f := {→1}                                 f := {-> 1}
        f := {1→1, 2→2}                           f := {1->1, 2->2}
        f := {(1,2)→3} else 2                     f := {(1,2)->3} else 2
    }

    display {
        expand(`p).
        hide(`p).
        view = expanded.
        relevant(`p1, `p2).
        goal(`p).
        optionalPropagation.
    }

    procedure main() {
        print(model_check    (T,S))
        print(model_expand   (T,S))
        print(model_propagate(T,S))
    }
