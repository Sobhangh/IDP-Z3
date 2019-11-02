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

Or(Convex == True, Convex == False)

Or(Equilateral == True, Equilateral == False)

ForAll(a1,
       Implies(Large(a1),
               And(Or(a1 == 1, a1 == 2, a1 == 3, a1 == 4))))

ForAll(a1,
       Implies(Large(a1),
               And(Or(a1 == 1, a1 == 2, a1 == 3, a1 == 4))))

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
And(And(And(Angle(1) < 180, Angle(2) < 180), Angle(3) < 180),
    Angle(4) < 180)

Equilateral ==
And(And(And(Or(Length(1) == Length(1), Sides < 1),
            Or(Length(2) == Length(1), Sides < 2)),
        Or(Length(3) == Length(1), Sides < 3)),
    Or(Length(4) == Length(1), Sides < 4))

Or(Or(Or(Subtype == right_triangle,
         Subtype == regular_triangle),
      Subtype == irregular),
   Not(Sides == 3))

(Subtype == regular_triangle) ==
And(Sides == 3, Equilateral)

(Subtype == regular_triangle) ==
And(Sides == 3,
    And(And(And(Or(Angle(1) == 60, Sides < 1),
                Or(Angle(2) == 60, Sides < 2)),
            Or(Angle(3) == 60, Sides < 3)),
        Or(Angle(4) == 60, Sides < 4)))

(Subtype == right_triangle) ==
And(Sides == 3,
    Or(Or(Or(Angle(1) == 90, Angle(2) == 90),
          Angle(3) == 90),
       Angle(4) == 90))

Or(Subtype == square, Subtype == rectangle) ==
And(Sides == 4,
    And(And(And(Or(Angle(1) == 90, Sides < 1),
                Or(Angle(2) == 90, Sides < 2)),
            Or(Angle(3) == 90, Sides < 3)),
        Or(Angle(4) == 90, Sides < 4)))

Or(Not(Subtype == rectangle),
   And(And(Length(1) == Length(3), Length(2) == Length(4)),
       Not(Length(1) == Length(2))))

(Subtype == square) == And(Sides == 4, Equilateral)

Or(Not(Type == triangle),
   And(And(Length(1) <= Length(2) + Length(3),
           Length(2) <= Length(3) + Length(1)),
       Length(3) <= Length(1) + Length(2)))

Perimeter ==
If(True, Length(1), 0) +
If(True, Length(2), 0) +
If(True, Length(3), 0) +
If(True, Length(4), 0)

If(True, Angle(1), 0) +
If(True, Angle(2), 0) +
If(True, Angle(3), 0) +
If(True, Angle(4), 0) ==
ToReal((Sides - 2)*180)

And(And(And(Length(1) >= 0, Length(2) >= 0), Length(3) >= 0),
    Length(4) >= 0)

And(And(And(Angle(1) >= 0, Angle(2) >= 0), Angle(3) >= 0),
    Angle(4) >= 0)

And(And(And(Not(Angle(1) == 180), Not(Angle(2) == 180)),
        Not(Angle(3) == 180)),
    Not(Angle(4) == 180))

And(And(And((Angle(1) == 0) == (Vertices < 1),
            (Angle(2) == 0) == (Vertices < 2)),
        (Angle(3) == 0) == (Vertices < 3)),
    (Angle(4) == 0) == (Vertices < 4))

And(And(And((Length(1) == 0) == (Sides < 1),
            (Length(2) == 0) == (Sides < 2)),
        (Length(3) == 0) == (Sides < 3)),
    (Length(4) == 0) == (Sides < 4))

ForAll([ci0, cout],
       Large(ci0) ==
       Or(And(ci0 == 1, Length(1) > 10),
          And(ci0 == 2, Length(2) > 10),
          And(ci0 == 3, Length(3) > 10),
          And(ci0 == 4, Length(4) > 10)))
