

Appendix: Syntax summary
========================

The following code illustrates the syntax of the various blocks used in IDP-Z3.

T denotes a type, c a constructor, p a proposition or predicate, f a constant or function.
The equivalent ASCII-only encoding is shown on the right.

.. code::

    vocabulary V {
        type T
        type T := {c1, c2, c3}
        type T := constructed from {c1, c2(T1, f:T2)}
        type T := {1,2,3}
        type T := {1..3}
        // built-in types: 𝔹, ℤ, ℝ, Date, Concept Bool, Int, Real, Date, Concept

        p : () → 𝔹                                p: () -> Bool
        p1, p2 : T1 ⨯ T2 → 𝔹                      p1, p2: T1*T2 -> Bool
        f: T → T                                  f: T -> T
        f1, f2: Concept[T1->T2] → T               f1, f2: Concept[T1->T2] -> T

        [this is the intended meaning of p]
        p : () → 𝔹

        import W
    }

    theory T:V {
        (¬p1()∧p2() ∨ p3() ⇒ p4() ⇔ p5()) ⇐ p6(). (~p1()&p2() | p3() => p4() <=> p5()) <= p6().
        p(f1(f2())).
        f1() < f2() ≤ f3() = f4() ≥ f5() > f6().  f1() < f2() =< f3() = f4() >= f5() > f6().
        f() ≠ c.                                  f() ~= c.
        ∀x,y ∈ T: p(x,y).                         !x,y in T: p(x,y).
        ∀x ∈ p, (y,z) ∈ q: q(x,x) ∨ p(y) ∨ p(z).  !x in p, (y,z) in q: q(x,x) | p(y) | p(z).
        ∃x ∈ Concept[()→B]: $(x)().               ?x in Concept[()->B]: $(x)().
        ∃x: p(x).                                 ?x: p(x).


        f() in {1,2,3}.
        f() = #{x∈T: p(x)}.                       f() = #{x in T: p(x)}.
        f() = sum(lambda x∈T: f(x)).              f() = sum(lambda x in T: f(x)).
        if p1() then p2() else p3().
        f1() = if p() then f2() else f3().

        p := {1,2,3}.
        p(#2020-01-01) is enumerated.
        p(#TODAY) is not enumerated.

        { p(1).
          ∀x∈T: p1(x) ← p2(x).                    !x in T: p1(x) <- p2(x).
          f(1)=1.
          ∀x: f(x)=1 ← p(x).                      !x: f(x)=1 <- p(x).
        }

        [this is the intended meaning of the rule]
        p().
    }

    structure S:V {
        p := false.
        p := {1,2,3}.
        p := {0..9, 100}.
        p := {#2021-01-01}.
        p := {(1,2), (3,4)}.
        p := {
        1 2
        3 4
        }.

        f := 1.
        f := {→1} .                               f := {-> 1}.
        f := {1→1, 2→2}.                          f := {1->1, 2->2}.
        f := {(1,2)→3} else 2.                    f := {(1,2)->3} else 2.
        f :>= {(1,2)→3}.                          f :⊇ {(1,2)->3}.
    }

    display {
        goal_symbol := {`p1, `p2}.
        hide(`p).
        expand := {`p}.
        view() = expanded.
        optionalPropagation().
    }

    procedure main() {
        pretty_print(model_check    (T,S))
        pretty_print(model_expand   (T,S))
        pretty_print(model_propagate(T,S))
    }

See also the :ref:`built-in functions`.