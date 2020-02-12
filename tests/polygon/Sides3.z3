ForAll(c!2,
       Implies(Large(c!2), And(And(c!2 >= 1, c!2 <= 4))))
-- theory
Sides == 3

(Type == triangle) == (Sides == 3)

(Type == quadrilateral) == (Sides == 4)

(Vertices == 3) == (Sides == 3)

(Vertices == 4) == (Sides == 4)

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

Or(Not(Type == triangle), Surface == 1/2*Base*Height)

Or(Not(Or(Subtype == square, Subtype == rectangle)),
   Surface == Length(1)*Length(2))

Or(Not(And(Subtype == irregular, Sides == 4)),
   Surface == -1)

Base >= 0

Height >= 0

Or(And(Sides >= 1, Length(1) == Base),
   And(Sides >= 2, Length(2) == Base),
   And(Sides >= 3, Length(3) == Base),
   And(Sides >= 4, Length(4) == Base))

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
Sides = 3
Type = triangle
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
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
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
Surface = ((Base * Height) / 2)
Surface = (Length(1) * Length(2))
Surface = (-(1))
0 ≤ Base
0 ≤ Height
∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)

-- case
Type:        
  ForAll(c!2,
       Implies(Large(c!2), And(And(c!2 >= 1, c!2 <= 4))))
Definitions: 
  
Universals:  
  Sides = 3
  Perimeter = (sum{n[side] : true : Length(n)})
  (sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
  ∀x[side] : 0 ≤ Length(x)
  ∀x[side] : 0 ≤ Angle(x)
  ∀x[side] : Angle(x) ≠ 180
  ∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
  ∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
  0 ≤ Base
  0 ≤ Height
  ∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)
Consequences:
  Type = triangle
  ~Type = quadrilateral
  ~Sides = 4
  Vertices = 3
  ~Vertices = 4
  Convex
  ∀n[side] : Angle(n) < 180
  ~Subtype = square
  ~Subtype = rectangle
  ~∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
  ~Length(2) = Length(4)
  Length(1) ≤ (Length(2) + Length(3))
  Length(2) ≤ (Length(3) + Length(1))
  Length(3) ≤ (Length(1) + Length(2))
  Surface = ((Base * Height) / 2)
  ~Surface = (-(1))
  Sides = 3
  Vertices = 3
  Type = triangle
  Length(4) = 0
  Angle(4) = 0
Simplified:  
  (Equilateral ⇔ (((Length(1) = Length(1)) ∧ (Length(2) = Length(1)) ∧ (Length(3) = Length(1)))))
  (((Subtype = right_triangle) ∨ (Subtype = regular_triangle) ∨ (Subtype = irregular)))
  ((Subtype = regular_triangle) ⇔ (Equilateral))
  ((Subtype = regular_triangle) ⇔ ((((Angle(1) = 60) ∧ (Angle(2) = 60) ∧ (Angle(3) = 60)))))
  ((Subtype = right_triangle) ⇔ ((((Angle(1) = 90) ∨ (Angle(2) = 90) ∨ (Angle(3) = 90) ∨ (Angle(4) = 90)))))
Irrelevant:  
  ((Angle(1) = 90) ∧ (Angle(2) = 90) ∧ (Angle(3) = 90))
  Length(1) = Length(3)
  Length(2) = (0)
  Length(1) = Length(2)
  Surface = (Length(1) * Length(2))
  Surface = (-(1))


-- propagation
{' Global': {'env_dec': False, 'env_done': True},
 'Angle': {'(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)': {'cf': False,
                                                                      'ct': True,
                                                                      'environmental': False,
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
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(2)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(3)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Real',
                        'value': ''},
           'Angle(4)': {'environmental': False,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'relevant': True,
                        'status': 'CONSEQUENCE',
                        'typ': 'Real',
                        'value': '0'},
           '∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)': {'cf': False,
                                                          'ct': True,
                                                          'environmental': False,
                                                          'normal': False,
                                                          'reading': 'A polygon with N vertices has N angles',
                                                          'relevant': True,
                                                          'status': 'UNIVERSAL',
                                                          'typ': 'Bool',
                                                          'value': True},
           '∀n[side] : (Angle(n) = 60) ∨ (Sides < n)': {'cf': False,
                                                        'ct': False,
                                                        'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 60°',
                                                        'relevant': True,
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'},
           '∀n[side] : (Angle(n) = 90) ∨ (Sides < n)': {'cf': True,
                                                        'ct': False,
                                                        'environmental': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 90°',
                                                        'relevant': False,
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': False},
           '∀n[side] : Angle(n) < 180': {'cf': False,
                                         'ct': True,
                                         'environmental': False,
                                         'normal': False,
                                         'reading': 'All angles are below 180°',
                                         'relevant': True,
                                         'status': 'CONSEQUENCE',
                                         'typ': 'Bool',
                                         'value': True},
           '∀x[side] : 0 ≤ Angle(x)': {'cf': False,
                                       'ct': True,
                                       'environmental': False,
                                       'normal': False,
                                       'reading': 'Angles are positive numbers',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
           '∀x[side] : Angle(x) ≠ 180': {'cf': False,
                                         'ct': True,
                                         'environmental': False,
                                         'normal': False,
                                         'reading': 'Angles cannot be 180°',
                                         'relevant': True,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
           '∃n[side] : Angle(n) = 90': {'cf': False,
                                        'ct': False,
                                        'environmental': False,
                                        'normal': False,
                                        'reading': 'One angle is 90°',
                                        'relevant': True,
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Base': {'0 ≤ Base': {'cf': False,
                       'ct': True,
                       'environmental': False,
                       'normal': False,
                       'reading': '0 ≤ Base',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          'Base': {'environmental': False,
                   'normal': True,
                   'reading': 'Base',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''}},
 'Convex': {'Convex': {'cf': False,
                       'ct': True,
                       'environmental': False,
                       'normal': True,
                       'reading': 'Convex',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'Bool',
                       'value': True}},
 'Equilateral': {'Equilateral': {'cf': False,
                                 'ct': False,
                                 'environmental': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Height': {'0 ≤ Height': {'cf': False,
                           'ct': True,
                           'environmental': False,
                           'normal': False,
                           'reading': '0 ≤ Height',
                           'relevant': True,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': True},
            'Height': {'environmental': False,
                       'normal': True,
                       'reading': 'Height',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}},
 'Large': {'Large(1)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Large(1)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(2)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(3)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'relevant': False,
                        'status': 'UNKNOWN',
                        'typ': 'Bool'},
           'Large(4)': {'cf': False,
                        'ct': False,
                        'environmental': False,
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
            'Length(1) = Length(2)': {'cf': False,
                                      'ct': False,
                                      'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(2)',
                                      'relevant': False,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
            'Length(1) = Length(3)': {'cf': False,
                                      'ct': False,
                                      'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(1) = Length(3)',
                                      'relevant': False,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
            'Length(1) ≤ (Length(2) + Length(3))': {'cf': False,
                                                    'ct': True,
                                                    'environmental': False,
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
            'Length(2) = Length(4)': {'cf': True,
                                      'ct': False,
                                      'environmental': False,
                                      'normal': False,
                                      'reading': 'Length(2) = Length(4)',
                                      'relevant': False,
                                      'status': 'CONSEQUENCE',
                                      'typ': 'Bool',
                                      'value': False},
            'Length(2) ≤ (Length(3) + Length(1))': {'cf': False,
                                                    'ct': True,
                                                    'environmental': False,
                                                    'normal': False,
                                                    'reading': 'Length(2) ≤ (Length(3) + Length(1))',
                                                    'relevant': True,
                                                    'status': 'CONSEQUENCE',
                                                    'typ': 'Bool',
                                                    'value': True},
            'Length(3)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(3)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3) ≤ (Length(1) + Length(2))': {'cf': False,
                                                    'ct': True,
                                                    'environmental': False,
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
                          'status': 'CONSEQUENCE',
                          'typ': 'Real',
                          'value': '0'},
            '∀n[side] : (Length(n) = 0) ⇔ (Sides < n)': {'cf': False,
                                                         'ct': True,
                                                         'environmental': False,
                                                         'normal': False,
                                                         'reading': 'A polygon with N sides has N lengths',
                                                         'relevant': True,
                                                         'status': 'UNIVERSAL',
                                                         'typ': 'Bool',
                                                         'value': True},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'cf': False,
                                                                 'ct': False,
                                                                 'environmental': False,
                                                                 'normal': False,
                                                                 'reading': 'All sides have the same length',
                                                                 'relevant': True,
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'},
            '∀x[side] : 0 ≤ Length(x)': {'cf': False,
                                         'ct': True,
                                         'environmental': False,
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
               'Perimeter = (sum{n[side] : true : Length(n)})': {'cf': False,
                                                                 'ct': True,
                                                                 'environmental': False,
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
                     'value': '3',
                     'values': ['3', '4']},
           'Sides = 3': {'cf': False,
                         'ct': True,
                         'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
           'Sides = 4': {'cf': True,
                         'ct': False,
                         'environmental': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'relevant': True,
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False},
           '∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)': {'cf': False,
                                                           'ct': True,
                                                           'environmental': False,
                                                           'normal': False,
                                                           'reading': '∃n[side] : (n ≤ Sides) ∧ (Length(n) = Base)',
                                                           'relevant': True,
                                                           'status': 'UNIVERSAL',
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
             'Subtype = irregular': {'cf': False,
                                     'ct': False,
                                     'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
             'Subtype = rectangle': {'cf': True,
                                     'ct': False,
                                     'environmental': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'relevant': True,
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False},
             'Subtype = regular_triangle': {'cf': False,
                                            'ct': False,
                                            'environmental': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'relevant': True,
                                            'status': 'UNKNOWN',
                                            'typ': 'Bool'},
             'Subtype = right_triangle': {'cf': False,
                                          'ct': False,
                                          'environmental': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'relevant': True,
                                          'status': 'UNKNOWN',
                                          'typ': 'Bool'},
             'Subtype = square': {'cf': True,
                                  'ct': False,
                                  'environmental': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'relevant': True,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False}},
 'Surface': {'Surface': {'environmental': False,
                         'normal': True,
                         'reading': 'Surface',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Real',
                         'value': ''},
             'Surface = ((Base * Height) / 2)': {'cf': False,
                                                 'ct': True,
                                                 'environmental': False,
                                                 'normal': False,
                                                 'reading': 'Surface = ((Base * Height) / 2)',
                                                 'relevant': True,
                                                 'status': 'CONSEQUENCE',
                                                 'typ': 'Bool',
                                                 'value': True},
             'Surface = (-(1))': {'cf': True,
                                  'ct': False,
                                  'environmental': False,
                                  'normal': False,
                                  'reading': 'Surface = (-(1))',
                                  'relevant': False,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False},
             'Surface = (Length(1) * Length(2))': {'cf': False,
                                                   'ct': False,
                                                   'environmental': False,
                                                   'normal': False,
                                                   'reading': 'Surface = (Length(1) * Length(2))',
                                                   'relevant': False,
                                                   'status': 'UNKNOWN',
                                                   'typ': 'Bool'}},
 'Type': {'Type': {'environmental': False,
                   'normal': True,
                   'reading': 'Type',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'type',
                   'value': 'triangle',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'cf': True,
                                   'ct': False,
                                   'environmental': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': False},
          'Type = triangle': {'cf': False,
                              'ct': True,
                              'environmental': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'relevant': True,
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': True}},
 'Vertices': {'Vertices': {'environmental': False,
                           'normal': True,
                           'reading': 'Vertices',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Int',
                           'value': '3',
                           'values': ['3', '4']},
              'Vertices = 3': {'cf': False,
                               'ct': True,
                               'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 3',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True},
              'Vertices = 4': {'cf': True,
                               'ct': False,
                               'environmental': False,
                               'normal': False,
                               'reading': 'Vertices = 4',
                               'relevant': True,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False}}}
