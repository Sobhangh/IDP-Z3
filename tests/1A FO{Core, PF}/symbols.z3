And(Or(Not(p), q),
    important(`p),
    important(`p),
    important(`q),
    Or(opposite(blue) == red,
       opposite(blue) == blue,
       opposite(blue) == green),
    Or(opposite(green) == red,
       opposite(green) == blue,
       opposite(green) == green),
    important(`p) == p,
    Not(important(`q)),
    And(important(`p) == p, Not(important(`q))))
