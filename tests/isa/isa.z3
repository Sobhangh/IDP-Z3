ForAll([c!16, c!17],
       Implies(isa(c!16, c!17),
               And(Or(c!16 == regular_triangle,
                      c!16 == right_triangle,
                      c!16 == rectangle,
                      c!16 == square),
                   Or(c!17 == triangle,
                      c!17 == quadrilateral))))

ForAll([c!18, c!19],
       Implies(asi(c!18, c!19),
               And(Or(c!18 == triangle,
                      c!18 == quadrilateral),
                   Or(c!19 == regular_triangle,
                      c!19 == right_triangle,
                      c!19 == rectangle,
                      c!19 == square))))
--
And(asi(triangle, regular_triangle) == True,
    asi(quadrilateral, regular_triangle) == False,
    asi(triangle, right_triangle) == True,
    asi(quadrilateral, right_triangle) == False,
    asi(triangle, rectangle) == False,
    asi(quadrilateral, rectangle) == True,
    asi(triangle, square) == False,
    asi(quadrilateral, square) == True)

And((typeOf(regular_triangle) == triangle) == True,
    (typeOf(regular_triangle) == quadrilateral) == False,
    (typeOf(right_triangle) == triangle) == True,
    (typeOf(right_triangle) == quadrilateral) == False,
    (typeOf(rectangle) == triangle) == False,
    (typeOf(rectangle) == quadrilateral) == True,
    (typeOf(square) == triangle) == False,
    (typeOf(square) == quadrilateral) == True)

And(If(typeOf(regular_triangle) == triangle, True, False),
    If(typeOf(right_triangle) == triangle, True, False),
    If(typeOf(rectangle) == quadrilateral, True, False),
    If(typeOf(square) == quadrilateral, True, False))

Type == typeOf(Subtype)

True
