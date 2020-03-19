
-- original ---------------------------------
vocabulary {
    
    type sides = {3..4}
    Sides: sides
    Vertices: sides


    type type constructed from {triangle, quadrilateral}
    Type : type

    type side = {1..4}
    Length(side):real
    Angle(side):real

    type subtype constructed from
        { regular_triangle
        , right_triangle
        , rectangle
        , square
        , irregular}
    Subtype : subtype

    Convex
    Equilateral
    Perimeter:real

    Large(side)
    Base : real
    Height: real
    Surface:real
}

theory {
    Sides=3. 

    Subtype=rectangle => Length(3)=Length(1).

    Equilateral <=> (∀n[side]: Length(n)=Length(1) | Sides < n).

    Subtype=rectangle <=> Sides=4.

}

view expanded
-- vocabulary -------------------------------
ForAll(c!403,
       Implies(Large(c!403),
               And(And(c!403 >= 1, c!403 <= 4))))
-- theory -----------------------------------
Sides == 3

Or(Not(Subtype == rectangle), Length(3) == Length(1))

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

(Subtype == rectangle) == (Sides == 4)

And(Sides >= 3, Sides <= 4)

And(Vertices >= 3, Vertices <= 4)

-- atoms ------------------------------------
Sides
Vertices
Type
Length(1)
Length(2)
Length(3)
Length(4)
Angle(1)
Angle(2)
Angle(3)
Angle(4)
Subtype
Convex
Equilateral
Perimeter
Large(1)
Large(2)
Large(3)
Large(4)
Base
Height
Surface
Sides = 3
Subtype = rectangle
Length(3) = Length(1)
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4

-- case -------------------------------------
Type:        
  ForAll(c!403,
       Implies(Large(c!403),
               And(And(c!403 >= 1, c!403 <= 4))))
Definitions: 
  
Universals:  
  Sides = 3
Consequences:
  ~Subtype = rectangle
  ~Sides = 4
  Sides = 3
Simplified:  
  Equilateral ⇔ (((Length(1) = Length(1)) ∧ (Length(2) = Length(1)) ∧ (Length(3) = Length(1))))
Irrelevant:  
  Length(3) = Length(1)


-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Angle': {'Angle(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(1)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''}},
 'Base': {'Base': {'environmental': False,
                   'normal': True,
                   'reading': 'Base',
                   'relevant': False,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''}},
 'Convex': {'Convex': {'environmental': False,
                       'normal': True,
                       'reading': 'Convex',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}},
 'Equilateral': {'Equilateral': {'environmental': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Height': {'Height': {'environmental': False,
                       'normal': True,
                       'reading': 'Height',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}},
 'Large': {'Large(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(1)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Large(4)',
                        'relevant': False,
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
 'Perimeter': {'Perimeter': {'environmental': False,
                             'normal': True,
                             'reading': 'Perimeter',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Real',
                             'value': ''}},
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
                         'relevant': True,
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
             'Subtype = rectangle': {'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False}},
 'Surface': {'Surface': {'environmental': False,
                         'normal': True,
                         'reading': 'Surface',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Real',
                         'value': ''}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': False,
                   'status': 'UNKNOWN',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']}},
 'Vertices': {'Vertices': {'environmental': False,
                           'normal': True,
                           'reading': 'Vertices',
                           'relevant': False,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': ['3', '4']}}}
