Or(Type == triangle, Type == quadrilateral)

Or(Subtype == regular_triangle,
   Subtype == right_triangle,
   Subtype == rectangle,
   Subtype == square)

ForAll([a1, a2],
       Implies(isa(a1, a2),
               And(Or(a1 == regular_triangle,
                      a1 == right_triangle,
                      a1 == rectangle,
                      a1 == square),
                   Or(a2 == triangle, a2 == quadrilateral))))

ForAll([a1, a2],
       Implies(asi(a1, a2),
               And(Or(a1 == triangle, a1 == quadrilateral),
                   Or(a2 == regular_triangle,
                      a2 == right_triangle,
                      a2 == rectangle,
                      a2 == square))))

Or(typeOf(regular_triangle) == triangle,
   typeOf(regular_triangle) == quadrilateral)

Or(typeOf(right_triangle) == triangle,
   typeOf(right_triangle) == quadrilateral)

Or(typeOf(rectangle) == triangle,
   typeOf(rectangle) == quadrilateral)

Or(typeOf(square) == triangle,
   typeOf(square) == quadrilateral)
--
And(And(And(And(And(And(And(asi(triangle, regular_triangle) ==
                            True,
                            asi(quadrilateral,
                                regular_triangle) ==
                            False),
                        asi(triangle, right_triangle) ==
                        True),
                    asi(quadrilateral, right_triangle) ==
                    False),
                asi(triangle, rectangle) == False),
            asi(quadrilateral, rectangle) == True),
        asi(triangle, square) == False),
    asi(quadrilateral, square) == True)

And(And(And(And(And(And(And((typeOf(regular_triangle) ==
                             triangle) ==
                            True,
                            (typeOf(regular_triangle) ==
                             quadrilateral) ==
                            False),
                        (typeOf(right_triangle) == triangle) ==
                        True),
                    (typeOf(right_triangle) == quadrilateral) ==
                    False),
                (typeOf(rectangle) == triangle) == False),
            (typeOf(rectangle) == quadrilateral) == True),
        (typeOf(square) == triangle) == False),
    (typeOf(square) == quadrilateral) == True)

And(And(And(If(typeOf(regular_triangle) == triangle,
               True,
               False),
            If(typeOf(right_triangle) == triangle,
               True,
               False)),
        If(typeOf(rectangle) == quadrilateral, True, False)),
    If(typeOf(square) == quadrilateral, True, False))

Type == typeOf(Subtype)
