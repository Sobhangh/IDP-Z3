ForAll(c!253,
       Implies(Large(c!253),
               And(And(c!253 >= 1, c!253 <= 4))))
-- theory
True

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

Equilateral == And(Sides < 2, Sides < 3, Sides < 4)

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

Not(Subtype == rectangle)

(Subtype == square) == And(Sides == 4, Equilateral)

True

Perimeter == 10

Angle(1) + Angle(2) + Angle(3) + Angle(4) ==
ToReal(180*(-2 + Sides))

True

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

And(Not(Sides < 1),
    Not(Sides < 2),
    Not(Sides < 3),
    Not(Sides < 4))

And(Sides >= 3, Sides <= 4)

And(Vertices >= 3, Vertices <= 4)

ForAll(c!256, Large(c!256) == False)

-- atoms
Sides
Vertices
Type
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
∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
Perimeter = (sum{n[side] : true : Length(n)})
(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
∀x[side] : 0 ≤ Angle(x)
∀x[side] : Angle(x) ≠ 180
∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
∀n[side] : (Length(n) = 0) ⇔ (Sides < n)

-- case
Type:        
  ForAll(c!253,
       Implies(Large(c!253),
               And(And(c!253 >= 1, c!253 <= 4))))
Definitions: 
  Rule:∀[][[]]: Large(1) ⇔(false)
Rule:∀[][[]]: Large(2) ⇔(false)
Rule:∀[][[]]: Large(3) ⇔(false)
Rule:∀[][[]]: Large(4) ⇔(false)
Universals:  
  ~Subtype = rectangle
  Perimeter = (sum{n[side] : true : Length(n)})
  (sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)
  ∀x[side] : 0 ≤ Angle(x)
  ∀x[side] : Angle(x) ≠ 180
  ∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)
Consequences:
  ~Type = triangle
  ~Sides = 3
  Type = quadrilateral
  Sides = 4
  ~Vertices = 3
  Vertices = 4
  ~Equilateral
  ~∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
  ~Subtype = right_triangle
  ~Subtype = regular_triangle
  ~Subtype = square
  ~∀n[side] : (Angle(n) = 90) ∨ (Sides < n)
  ∀n[side] : (Length(n) = 0) ⇔ (Sides < n)
Simplified:  
  (Convex ⇔ (((Angle(1) < 180) ∧ (Angle(2) < 180) ∧ (Angle(3) < 180) ∧ (Angle(4) < 180))))
Irrelevant:  
  Subtype = irregular
  ((Angle(1) = 60) ∧ (Angle(2) = 60) ∧ (Angle(3) = 60) ∧ (Angle(4) = 60))
  ((Angle(1) = 90) ∨ (Angle(2) = 90) ∨ (Angle(3) = 90) ∨ (Angle(4) = 90))


-- propagation
{'Angle': {'(sum{n[side] : true : Angle(n)}) = ((Sides - 2) * 180)': {'cf': False,
                                                                      'ct': True,
                                                                      'irrelevant': False,
                                                                      'normal': False,
                                                                      'reading': 'The sum of the angles is 180° for a '
                                                                                 'triangle, and 360° for a '
                                                                                 'quadrilateral',
                                                                      'status': 'UNIVERSAL',
                                                                      'typ': 'Bool',
                                                                      'value': True},
           'Angle(1)': {'normal': True, 'reading': 'Angle(1)', 'typ': 'Real', 'value': ''},
           'Angle(2)': {'normal': True, 'reading': 'Angle(2)', 'typ': 'Real', 'value': ''},
           'Angle(3)': {'normal': True, 'reading': 'Angle(3)', 'typ': 'Real', 'value': ''},
           'Angle(4)': {'normal': True, 'reading': 'Angle(4)', 'typ': 'Real', 'value': ''},
           '∀n[side] : (Angle(n) = 0) ⇔ (Vertices < n)': {'cf': False,
                                                          'ct': True,
                                                          'irrelevant': False,
                                                          'normal': False,
                                                          'reading': 'A polygon with N vertices has N angles',
                                                          'status': 'UNIVERSAL',
                                                          'typ': 'Bool',
                                                          'value': True},
           '∀n[side] : (Angle(n) = 60) ∨ (Sides < n)': {'cf': False,
                                                        'ct': False,
                                                        'irrelevant': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 60°',
                                                        'status': 'UNKNOWN',
                                                        'typ': 'Bool'},
           '∀n[side] : (Angle(n) = 90) ∨ (Sides < n)': {'cf': True,
                                                        'ct': False,
                                                        'irrelevant': False,
                                                        'normal': False,
                                                        'reading': 'All angles are 90°',
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': False},
           '∀n[side] : Angle(n) < 180': {'cf': False,
                                         'ct': False,
                                         'irrelevant': False,
                                         'normal': False,
                                         'reading': 'All angles are below 180°',
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
           '∀x[side] : 0 ≤ Angle(x)': {'cf': False,
                                       'ct': True,
                                       'irrelevant': False,
                                       'normal': False,
                                       'reading': 'Angles are positive numbers',
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
           '∀x[side] : Angle(x) ≠ 180': {'cf': False,
                                         'ct': True,
                                         'irrelevant': False,
                                         'normal': False,
                                         'reading': 'Angles cannot be 180°',
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
           '∃n[side] : Angle(n) = 90': {'cf': False,
                                        'ct': False,
                                        'irrelevant': False,
                                        'normal': False,
                                        'reading': 'One angle is 90°',
                                        'status': 'UNKNOWN',
                                        'typ': 'Bool'}},
 'Convex': {'Convex': {'cf': False,
                       'ct': False,
                       'irrelevant': False,
                       'normal': True,
                       'reading': 'Convex',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}},
 'Equilateral': {'Equilateral': {'cf': True,
                                 'ct': False,
                                 'irrelevant': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': False}},
 'Large': {'Large(1)': {'cf': True,
                        'ct': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Large(1)',
                        'status': 'UNKNOWN',
                        'typ': 'Bool',
                        'value': False},
           'Large(2)': {'cf': True,
                        'ct': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Large(2)',
                        'status': 'UNKNOWN',
                        'typ': 'Bool',
                        'value': False},
           'Large(3)': {'cf': True,
                        'ct': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Large(3)',
                        'status': 'UNKNOWN',
                        'typ': 'Bool',
                        'value': False},
           'Large(4)': {'cf': True,
                        'ct': False,
                        'irrelevant': False,
                        'normal': True,
                        'reading': 'Large(4)',
                        'status': 'UNKNOWN',
                        'typ': 'Bool',
                        'value': False}},
 'Perimeter': {'Perimeter': {'normal': True, 'reading': 'Perimeter', 'typ': 'Real', 'value': '10'},
               'Perimeter = (sum{n[side] : true : Length(n)})': {'cf': False,
                                                                 'ct': True,
                                                                 'irrelevant': False,
                                                                 'normal': False,
                                                                 'reading': 'The perimeter is the sum of the lengths '
                                                                            'of the sides',
                                                                 'status': 'UNIVERSAL',
                                                                 'typ': 'Bool',
                                                                 'value': True}},
 'Sides': {'Sides': {'normal': True, 'reading': 'Sides', 'typ': 'Int', 'value': '4', 'values': ['3', '4']},
           'Sides = 3': {'cf': True,
                         'ct': False,
                         'irrelevant': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False},
           'Sides = 4': {'cf': False,
                         'ct': True,
                         'irrelevant': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': True},
           '∀n[side] : (Length(n) = 0) ⇔ (Sides < n)': {'cf': False,
                                                        'ct': True,
                                                        'irrelevant': False,
                                                        'normal': False,
                                                        'reading': 'A polygon with N sides has N lengths',
                                                        'status': 'CONSEQUENCE',
                                                        'typ': 'Bool',
                                                        'value': True},
           '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'cf': True,
                                                                'ct': False,
                                                                'irrelevant': False,
                                                                'normal': False,
                                                                'reading': 'All sides have the same length',
                                                                'status': 'CONSEQUENCE',
                                                                'typ': 'Bool',
                                                                'value': False}},
 'Subtype': {'Subtype': {'normal': True,
                         'reading': 'Subtype',
                         'typ': 'subtype',
                         'value': 'irregular',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = irregular': {'cf': False,
                                     'ct': True,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Subtype = irregular',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool',
                                     'value': True},
             'Subtype = rectangle': {'cf': True,
                                     'ct': False,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': False},
             'Subtype = regular_triangle': {'cf': True,
                                            'ct': False,
                                            'irrelevant': False,
                                            'normal': False,
                                            'reading': 'Subtype = regular_triangle',
                                            'status': 'CONSEQUENCE',
                                            'typ': 'Bool',
                                            'value': False},
             'Subtype = right_triangle': {'cf': True,
                                          'ct': False,
                                          'irrelevant': False,
                                          'normal': False,
                                          'reading': 'Subtype = right_triangle',
                                          'status': 'CONSEQUENCE',
                                          'typ': 'Bool',
                                          'value': False},
             'Subtype = square': {'cf': True,
                                  'ct': False,
                                  'irrelevant': False,
                                  'normal': False,
                                  'reading': 'Subtype = square',
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False}},
 'Type': {'Type': {'normal': True,
                   'reading': 'Type',
                   'typ': 'type',
                   'value': 'quadrilateral',
                   'values': ['triangle', 'quadrilateral']},
          'Type = quadrilateral': {'cf': False,
                                   'ct': True,
                                   'irrelevant': False,
                                   'normal': False,
                                   'reading': 'Type = quadrilateral',
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': True},
          'Type = triangle': {'cf': True,
                              'ct': False,
                              'irrelevant': False,
                              'normal': False,
                              'reading': 'Type = triangle',
                              'status': 'CONSEQUENCE',
                              'typ': 'Bool',
                              'value': False}},
 'Vertices': {'Vertices': {'normal': True, 'reading': 'Vertices', 'typ': 'Int', 'value': '4', 'values': ['3', '4']},
              'Vertices = 3': {'cf': True,
                               'ct': False,
                               'irrelevant': False,
                               'normal': False,
                               'reading': 'Vertices = 3',
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': False},
              'Vertices = 4': {'cf': False,
                               'ct': True,
                               'irrelevant': False,
                               'normal': False,
                               'reading': 'Vertices = 4',
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True}}}
