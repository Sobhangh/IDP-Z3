
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
∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)
∀st[subtype] : isa(st,typeOf(st))
Type = typeOf(Subtype)

-- case
Type:        
  
Definitions: 
  
Universals:  
  ∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
  ∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)
  ∀st[subtype] : isa(st,typeOf(st))
  Type = typeOf(Subtype)
Consequences:
  
Simplified:  
  
Irrelevant:  
  


-- propagation
{'Subtype': {'Subtype': {'normal': True,
                         'reading': 'Subtype',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square']}},
 'Type': {'Type': {'normal': True,
                   'reading': 'Type',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']},
          'Type = typeOf(Subtype)': {'cf': False,
                                     'ct': True,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Type = typeOf(Subtype)',
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True}},
 'asi': {'asi(quadrilateral,rectangle)': {'cf': False,
                                          'ct': True,
                                          'irrelevant': False,
                                          'normal': True,
                                          'reading': 'asi(quadrilateral,rectangle)',
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool',
                                          'value': True},
         'asi(quadrilateral,regular_triangle)': {'cf': True,
                                                 'ct': False,
                                                 'irrelevant': False,
                                                 'normal': True,
                                                 'reading': 'asi(quadrilateral,regular_triangle)',
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Bool',
                                                 'value': False},
         'asi(quadrilateral,right_triangle)': {'cf': True,
                                               'ct': False,
                                               'irrelevant': False,
                                               'normal': True,
                                               'reading': 'asi(quadrilateral,right_triangle)',
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool',
                                               'value': False},
         'asi(quadrilateral,square)': {'cf': False,
                                       'ct': True,
                                       'irrelevant': False,
                                       'normal': True,
                                       'reading': 'asi(quadrilateral,square)',
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool',
                                       'value': True},
         'asi(triangle,rectangle)': {'cf': True,
                                     'ct': False,
                                     'irrelevant': False,
                                     'normal': True,
                                     'reading': 'asi(triangle,rectangle)',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool',
                                     'value': False},
         'asi(triangle,regular_triangle)': {'cf': False,
                                            'ct': True,
                                            'irrelevant': False,
                                            'normal': True,
                                            'reading': 'asi(triangle,regular_triangle)',
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool',
                                            'value': True},
         'asi(triangle,right_triangle)': {'cf': False,
                                          'ct': True,
                                          'irrelevant': False,
                                          'normal': True,
                                          'reading': 'asi(triangle,right_triangle)',
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool',
                                          'value': True},
         'asi(triangle,square)': {'cf': True,
                                  'ct': False,
                                  'irrelevant': False,
                                  'normal': True,
                                  'reading': 'asi(triangle,square)',
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool',
                                  'value': False},
         '∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)': {'cf': False,
                                                         'ct': True,
                                                         'irrelevant': False,
                                                         'normal': False,
                                                         'reading': '∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)',
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True}},
 'typeOf': {'typeOf(rectangle)': {'normal': True,
                                  'reading': 'typeOf(rectangle)',
                                  'typ': 'type',
                                  'value': 'quadrilateral',
                                  'values': ['triangle', 'quadrilateral']},
            'typeOf(regular_triangle)': {'normal': True,
                                         'reading': 'typeOf(regular_triangle)',
                                         'typ': 'type',
                                         'value': 'triangle',
                                         'values': ['triangle', 'quadrilateral']},
            'typeOf(right_triangle)': {'normal': True,
                                       'reading': 'typeOf(right_triangle)',
                                       'typ': 'type',
                                       'value': 'triangle',
                                       'values': ['triangle', 'quadrilateral']},
            'typeOf(square)': {'normal': True,
                               'reading': 'typeOf(square)',
                               'typ': 'type',
                               'value': 'quadrilateral',
                               'values': ['triangle', 'quadrilateral']},
            '∀st[subtype] : isa(st,typeOf(st))': {'cf': False,
                                                  'ct': True,
                                                  'irrelevant': False,
                                                  'normal': False,
                                                  'reading': '∀st[subtype] : isa(st,typeOf(st))',
                                                  'status': 'UNIVERSAL',
                                                  'typ': 'Bool',
                                                  'value': True},
            '∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)': {'cf': False,
                                                                   'ct': True,
                                                                   'irrelevant': False,
                                                                   'normal': False,
                                                                   'reading': '∀t[type]st[subtype] : (typeOf(st) = t) '
                                                                              '⇔ isa(st,t)',
                                                                   'status': 'UNIVERSAL',
                                                                   'typ': 'Bool',
                                                                   'value': True}}}
