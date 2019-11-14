
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
