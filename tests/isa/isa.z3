
-- theory
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

And(typeOf(regular_triangle) == triangle,
    typeOf(right_triangle) == triangle,
    typeOf(rectangle) == quadrilateral,
    typeOf(square) == quadrilateral)

Type == typeOf(Subtype)

True

-- atoms
Type
Subtype
asi(triangle,regular_triangle)
asi(triangle,right_triangle)
asi(triangle,rectangle)
asi(triangle,square)
asi(quadrilateral,regular_triangle)
asi(quadrilateral,right_triangle)
asi(quadrilateral,rectangle)
asi(quadrilateral,square)
typeOf(regular_triangle)
typeOf(right_triangle)
typeOf(rectangle)
typeOf(square)
∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
∀t[type]st[subtype] : typeOf(st) = t ⇔ isa(st,t)
∀st[subtype] : isa(st,typeOf(st))
Type = typeOf(Subtype)

-- propagation
{'Subtype': {'Subtype': {'normal': True,
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square']}},
 'Type': {'Type': {'normal': True, 'typ': 'type', 'value': '', 'values': ['triangle', 'quadrilateral']},
          'Type = typeOf(Subtype)': {'cf': False, 'ct': False, 'normal': False, 'typ': 'Bool'}},
 'asi': {'asi(quadrilateral,rectangle)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
         'asi(quadrilateral,regular_triangle)': {'cf': True, 'ct': False, 'normal': True, 'typ': 'Bool'},
         'asi(quadrilateral,right_triangle)': {'cf': True, 'ct': False, 'normal': True, 'typ': 'Bool'},
         'asi(quadrilateral,square)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
         'asi(triangle,rectangle)': {'cf': True, 'ct': False, 'normal': True, 'typ': 'Bool'},
         'asi(triangle,regular_triangle)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
         'asi(triangle,right_triangle)': {'cf': False, 'ct': True, 'normal': True, 'typ': 'Bool'},
         'asi(triangle,square)': {'cf': True, 'ct': False, 'normal': True, 'typ': 'Bool'},
         '∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)': {'cf': False, 'ct': False, 'normal': False, 'typ': 'Bool'}},
 'typeOf': {'typeOf(rectangle)': {'normal': True,
                                  'typ': 'type',
                                  'value': 'quadrilateral',
                                  'values': ['triangle', 'quadrilateral']},
            'typeOf(regular_triangle)': {'normal': True,
                                         'typ': 'type',
                                         'value': 'triangle',
                                         'values': ['triangle', 'quadrilateral']},
            'typeOf(right_triangle)': {'normal': True,
                                       'typ': 'type',
                                       'value': 'triangle',
                                       'values': ['triangle', 'quadrilateral']},
            'typeOf(square)': {'normal': True,
                               'typ': 'type',
                               'value': 'quadrilateral',
                               'values': ['triangle', 'quadrilateral']},
            '∀st[subtype] : isa(st,typeOf(st))': {'cf': False, 'ct': False, 'normal': False, 'typ': 'Bool'},
            '∀t[type]st[subtype] : typeOf(st) = t ⇔ isa(st,t)': {'cf': False,
                                                                 'ct': False,
                                                                 'normal': False,
                                                                 'typ': 'Bool'}}}
