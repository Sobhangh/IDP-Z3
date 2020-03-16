ForAll(c!361,
       Implies(Large(c!361),
               And(And(c!361 >= 1, c!361 <= 4))))
-- theory
And(Or(Angle(1) == 90, Sides < 1),
    Or(Angle(2) == 90, Sides < 2),
    Or(Angle(3) == 90, Sides < 3),
    Or(Angle(4) == 90, Sides < 4))

(Type == triangle) == (Sides == 3)

(Type == quadrilateral) == (Sides == 4)

And((Vertices == 3) == (Sides == 3),
    (Vertices == 4) == (Sides == 4))

Or(Not(Sides == 3), Convex)

Convex ==
And(Angle(1) < 180,
    Angle(2) < 180,
    Angle(3) < 180,
    Angle(4) < 180)

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

Or(Not(Sides == 3),
   Or(Subtype == right_triangle,
      Subtype == regular_triangle,
      Subtype == irregular))

(Subtype == regular_triangle) ==
And(Sides == 3, Equilateral)

(Subtype == regular_triangle) ==
And(Sides == 3,
    And(Or(Angle(1) == 60, Sides < 1),
        Or(Angle(2) == 60, Sides < 2),
        Or(Angle(3) == 60, Sides < 3),
        Or(Angle(4) == 60, Sides < 4)))

(Subtype == right_triangle) ==
And(Sides == 3,
    Or(Angle(1) == 90,
       Angle(2) == 90,
       Angle(3) == 90,
       Angle(4) == 90))

Or(Subtype == square, Subtype == rectangle) ==
And(Sides == 4,
    And(Or(Angle(1) == 90, Sides < 1),
        Or(Angle(2) == 90, Sides < 2),
        Or(Angle(3) == 90, Sides < 3),
        Or(Angle(4) == 90, Sides < 4)))

Or(Not(Subtype == rectangle),
   And(Length(1) == Length(3),
       Length(2) == Length(4),
       Not(Length(1) == Length(2))))

(Subtype == square) == And(Sides == 4, Equilateral)

Or(Not(Type == triangle),
   And(Length(1) <= Length(2) + Length(3),
       Length(2) <= Length(3) + Length(1),
       Length(3) <= Length(1) + Length(2)))

Perimeter == Length(1) + Length(2) + Length(3) + Length(4)

Angle(1) + Angle(2) + Angle(3) + Angle(4) ==
ToReal(180*(-2 + Sides))

And(Length(1) >= 0,
    Length(2) >= 0,
    Length(3) >= 0,
    Length(4) >= 0)

And(Angle(1) >= 0,
    Angle(2) >= 0,
    Angle(3) >= 0,
    Angle(4) >= 0)

And(Not(Angle(1) == 180),
    Not(Angle(2) == 180),
    Not(Angle(3) == 180),
    Not(Angle(4) == 180))

And((Angle(1) == 0) == (Vertices < 1),
    (Angle(2) == 0) == (Vertices < 2),
    (Angle(3) == 0) == (Vertices < 3),
    (Angle(4) == 0) == (Vertices < 4))

And((Length(1) == 0) == (Sides < 1),
    (Length(2) == 0) == (Sides < 2),
    (Length(3) == 0) == (Sides < 3),
    (Length(4) == 0) == (Sides < 4))

And(Sides >= 3, Sides <= 4)

And(Vertices >= 3, Vertices <= 4)

-- atoms
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
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
Type = triangle
Sides = 3
Type = quadrilateral
Sides = 4
Vertices = 3
Vertices = 4
∀n[side] : Angle(n) < 180
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Subtype = right_triangle
Subtype = regular_triangle
Subtype = irregular
∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
∃n[side] : Angle(n) = 90
Subtype = square
Subtype = rectangle
Length(1) = Length(3)
Length(2) = Length(4)
Length(1) = Length(2)
Length(1) ≤ (Length(2) + Length(3))
Length(2) ≤ (Length(3) + Length(1))
Length(3) ≤ (Length(1) + Length(2))
Perimeter = (sum{n[side] : true : Length(n)})
(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
∀x[side] : 0 ≤ Length(x)
∀x[side] : 0 ≤ Angle(x)
∀x[side] : Angle(x) ≠ 180
∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
∀n[side] : (Length(n) = 0) ⇔ (Sides < n)

-- case
Type:        
  ForAll(c!361,
       Implies(Large(c!361),
               And(And(c!361 >= 1, c!361 <= 4))))
Definitions: 
  
Universals:  
  ∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
  Perimeter = (sum{n[side] : true : Length(n)})
  (sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
  ∀x[side] : 0 ≤ Length(x)
  ∀x[side] : 0 ≤ Angle(x)
  ∀x[side] : Angle(x) ≠ 180
  ∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
  ∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
Consequences:
  ~Type = triangle
  ~Sides = 3
  Type = quadrilateral
  Sides = 4
  ~Vertices = 3
  Vertices = 4
  Convex
  ∀n[side] : Angle(n) < 180
  ~Subtype = right_triangle
  ~Subtype = regular_triangle
  ~Subtype = irregular
  ~∀n[side] : (Angle(n) = 60) ∨ (Sides < n)
  ∃n[side] : Angle(n) = 90
  Length(1) = Length(3)
  Length(2) = Length(4)
  Length(1) ≤ (Length(2) + Length(3))
  Length(3) ≤ (Length(1) + Length(2))
  Sides = 4
  Vertices = 4
  Type = quadrilateral
  Angle(1) = 90
  Angle(2) = 90
  Angle(3) = 90
  Angle(4) = 90
Simplified:  
  (Equilateral ⇔ (((Length(1) = Length(1)) ∧ (Length(2) = Length(1)) ∧ (Length(3) = Length(1)) ∧ (Length(4) = Length(1)))))
  ((((Subtype = square) ∨ (Subtype = rectangle))))
  ((Subtype = rectangle) ⇒ (~(Length(1) = Length(2))))
  ((Subtype = square) ⇔ (Equilateral))
Irrelevant:  
  


-- propagation
{' Global': {'env_dec': False},
 'Angle': {'(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)': {'environmental': False,
                                                                      'normal': False,
                                                                      'reading': 'The sum of the angles is 180° for a '
                                                                                 'triangle, and 360° for a '
                                                                                 'quadrilateral',
                                                                      'relevant': True,
                                                                      'status': 'UNIVERSAL',
                                                                      'typ': 'Bool',
                                                                      'value': True},
           'Angle(1)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(1)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '90'},
           'Angle(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '90'},
           'Angle(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '90'},
           'Angle(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '90'},
           '∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)': {'environmental': False,
                                                          'normal': False,
                                                          'reading': 'A polygon with N vertices has N angles',
                                                          'relevant': True,
                                                          'status': 'UNIVERSAL',
                                                          'typ': 'Bool',
                                                          'value': True},
           '∀n[side] : (Angle(n) = 60) ∨ (Sides < n)': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 60°',
                                                        'relevant': True,
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': False},
           '∀n[side] : (Angle(n) = 90) ∨ (Sides < n)': {'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 90°',
                                                        'relevant': True,
                                                        'status': 'UNIVERSAL',
                                                        'typ': 'Bool',
                                                        'value': True},
           '∀n[side] : Angle(n) < 180': {'environmental': False,
                                         'normal': False,
                                         'reading': 'All angles are below 180°',
                                         'relevant': True,
                                         'status': 'CONSEQUENCE',
                                         'typ': 'Bool',
                                         'value': True},
           '∀x[side] : 0 ≤ Angle(x)': {'environmental': False,
                                       'normal': False,
                                       'reading': 'Angles are positive numbers',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
           '∀x[side] : Angle(x) ≠ 180': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Angles cannot be 180°',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
           '∃n[side] : Angle(n) = 90': {'environmental': False,
                                        'normal': False,
                                        'reading': 'One angle is 90°',
                                        'relevant': True,
                                        'status': 'CONSEQUENCE',
                                        'typ': 'Bool',
                                        'value': True}},
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
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Bool',
                       'value': True}},
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
            'Length(1) = Length(2)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(2)',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
            'Length(1) = Length(3)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(3)',
                                      'relevant': True,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': True},
            'Length(1) ≤ (Length(2) + Length(3))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(1) ≤ (Length(2) + Length(3))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(2)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(2)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(2) = Length(4)': {'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(2) = Length(4)',
                                      'relevant': True,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': True},
            'Length(2) ≤ (Length(3) + Length(1))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(2) ≤ (Length(3) + Length(1))',
                                                    'relevant': True,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
            'Length(3)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(3)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3) ≤ (Length(1) + Length(2))': {'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(3) ≤ (Length(1) + Length(2))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(4)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(4)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            '∀n[side] : (Length(n) = 0) ⇔ (Sides < n)': {'environmental': False,
                                                         'normal': False,
                                                         'reading': 'A polygon with N sides has N lengths',
                                                         'relevant': True,
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': 'All sides have the same length',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'},
            '∀x[side] : 0 ≤ Length(x)': {'environmental': False,
                                         'normal': False,
                                         'reading': 'Lengths are positive numbers',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True}},
 'Perimeter': {'Perimeter': {'environmental': False,
                             'normal': True,
                             'reading': 'Perimeter',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Real',
                             'value': ''},
               'Perimeter = (sum{n[side] : true : Length(n)})': {'environmental': False,
                                                                 'normal': False,
                                                                 'reading': 'The perimeter is the sum of the lengths '
                                                                            'of the sides',
                                                                 'relevant': True,
                                                                 'status': 'UNIVERSAL',
                                                                 'typ': 'Bool',
                                                                 'value': True}},
 'Sides': {'Sides': {'environmental': False,
                     'normal': True,
                     'reading': 'Sides',
                     'relevant': True,
                     'status': 'CONSEQUENCE',
                     'typ': 'Int',
                     'value': '4',
                     'values': ['3', '4']},
           'Sides = 3': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False},
           'Sides = 4': {'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': True}},
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
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False},
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
                                            'status': 'CONSEQUENCE',
                                            'typ': 'Bool',
                                            'value': False},
             'Subtype = right_triangle': {'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': True,
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': False},
             'Subtype = square': {'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': True,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}},
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
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'type',
                   'value': 'quadrilateral',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': True},
          'Type = triangle': {'environmental': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': False}},
 'Vertices': {'Vertices': {'environmental': False,
                           'normal': True,
                           'reading': 'Vertices',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Int',
                           'value': '4',
                           'values': ['3', '4']},
              'Vertices = 3': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 3',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False},
              'Vertices = 4': {'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 4',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True}}}
