And(spouse(Alice) == Bob,
    spouse(Bob) == Alice,
    Or(Not(married(Alice)), 20 < age(Bob)),
    Or(Not(married(Bob)), 20 < age(Alice)),
    Or(Not(married(Tom)), 20 < age(spouse(Tom))))

Model 1
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->21, Dog->21, Frog->21, Alice->21, Bob->21, Tom->21}.


More models may be available.  Change the max argument to see them.
