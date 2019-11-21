
--
And(asi(triangle, regular_triangle),
    Not(asi(quadrilateral, regular_triangle)),
    asi(triangle, right_triangle),
    Not(asi(quadrilateral, right_triangle)),
    Not(asi(triangle, rectangle)),
    asi(quadrilateral, rectangle),
    Not(asi(triangle, square)),
    asi(quadrilateral, square))

And(typeOf(regular_triangle) == triangle,
    Not(typeOf(regular_triangle) == quadrilateral),
    typeOf(right_triangle) == triangle,
    Not(typeOf(right_triangle) == quadrilateral),
    Not(typeOf(rectangle) == triangle),
    typeOf(rectangle) == quadrilateral,
    Not(typeOf(square) == triangle),
    typeOf(square) == quadrilateral)

And(If(typeOf(regular_triangle) == triangle, True, False),
    If(typeOf(right_triangle) == triangle, True, False),
    If(typeOf(rectangle) == quadrilateral, True, False),
    If(typeOf(square) == quadrilateral, True, False))

Type == typeOf(Subtype)

True
