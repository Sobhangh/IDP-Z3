And(Sides >= 3, Sides <= 4)

And(Vertices >= 3, Vertices <= 4)

ForAll(c!4,
       Implies(Large(c!4), And(And(c!4 >= 1, c!4 <= 4))))
-- theory
Sides == 3

Or(Not(Subtype == rectangle), Length(3) == Length(1))

Equilateral ==
And(Or(Length(1) == Length(1), Sides < 1),
    Or(Length(2) == Length(1), Sides < 2),
    Or(Length(3) == Length(1), Sides < 3),
    Or(Length(4) == Length(1), Sides < 4))

(Subtype == rectangle) == (Sides == 4)

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
Subtype = rectangle
Length(3) = Length(1)
∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)
Sides = 4

-- case
Definitions: 
  
Universals:  
  Sides = 3
Consequences:
  ~Subtype = rectangle
Simplified:  
  (true)
  Equilateral ⇔ (((Length(1) = Length(1)) ∧ (Length(2) = Length(1)) ∧ (Length(3) = Length(1))))
Irrelevant:  
  Sides = 4


-- propagation
{'Angle': {'Angle(1)': {'normal': True, 'reading': 'Angle(1)', 'typ': 'Real', 'value': ''},
           'Angle(2)': {'normal': True, 'reading': 'Angle(2)', 'typ': 'Real', 'value': ''},
           'Angle(3)': {'normal': True, 'reading': 'Angle(3)', 'typ': 'Real', 'value': ''},
           'Angle(4)': {'normal': True, 'reading': 'Angle(4)', 'typ': 'Real', 'value': ''}},
 'Base': {'Base': {'normal': True, 'reading': 'Base', 'typ': 'Real', 'value': ''}},
 'Convex': {'Convex': {'cf': False,
                       'ct': False,
                       'irrelevant': True,
                       'normal': True,
                       'reading': 'Convex',
                       'typ': 'Bool'}},
 'Equilateral': {'Equilateral': {'cf': False,
                                 'ct': False,
                                 'irrelevant': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'typ': 'Bool'}},
 'Height': {'Height': {'normal': True, 'reading': 'Height', 'typ': 'Real', 'value': ''}},
 'Large': {'Large(1)': {'cf': False,
                        'ct': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(1)',
                        'typ': 'Bool'},
           'Large(2)': {'cf': False,
                        'ct': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(2)',
                        'typ': 'Bool'},
           'Large(3)': {'cf': False,
                        'ct': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(3)',
                        'typ': 'Bool'},
           'Large(4)': {'cf': False,
                        'ct': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(4)',
                        'typ': 'Bool'}},
 'Length': {'Length(1)': {'normal': True, 'reading': 'Length(1)', 'typ': 'Real', 'value': ''},
            'Length(2)': {'normal': True, 'reading': 'Length(2)', 'typ': 'Real', 'value': ''},
            'Length(3)': {'normal': True, 'reading': 'Length(3)', 'typ': 'Real', 'value': ''},
            'Length(3) = Length(1)': {'cf': False,
                                      'ct': False,
                                      'irrelevant': False,
                                      'normal': False,
                                      'reading': 'Length(3) = Length(1)',
                                      'typ': 'Bool'},
            'Length(4)': {'normal': True, 'reading': 'Length(4)', 'typ': 'Real', 'value': ''},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'cf': False,
                                                                 'ct': False,
                                                                 'irrelevant': False,
                                                                 'normal': False,
                                                                 'reading': '',
                                                                 'typ': 'Bool'}},
 'Perimeter': {'Perimeter': {'normal': True, 'reading': 'Perimeter', 'typ': 'Real', 'value': ''}},
 'Sides': {'Sides': {'normal': True, 'reading': 'Sides', 'typ': 'Int', 'value': '3', 'values': ['3', '4']},
           'Sides = 3': {'cf': False,
                         'ct': True,
                         'irrelevant': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'typ': 'Bool'},
           'Sides = 4': {'cf': False,
                         'ct': False,
                         'irrelevant': True,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'typ': 'Bool'}},
 'Subtype': {'Subtype': {'normal': True,
                         'reading': 'Subtype',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = rectangle': {'cf': False,
                                     'ct': False,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'typ': 'Bool'}},
 'Surface': {'Surface': {'normal': True, 'reading': 'Surface', 'typ': 'Real', 'value': ''}},
 'Type': {'Type': {'normal': True,
                   'reading': 'Type',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']}},
 'Vertices': {'Vertices': {'normal': True, 'reading': 'Vertices', 'typ': 'Int', 'value': '', 'values': ['3', '4']}}}
