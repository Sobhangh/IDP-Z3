And(Or(Not(married(Alice)), 20 < age(Bob)),
    Or(Not(married(Bob)), 20 < age(Alice)),
    Or(Not(married(Tom)), 20 < age(spouse(Tom))),
    Not(And(married(Alice), affair(Alice, Bob))),
    Not(And(married(Alice), affair(Alice, Tom))),
    Not(And(married(Bob), affair(Bob, Alice))),
    Not(And(married(Bob), affair(Bob, Tom))),
    Not(And(married(Tom), affair(Tom, Alice))),
    Not(And(married(Tom), affair(Tom, Bob))),
    Or(And(married(Alice), affair(Alice, Alice)),
       And(married(Alice), affair(Alice, Bob)),
       And(married(Alice), affair(Alice, Tom)),
       And(married(Bob), affair(Bob, Alice)),
       And(married(Bob), affair(Bob, Bob)),
       And(married(Bob), affair(Bob, Tom)),
       And(married(Tom), affair(Tom, Alice)),
       And(married(Tom), affair(Tom, Bob)),
       And(married(Tom), affair(Tom, Tom))),
    ForAll(c!0,
           Or(Not(is(marriage, c!0)),
              Marriage(c!0) ==
              And(Or(A(c!0) == Tom,
                     Or(A(c!0) == Bob, A(c!0) == Alice)),
                  married(A(c!0))))),
    married(Bob),
    married(Alice),
    Not(married(Tom)),
    Or(Not(married(Alice)), married(Bob)),
    Or(Not(married(Bob)), married(Alice)),
    Or(Not(married(Tom)),
       And(married(spouse(Tom)),
           Or(spouse(Tom) == Alice,
              spouse(Tom) == Bob,
              spouse(Tom) == Tom))))

Model 1
==========
married := {Alice, Bob}.
spouse := {Alice -> Bob, Bob -> Alice}.
affair := {(Alice, Alice)}.
age := {Cat -> 21, Dog -> 21, Frog -> 21, Alice -> 21, Bob -> 21, Tom -> 21}.


More models may be available.  Change the max argument to see them.
