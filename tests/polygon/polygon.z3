Or(Sides == 3, Sides == 4)

Or(Vertices == 3, Vertices == 4)

Or(Type == triangle, Type == quadrilateral)

True

True

True

True

True

True

True

True

Or(Subtype == regular_triangle,
   Subtype == right_triangle,
   Subtype == rectangle,
   Subtype == square,
   Subtype == irregular)

ForAll(a1,
       Implies(Large(a1),
               And(Or(a1 == 1, a1 == 2, a1 == 3, a1 == 4))))
--
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

ForAll(c!12,
       Large(c!12) ==
       Or(And(c!12 == 1, False),
          And(c!12 == 2, False),
          And(c!12 == 3, False),
          And(c!12 == 4, False)))
