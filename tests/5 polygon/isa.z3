
-- original ---------------------------------
vocabulary {
    type type constructed from {'1tri angle', 'quadrilateral'}
    Type : type


    type subtype constructed from
        { regular_triangle
        , right_triangle
        , rectangle
        , square}
    Subtype : subtype

    isa(subtype, type)

    [ASI]
        [short:this is a short info]
        [long:long, this is a long info]
    asi(type, subtype)
    typeOf(subtype): type
}

theory {
    !t[type] st[subtype]: isa(st,t) <=> asi(t, st).
    !t[type] st[subtype]: typeOf(st) = t <=> isa(st, t).
    !st[subtype]: isa(st, typeOf(st)).
    Type = typeOf(Subtype).
    isa(regular_triangle, '1tri angle').
}

structure {
    isa = {regular_triangle, '1tri angle'; right_triangle, '1tri angle';
           rectangle, quadrilateral; square, quadrilateral}
}
-- vocabulary -------------------------------

-- theory -----------------------------------
And(asi(1tri angle, regular_triangle),
    asi(1tri angle, right_triangle),
    Not(asi(1tri angle, rectangle)),
    Not(asi(1tri angle, square)),
    Not(asi(quadrilateral, regular_triangle)),
    Not(asi(quadrilateral, right_triangle)),
    asi(quadrilateral, rectangle),
    asi(quadrilateral, square))

And(typeOf(regular_triangle) == 1tri angle,
    typeOf(right_triangle) == 1tri angle,
    Not(typeOf(rectangle) == 1tri angle),
    Not(typeOf(square) == 1tri angle),
    Not(typeOf(regular_triangle) == quadrilateral),
    Not(typeOf(right_triangle) == quadrilateral),
    typeOf(rectangle) == quadrilateral,
    typeOf(square) == quadrilateral)

And(typeOf(regular_triangle) == 1tri angle,
    typeOf(right_triangle) == 1tri angle,
    typeOf(rectangle) == quadrilateral,
    typeOf(square) == quadrilateral)

Type == typeOf(Subtype)

True

Or(Type == 1tri angle, Type == quadrilateral)

Or(Subtype == regular_triangle,
   Subtype == right_triangle,
   Subtype == rectangle,
   Subtype == square)

Or(typeOf(regular_triangle) == 1tri angle,
   typeOf(regular_triangle) == quadrilateral)

Or(typeOf(right_triangle) == 1tri angle,
   typeOf(right_triangle) == quadrilateral)

Or(typeOf(rectangle) == 1tri angle,
   typeOf(rectangle) == quadrilateral)

Or(typeOf(square) == 1tri angle,
   typeOf(square) == quadrilateral)

-- subtences ------------------------------------
∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
∀t[type]st[subtype] : typeOf(st) = t ⇔ isa(st,t)
∀st[subtype] : isa(st,typeOf(st))
Type = typeOf(Subtype)
Type = 1tri angle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
Subtype = rectangle
Subtype = square
typeOf(regular_triangle) = 1tri angle
typeOf(regular_triangle) = quadrilateral
typeOf(right_triangle) = 1tri angle
typeOf(right_triangle) = quadrilateral
typeOf(rectangle) = 1tri angle
typeOf(rectangle) = quadrilateral
typeOf(square) = 1tri angle
typeOf(square) = quadrilateral

-- GUILines ------------------------------------
Type
Subtype
asi(1tri angle,regular_triangle)
asi(1tri angle,right_triangle)
asi(1tri angle,rectangle)
asi(1tri angle,square)
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
Type = 1tri angle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
Subtype = rectangle
Subtype = square
typeOf(regular_triangle) = 1tri angle
typeOf(regular_triangle) = quadrilateral
typeOf(right_triangle) = 1tri angle
typeOf(right_triangle) = quadrilateral
typeOf(rectangle) = 1tri angle
typeOf(rectangle) = quadrilateral
typeOf(square) = 1tri angle
typeOf(square) = quadrilateral

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
  ∀t[type]st[subtype] : typeOf(st) = t ⇔ isa(st,t)
  ∀st[subtype] : isa(st,typeOf(st))
  Type = typeOf(Subtype)
  asi(1tri angle,regular_triangle)
  asi(1tri angle,right_triangle)
  ~asi(1tri angle,rectangle)
  ~asi(1tri angle,square)
  ~asi(quadrilateral,regular_triangle)
  ~asi(quadrilateral,right_triangle)
  asi(quadrilateral,rectangle)
  asi(quadrilateral,square)
  typeOf(regular_triangle) -> 1tri angle
  typeOf(right_triangle) -> 1tri angle
  typeOf(rectangle) -> quadrilateral
  typeOf(square) -> quadrilateral
  isa(regular_triangle,typeOf(regular_triangle))
  isa(right_triangle,typeOf(right_triangle))
  isa(rectangle,typeOf(rectangle))
  isa(square,typeOf(square))
Consequences:
  typeOf(regular_triangle) = 1tri angle
  ~typeOf(regular_triangle) = quadrilateral
  typeOf(right_triangle) = 1tri angle
  ~typeOf(right_triangle) = quadrilateral
  ~typeOf(rectangle) = 1tri angle
  typeOf(rectangle) = quadrilateral
  ~typeOf(square) = 1tri angle
  typeOf(square) = quadrilateral
Simplified:  
  true
  true
  true
  true
  true
  Type = 1tri angle ∨ Type = quadrilateral
  Subtype = regular_triangle ∨ Subtype = right_triangle ∨ Subtype = rectangle ∨ Subtype = square
  true
  true
  true
  true
Irrelevant:  
  ~typeOf(regular_triangle) = quadrilateral
  ~typeOf(right_triangle) = quadrilateral
  isa(regular_triangle,typeOf(regular_triangle))
  isa(right_triangle,typeOf(right_triangle))
  isa(rectangle,typeOf(rectangle))
  isa(square,typeOf(square))


-- meta -------------------------------------
{'symbols': [{'idpname': 'Type', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Subtype', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'guiname': 'ASI',
              'idpname': 'asi',
              'longinfo': 'long, this is a long info',
              'priority': 'core',
              'shortinfo': 'this is a short info',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'idpname': 'typeOf', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Subtype': {'Subtype': {'environmental': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square']},
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
             'Subtype = regular_triangle': {'environmental': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'relevant': True,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
             'Subtype = right_triangle': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
             'Subtype = square': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'type',
                   'value': '',
                   'values': ['1tri angle', 'quadrilateral']},
          'Type = 1tri angle': {'environmental': False,
                                'normal': False,
                                'reading': 'Type = 1tri angle',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
          'Type = quadrilateral': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
          'Type = typeOf(Subtype)': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Type = typeOf(Subtype)',
                                     'relevant': True,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True}},
 'asi': {'asi(1tri angle,rectangle)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'asi(t,st)',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': False},
         'asi(1tri angle,regular_triangle)': {'environmental': False,
                                              'normal': True,
                                              'reading': 'asi(t,st)',
                                              'relevant': True,
                                              'status': 'UNIVERSAL',
                                              'typ': 'Bool',
                                              'value': True},
         'asi(1tri angle,right_triangle)': {'environmental': False,
                                            'normal': True,
                                            'reading': 'asi(t,st)',
                                            'relevant': True,
                                            'status': 'UNIVERSAL',
                                            'typ': 'Bool',
                                            'value': True},
         'asi(1tri angle,square)': {'environmental': False,
                                    'normal': True,
                                    'reading': 'asi(t,st)',
                                    'relevant': True,
                                    'status': 'UNIVERSAL',
                                    'typ': 'Bool',
                                    'value': False},
         'asi(quadrilateral,rectangle)': {'environmental': False,
                                          'normal': True,
                                          'reading': 'asi(t,st)',
                                          'relevant': True,
                                          'status': 'UNIVERSAL',
                                          'typ': 'Bool',
                                          'value': True},
         'asi(quadrilateral,regular_triangle)': {'environmental': False,
                                                 'normal': True,
                                                 'reading': 'asi(t,st)',
                                                 'relevant': True,
                                                 'status': 'UNIVERSAL',
                                                 'typ': 'Bool',
                                                 'value': False},
         'asi(quadrilateral,right_triangle)': {'environmental': False,
                                               'normal': True,
                                               'reading': 'asi(t,st)',
                                               'relevant': True,
                                               'status': 'UNIVERSAL',
                                               'typ': 'Bool',
                                               'value': False},
         'asi(quadrilateral,square)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'asi(t,st)',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
         '∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)': {'environmental': False,
                                                         'normal': False,
                                                         'reading': '∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)',
                                                         'relevant': True,
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True}},
 'typeOf': {'typeOf(rectangle)': {'environmental': False,
                                  'normal': True,
                                  'reading': 'typeOf(st)',
                                  'relevant': True,
                                  'status': 'UNIVERSAL',
                                  'typ': 'type',
                                  'value': 'quadrilateral',
                                  'values': ['1tri angle', 'quadrilateral']},
            'typeOf(rectangle) = 1tri angle': {'environmental': False,
                                               'normal': False,
                                               'reading': 'typeOf(rectangle) = 1tri angle',
                                               'relevant': True,
                                               'status': 'CONSEQUENCE',
                                               'typ': 'Bool',
                                               'value': False},
            'typeOf(rectangle) = quadrilateral': {'environmental': False,
                                                  'normal': False,
                                                  'reading': 'typeOf(rectangle) = quadrilateral',
                                                  'relevant': True,
                                                  'status': 'CONSEQUENCE',
                                                  'typ': 'Bool',
                                                  'value': True},
            'typeOf(regular_triangle)': {'environmental': False,
                                         'normal': True,
                                         'reading': 'typeOf(st)',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'type',
                                         'value': '1tri angle',
                                         'values': ['1tri angle', 'quadrilateral']},
            'typeOf(regular_triangle) = 1tri angle': {'environmental': False,
                                                      'normal': False,
                                                      'reading': 'typeOf(regular_triangle) = 1tri angle',
                                                      'relevant': True,
                                                      'status': 'CONSEQUENCE',
                                                      'typ': 'Bool',
                                                      'value': True},
            'typeOf(regular_triangle) = quadrilateral': {'environmental': False,
                                                         'normal': False,
                                                         'reading': 'typeOf(regular_triangle) = quadrilateral',
                                                         'relevant': False,
                                                         'status': 'CONSEQUENCE',
                                                         'typ': 'Bool',
                                                         'value': False},
            'typeOf(right_triangle)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'typeOf(st)',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'type',
                                       'value': '1tri angle',
                                       'values': ['1tri angle', 'quadrilateral']},
            'typeOf(right_triangle) = 1tri angle': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'typeOf(right_triangle) = 1tri angle',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'typeOf(right_triangle) = quadrilateral': {'environmental': False,
                                                       'normal': False,
                                                       'reading': 'typeOf(right_triangle) = quadrilateral',
                                                       'relevant': False,
                                                       'status': 'CONSEQUENCE',
                                                       'typ': 'Bool',
                                                       'value': False},
            'typeOf(square)': {'environmental': False,
                               'normal': True,
                               'reading': 'typeOf(st)',
                               'relevant': True,
                               'status': 'UNIVERSAL',
                               'typ': 'type',
                               'value': 'quadrilateral',
                               'values': ['1tri angle', 'quadrilateral']},
            'typeOf(square) = 1tri angle': {'environmental': False,
                                            'normal': False,
                                            'reading': 'typeOf(square) = 1tri angle',
                                            'relevant': True,
                                            'status': 'CONSEQUENCE',
                                            'typ': 'Bool',
                                            'value': False},
            'typeOf(square) = quadrilateral': {'environmental': False,
                                               'normal': False,
                                               'reading': 'typeOf(square) = quadrilateral',
                                               'relevant': True,
                                               'status': 'CONSEQUENCE',
                                               'typ': 'Bool',
                                               'value': True},
            '∀st[subtype] : isa(st,typeOf(st))': {'environmental': False,
                                                  'normal': False,
                                                  'reading': '∀st[subtype] : isa(st,typeOf(st))',
                                                  'relevant': True,
                                                  'status': 'UNIVERSAL',
                                                  'typ': 'Bool',
                                                  'value': True},
            '∀t[type]st[subtype] : typeOf(st) = t ⇔ isa(st,t)': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': '∀t[type]st[subtype] : typeOf(st) = t ⇔ '
                                                                            'isa(st,t)',
                                                                 'relevant': True,
                                                                 'status': 'UNIVERSAL',
                                                                 'typ': 'Bool',
                                                                 'value': True}}}
