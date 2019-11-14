Or(Sides == 3, Sides == 4)

Or(Vertices == 3, Vertices == 4)

ForAll(c!0,
       Implies(Large(c!0),
               And(Or(c!0 == 1,
                      c!0 == 2,
                      c!0 == 3,
                      c!0 == 4))))
--
And(If(False, 4, If(False, 3, If(True, 2, If(False, 1, 5)))) >
    1,
    If(False, 4, If(True, 3, If(False, 2, If(False, 1, 5)))) >
    2,
    If(True, 4, If(False, 3, If(False, 2, If(False, 1, 5)))) >
    3,
    If(False,
       4,
       If(False, 3, If(False, 2, If(False, 1, 5)))) >
    4)

(Type == triangle) == (Sides == 3)

(Type == quadrilateral) == (Sides == 4)

And((Vertices == 3) == (Sides == 3),
    (Vertices == 4) == (Sides == 4))

Or(Not(Sides == 3), Convex)

Convex ==
And(Angle(1) < 180,
    Angle(2) < 180,
    Angle(3) < 180,
    Angle(4) < 180)

Equilateral ==
And(Or(True, Sides < 1),
    Or(False, Sides < 2),
    Or(False, Sides < 3),
    Or(False, Sides < 4))

Or(Or(Subtype == right_triangle,
      Subtype == regular_triangle,
      Subtype == irregular),
   Not(Sides == 3))

(Subtype == regular_triangle) ==
And(Sides == 3, Equilateral)

(Subtype == regular_triangle) ==
And(Sides == 3,
    And(Or(Angle(1) == 60, Sides < 1),
        Or(Angle(2) == 60, Sides < 2),
        Or(Angle(3) == 60, Sides < 3),
        Or(Angle(4) == 60, Sides < 4)))

(Subtype == right_triangle) ==
And(Sides == 3,
    Or(Angle(1) == 90,
       Angle(2) == 90,
       Angle(3) == 90,
       Angle(4) == 90))

Or(Subtype == square, Subtype == rectangle) ==
And(Sides == 4,
    And(Or(Angle(1) == 90, Sides < 1),
        Or(Angle(2) == 90, Sides < 2),
        Or(Angle(3) == 90, Sides < 3),
        Or(Angle(4) == 90, Sides < 4)))

Or(Not(Subtype == rectangle), And(False, False, Not(False)))

(Subtype == square) == And(Sides == 4, Equilateral)

Or(Not(Type == triangle), And(True, True, True))

Perimeter ==
ToReal(If(True, 1, 0) +
       If(True, 2, 0) +
       If(True, 3, 0) +
       If(True, 4, 0))

If(True, Angle(1), 0) +
If(True, Angle(2), 0) +
If(True, Angle(3), 0) +
If(True, Angle(4), 0) ==
ToReal((Sides - 2)*180)

And(True, True, True, True)

And(Angle(1) >= 0,
    Angle(2) >= 0,
    Angle(3) >= 0,
    Angle(4) >= 0)

And(Not(Angle(1) == 180),
    Not(Angle(2) == 180),
    Not(Angle(3) == 180),
    Not(Angle(4) == 180))

And((Angle(1) == 0) == (Vertices < 1),
    (Angle(2) == 0) == (Vertices < 2),
    (Angle(3) == 0) == (Vertices < 3),
    (Angle(4) == 0) == (Vertices < 4))

And((Sides < 1) == False,
    (Sides < 2) == False,
    (Sides < 3) == False,
    (Sides < 4) == False)

ForAll(c!14,
       Large(c!14) ==
       Or(And(c!14 == 1, False),
          And(c!14 == 2, False),
          And(c!14 == 3, False),
          And(c!14 == 4, False)))
