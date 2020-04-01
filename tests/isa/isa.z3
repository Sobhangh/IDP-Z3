
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
    Not(asi(quadrilateral, regular_triangle)),
    asi(1tri angle, right_triangle),
    Not(asi(quadrilateral, right_triangle)),
    Not(asi(1tri angle, rectangle)),
    asi(quadrilateral, rectangle),
    Not(asi(1tri angle, square)),
    asi(quadrilateral, square))

And(typeOf(regular_triangle) == 1tri angle,
    Not(typeOf(regular_triangle) == quadrilateral),
    typeOf(right_triangle) == 1tri angle,
    Not(typeOf(right_triangle) == quadrilateral),
    Not(typeOf(rectangle) == 1tri angle),
    typeOf(rectangle) == quadrilateral,
    Not(typeOf(square) == 1tri angle),
    typeOf(square) == quadrilateral)

And(typeOf(regular_triangle) == 1tri angle,
    typeOf(right_triangle) == 1tri angle,
    typeOf(rectangle) == quadrilateral,
    typeOf(square) == quadrilateral)

Type == typeOf(Subtype)

True

-- subtences ------------------------------------
∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)
∀st[subtype] : isa(st,typeOf(st))
Type = typeOf(Subtype)

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
∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)
∀st[subtype] : isa(st,typeOf(st))
Type = typeOf(Subtype)

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ∀t[type]st[subtype] : isa(st,t) ⇔ asi(t,st)
  ∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)
  ∀st[subtype] : isa(st,typeOf(st))
  Type = typeOf(Subtype)
Consequences:
  asi(1tri angle,regular_triangle)
  asi(1tri angle,right_triangle)
  ~asi(1tri angle,rectangle)
  ~asi(1tri angle,square)
  ~asi(quadrilateral,regular_triangle)
  ~asi(quadrilateral,right_triangle)
  asi(quadrilateral,rectangle)
  asi(quadrilateral,square)
  typeOf(regular_triangle) = 1tri angle
  typeOf(right_triangle) = 1tri angle
  typeOf(rectangle) = quadrilateral
  typeOf(square) = quadrilateral
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'Type', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'Subtype', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'asi', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'typeOf', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}]}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Subtype': {'Subtype': {'environmental': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square']}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'type',
                   'value': '',
                   'values': ['1tri angle', 'quadrilateral']},
          'Type = typeOf(Subtype)': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Type = typeOf(Subtype)',
                                     'relevant': True,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True}},
 'asi': {'asi(1tri angle,rectangle)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'asi(1tri angle,rectangle)',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'Bool',
                                       'value': False},
         'asi(1tri angle,regular_triangle)': {'environmental': False,
                                              'normal': True,
                                              'reading': 'asi(1tri angle,regular_triangle)',
                                              'relevant': True,
                                              'status': 'CONSEQUENCE',
                                              'typ': 'Bool',
                                              'value': True},
         'asi(1tri angle,right_triangle)': {'environmental': False,
                                            'normal': True,
                                            'reading': 'asi(1tri angle,right_triangle)',
                                            'relevant': True,
                                            'status': 'CONSEQUENCE',
                                            'typ': 'Bool',
                                            'value': True},
         'asi(1tri angle,square)': {'environmental': False,
                                    'normal': True,
                                    'reading': 'asi(1tri angle,square)',
                                    'relevant': True,
                                    'status': 'CONSEQUENCE',
                                    'typ': 'Bool',
                                    'value': False},
         'asi(quadrilateral,rectangle)': {'environmental': False,
                                          'normal': True,
                                          'reading': 'asi(quadrilateral,rectangle)',
                                          'relevant': True,
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': True},
         'asi(quadrilateral,regular_triangle)': {'environmental': False,
                                                 'normal': True,
                                                 'reading': 'asi(quadrilateral,regular_triangle)',
                                                 'relevant': True,
                                                 'status': 'CONSEQUENCE',
                                                 'typ': 'Bool',
                                                 'value': False},
         'asi(quadrilateral,right_triangle)': {'environmental': False,
                                               'normal': True,
                                               'reading': 'asi(quadrilateral,right_triangle)',
                                               'relevant': True,
                                               'status': 'CONSEQUENCE',
                                               'typ': 'Bool',
                                               'value': False},
         'asi(quadrilateral,square)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'asi(quadrilateral,square)',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
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
                                  'reading': 'typeOf(rectangle)',
                                  'relevant': True,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'type',
                                  'value': 'quadrilateral',
                                  'values': ['1tri angle', 'quadrilateral']},
            'typeOf(regular_triangle)': {'environmental': False,
                                         'normal': True,
                                         'reading': 'typeOf(regular_triangle)',
                                         'relevant': True,
                                         'status': 'CONSEQUENCE',
                                         'typ': 'type',
                                         'value': '1tri angle',
                                         'values': ['1tri angle', 'quadrilateral']},
            'typeOf(right_triangle)': {'environmental': False,
                                       'normal': True,
                                       'reading': 'typeOf(right_triangle)',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'type',
                                       'value': '1tri angle',
                                       'values': ['1tri angle', 'quadrilateral']},
            'typeOf(square)': {'environmental': False,
                               'normal': True,
                               'reading': 'typeOf(square)',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'type',
                               'value': 'quadrilateral',
                               'values': ['1tri angle', 'quadrilateral']},
            '∀st[subtype] : isa(st,typeOf(st))': {'environmental': False,
                                                  'normal': False,
                                                  'reading': '∀st[subtype] : isa(st,typeOf(st))',
                                                  'relevant': True,
                                                  'status': 'UNIVERSAL',
                                                  'typ': 'Bool',
                                                  'value': True},
            '∀t[type]st[subtype] : (typeOf(st) = t) ⇔ isa(st,t)': {'environmental': False,
                                                                   'normal': False,
                                                                   'reading': '∀t[type]st[subtype] : (typeOf(st) = t) '
                                                                              '⇔ isa(st,t)',
                                                                   'relevant': True,
                                                                   'status': 'UNIVERSAL',
                                                                   'typ': 'Bool',
                                                                   'value': True}}}
