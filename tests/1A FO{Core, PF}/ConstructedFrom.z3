Formula: 
And(Or(Color == red, Color == rgb(1, 1)),
    Or(Color == red,
       Color == blue,
       Color == green,
       Color == rgb(1, 1),
       Color == rgb(1, 2),
       Color == rgb(2, 1),
       Color == rgb(2, 2)),
    Or(opposite(blue) == red,
       opposite(blue) == blue,
       opposite(blue) == green,
       opposite(blue) == rgb(1, 1),
       opposite(blue) == rgb(1, 2),
       opposite(blue) == rgb(2, 1),
       opposite(blue) == rgb(2, 2)),
    Or(opposite(green) == red,
       opposite(green) == blue,
       opposite(green) == green,
       opposite(green) == rgb(1, 1),
       opposite(green) == rgb(1, 2),
       opposite(green) == rgb(2, 1),
       opposite(green) == rgb(2, 2)),
    Or(opposite(rgb(1, 2)) == red,
       opposite(rgb(1, 2)) == blue,
       opposite(rgb(1, 2)) == green,
       opposite(rgb(1, 2)) == rgb(1, 1),
       opposite(rgb(1, 2)) == rgb(1, 2),
       opposite(rgb(1, 2)) == rgb(2, 1),
       opposite(rgb(1, 2)) == rgb(2, 2)),
    Or(opposite(rgb(2, 1)) == red,
       opposite(rgb(2, 1)) == blue,
       opposite(rgb(2, 1)) == green,
       opposite(rgb(2, 1)) == rgb(1, 1),
       opposite(rgb(2, 1)) == rgb(1, 2),
       opposite(rgb(2, 1)) == rgb(2, 1),
       opposite(rgb(2, 1)) == rgb(2, 2)),
    Or(opposite(rgb(2, 2)) == red,
       opposite(rgb(2, 2)) == blue,
       opposite(rgb(2, 2)) == green,
       opposite(rgb(2, 2)) == rgb(1, 1),
       opposite(rgb(2, 2)) == rgb(1, 2),
       opposite(rgb(2, 2)) == rgb(2, 1),
       opposite(rgb(2, 2)) == rgb(2, 2)))
WDF: 
true

Model 1
==========
Color := red.
opposite := {red -> green, blue -> red, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 2
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 3
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> green, rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 4
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> rgb(1, 1), rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 5
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> rgb(2, 1), rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 6
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> rgb(2, 2), rgb(2, 1) -> red, rgb(2, 2) -> red}.


Model 7
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> blue, rgb(2, 2) -> red}.


Model 8
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> green, rgb(2, 2) -> red}.


Model 9
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> rgb(2, 2), rgb(2, 2) -> red}.


Model 10
==========
Color := red.
opposite := {red -> green, blue -> blue, green -> red, rgb(1, 1) -> rgb(1, 2), rgb(1, 2) -> blue, rgb(2, 1) -> rgb(1, 1), rgb(2, 2) -> red}.


More models may be available.  Change the max argument to see them.
