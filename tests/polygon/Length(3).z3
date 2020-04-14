
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

    Subtype=rectangle => Length(3)=Length(1).

    Equilateral <=> (∀n[side]: Length(n)=Length(1) | Sides < n).

    Subtype=rectangle <=> Sides=4.

}

view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Sides == 3

Or(Not(Subtype == rectangle), Length(3) == Length(1))

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

(Subtype == rectangle) == (Sides == 4)

Or(Sides == 3, Sides == 4)

Or(Type == triangle, Type == quadrilateral)

Or(Subtype == regular_triangle,
   Subtype == right_triangle,
   Subtype == rectangle,
   Subtype == square,
   Subtype == irregular)

-- subtences ------------------------------------
Sides = 3
Subtype = rectangle
Length(3) = Length(1)
Equilateral
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4
Type = triangle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
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
Subtype = rectangle
Length(3) = Length(1)
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4
Type = triangle
Type = quadrilateral
Subtype = regular_triangle
Subtype = right_triangle
Subtype = square
Subtype = irregular

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Sides = 3
Consequences:
  ~Subtype = rectangle <= {'(Subtype = rectangle) ⇔ (Sides = 4)', 'Sides', 'Sides = 4'}
  ~Sides = 4 <= {'Sides'}
  Sides = 3
Simplified:  
  Equilateral ⇔ ((((Length(1) = Length(1))) ∧ ((Length(2) = Length(1))) ∧ ((Length(3) = Length(1)))))
  (Subtype = regular_triangle) ∨ (Subtype = right_triangle) ∨ (Subtype = square) ∨ (Subtype = irregular)
Irrelevant:  
  ~Length(3) = Length(1)
  ~Sides = 4 <= {'Sides'}
  ~Type = triangle
  ~Type = quadrilateral


-- meta -------------------------------------
{'symbols': [{'idpname': 'Sides', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Length', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Subtype', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'Equilateral',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
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
            'Length(3) = Length(1)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(3) = Length(1)',
                                      'relevant': False,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
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
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = irregular': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False},
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
