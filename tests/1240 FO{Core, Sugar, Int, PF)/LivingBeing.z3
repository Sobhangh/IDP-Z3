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


Model 2
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Dog, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->21, Dog->20, Frog->20, Alice->20, Bob->20, Tom->2}.


Model 3
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->19, Dog->19, Frog->19, Alice->19, Bob->19, Tom->19}.


Model 4
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->0, Dog->0, Frog->3, Alice->20, Bob->0, Tom->0}.


Model 5
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->-1, Dog->-1, Frog->-1, Alice->20, Bob->-1, Tom->-1}.


Model 6
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->-2, Dog->4, Frog->-2, Alice->-2, Bob->-2, Tom->-2}.


Model 7
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->21, Dog->0, Frog->5, Alice->20, Bob->0, Tom->6}.


Model 8
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->0, Dog->0, Frog->7, Alice->0, Bob->0, Tom->8}.


Model 9
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->21, Dog->0, Frog->9, Alice->20, Bob->0, Tom->10}.


Model 10
==========
animal := {Cat, Dog, Frog}.
person := {Alice, Bob, Tom}.
married := {}.
spouse := {Cat->Cat, Dog->Cat, Frog->Cat, Alice->Bob, Bob->Alice, Tom->Cat}.
age := {Cat->20, Dog->20, Frog->11, Alice->20, Bob->0, Tom->12}.


More models may be available.  Change the max argument to see them.
