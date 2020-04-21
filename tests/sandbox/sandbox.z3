
-- original ---------------------------------
vocabulary {
    
    type sides = {3..4}
    Sides: sides


    type type constructed from {triangle, quadrilateral}
    Type : type

    type side = {1..4}
    Length(side):real

    type subtype constructed from
        { regular_triangle
        , right_triangle
        , rectangle
        , square
        , irregular}
    Subtype : subtype

    Equilateral
}

theory {
    Sides=3. 

    Equilateral <=> (∀n[side]: Length(n)=Length(1) | Sides < n).

}
-- vocabulary -------------------------------

-- theory -----------------------------------
Sides == 3

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

Or(Sides == 3, Sides == 4)

Or(Type == triangle, Type == quadrilateral)

Or(Subtype == regular_triangle,
   Subtype == right_triangle,
   Subtype == rectangle,
   Subtype == square,
   Subtype == irregular)

-- subtences ------------------------------------
Sides = 3
Equilateral
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4
Type = triangle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
Subtype = rectangle
Subtype = square
Subtype = irregular

-- GUILines ------------------------------------
Sides
Type
Length(1)
Length(2)
Length(3)
Length(4)
Subtype
Equilateral
Sides = 3
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4
Type = triangle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
Subtype = rectangle
Subtype = square
Subtype = irregular

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Sides = 3
Consequences:
  ~Sides = 4
  Sides = 3
Simplified:  
  Equilateral ⇔ (((Length(1) = Length(1)) ∧ (Length(2) = Length(1)) ∧ (Length(3) = Length(1))))
Irrelevant:  
  ~Sides = 4
  ~Type = triangle
  ~Type = quadrilateral
  ~Subtype = regular_triangle
  ~Subtype = right_triangle
  ~Subtype = rectangle
  ~Subtype = square
  ~Subtype = irregular


-- meta -------------------------------------
{'symbols': [{'idpname': 'Sides', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Length', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Equilateral',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Equilateral': {'Equilateral': {'environmental': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Length': {'Length(1)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(1)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(2)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(2)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(3)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(4)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(4)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': '∀n[side] : (Length(n) = Length(1)) ∨ '
                                                                            '(Sides < n)',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'}},
 'Sides': {'Sides': {'environmental': False,
                     'normal': True,
                     'reading': 'Sides',
                     'relevant': True,
                     'status': 'CONSEQUENCE',
                     'typ': 'Int',
                     'value': '3',
                     'values': ['3', '4']},
           'Sides = 3': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
           'Sides = 4': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'relevant': False,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False}},
 'Subtype': {'Subtype': {'environmental': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = irregular': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
             'Subtype = regular_triangle': {'environmental': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'relevant': False,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
             'Subtype = right_triangle': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': False,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
             'Subtype = square': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': False,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': False,
                   'status': 'UNKNOWN',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
          'Type = triangle': {'environmental': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'relevant': False,
                              'status': 'UNKNOWN',
                              'typ': 'Bool'}}}
