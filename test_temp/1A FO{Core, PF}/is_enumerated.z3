T, S

Model 1
==========
Color := blue.
opposite := {red -> green, blue -> blue, green -> green}.
f := {(A, A) -> A, (A, B) -> A, (B, A) -> B, (B, B) -> A}.


Model 2
==========
Color := blue.
opposite := {red -> green, blue -> blue, green -> green}.
f := {(A, A) -> A, (A, B) -> A, (B, A) -> B, (B, B) -> B}.


No more models.
propagate
And(Color == blue,
    opposite(blue) == blue,
    Not(Or(Color == green, Color == red)),
    Or(f(B, B) == A, f(B, B) == B))
T, S2
No models.
T2, S

Model 1
==========
Color := green.
opposite := {red -> green, blue -> green, green -> green}.
f := {(A, A) -> A, (A, B) -> A, (B, A) -> B, (B, B) -> A}.


Model 2
==========
Color := green.
opposite := {red -> green, blue -> green, green -> green}.
f := {(A, A) -> A, (A, B) -> A, (B, A) -> B, (B, B) -> B}.


No more models.
T4, S2

Model 1
==========
Color := blue.


No more models.
T5, S2
No models.
