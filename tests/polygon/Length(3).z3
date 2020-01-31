ForAll(c!91,
       Implies(Large(c!91), And(And(c!91 >= 1, c!91 <= 4))))
-- theory
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
Type:        
  ForAll(c!91,
       Implies(Large(c!91), And(And(c!91 >= 1, c!91 <= 4))))
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


-- propagation
{'Angle': {'Angle(1)': {'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Angle(1)',
                        'status': 'IRRELEVANT',
                        'typ': 'Real',
                        'value': ''},
           'Angle(2)': {'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Angle(2)',
                        'status': 'IRRELEVANT',
                        'typ': 'Real',
                        'value': ''},
           'Angle(3)': {'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Angle(3)',
                        'status': 'IRRELEVANT',
                        'typ': 'Real',
                        'value': ''},
           'Angle(4)': {'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Angle(4)',
                        'status': 'IRRELEVANT',
                        'typ': 'Real',
                        'value': ''}},
 'Base': {'Base': {'environmental': False,
                   'irrelevant': True,
                   'normal': True,
                   'reading': 'Base',
                   'status': 'IRRELEVANT',
                   'typ': 'Real',
                   'value': ''}},
 'Convex': {'Convex': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': True,
                       'normal': True,
                       'reading': 'Convex',
                       'status': 'IRRELEVANT',
                       'typ': 'Bool'}},
 'Equilateral': {'Equilateral': {'cf': False,
                                 'ct': False,
                                 'environmental': False,
                                 'irrelevant': False,
                                 'normal': True,
                                 'reading': 'Equilateral',
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Height': {'Height': {'environmental': False,
                       'irrelevant': True,
                       'normal': True,
                       'reading': 'Height',
                       'status': 'IRRELEVANT',
                       'typ': 'Real',
                       'value': ''}},
 'Large': {'Large(1)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(1)',
                        'status': 'IRRELEVANT',
                        'typ': 'Bool'},
           'Large(2)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(2)',
                        'status': 'IRRELEVANT',
                        'typ': 'Bool'},
           'Large(3)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(3)',
                        'status': 'IRRELEVANT',
                        'typ': 'Bool'},
           'Large(4)': {'cf': False,
                        'ct': False,
                        'environmental': False,
                        'irrelevant': True,
                        'normal': True,
                        'reading': 'Large(4)',
                        'status': 'IRRELEVANT',
                        'typ': 'Bool'}},
 'Length': {'Length(1)': {'environmental': False,
                          'irrelevant': False,
                          'normal': True,
                          'reading': 'Length(1)',
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(2)': {'environmental': False,
                          'irrelevant': False,
                          'normal': True,
                          'reading': 'Length(2)',
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3)': {'environmental': False,
                          'irrelevant': False,
                          'normal': True,
                          'reading': 'Length(3)',
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3) = Length(1)': {'cf': False,
                                      'ct': False,
                                      'environmental': False,
                                      'irrelevant': True,
                                      'normal': False,
                                      'reading': 'Length(3) = Length(1)',
                                      'status': 'IRRELEVANT',
                                      'typ': 'Bool'},
            'Length(4)': {'environmental': False,
                          'irrelevant': False,
                          'normal': True,
                          'reading': 'Length(4)',
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            '∀n[side] : (Length(n) = Length(1)) ∨ (Sides < n)': {'cf': False,
                                                                 'ct': False,
                                                                 'environmental': False,
                                                                 'irrelevant': False,
                                                                 'normal': False,
                                                                 'reading': '∀n[side] : (Length(n) = Length(1)) ∨ '
                                                                            '(Sides < n)',
                                                                 'status': 'UNKNOWN',
                                                                 'typ': 'Bool'}},
 'Perimeter': {'Perimeter': {'environmental': False,
                             'irrelevant': True,
                             'normal': True,
                             'reading': 'Perimeter',
                             'status': 'IRRELEVANT',
                             'typ': 'Real',
                             'value': ''}},
 'Sides': {'Sides': {'environmental': False,
                     'irrelevant': False,
                     'normal': True,
                     'reading': 'Sides',
                     'status': 'CONSEQUENCE',
                     'typ': 'Int',
                     'value': '3',
                     'values': ['3', '4']},
           'Sides = 3': {'cf': False,
                         'ct': True,
                         'environmental': False,
                         'irrelevant': False,
                         'normal': False,
                         'reading': 'Sides = 3',
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
           'Sides = 4': {'cf': True,
                         'ct': False,
                         'environmental': False,
                         'irrelevant': False,
                         'normal': False,
                         'reading': 'Sides = 4',
                         'status': 'CONSEQUENCE',
                         'typ': 'Bool',
                         'value': False}},
 'Subtype': {'Subtype': {'environmental': False,
                         'irrelevant': False,
                         'normal': True,
                         'reading': 'Subtype',
                         'status': 'UNKNOWN',
                         'typ': 'subtype',
                         'value': '',
                         'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype = rectangle': {'cf': True,
                                     'ct': False,
                                     'environmental': False,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': 'Subtype = rectangle',
                                     'status': 'CONSEQUENCE',
                                     'typ': 'Bool',
                                     'value': False}},
 'Surface': {'Surface': {'environmental': False,
                         'irrelevant': True,
                         'normal': True,
                         'reading': 'Surface',
                         'status': 'IRRELEVANT',
                         'typ': 'Real',
                         'value': ''}},
 'Type': {'Type': {'environmental': False,
                   'irrelevant': True,
                   'normal': True,
                   'reading': 'Type',
                   'status': 'IRRELEVANT',
                   'typ': 'type',
                   'value': '',
                   'values': ['triangle', 'quadrilateral']}},
 'Vertices': {'Vertices': {'environmental': False,
                           'irrelevant': True,
                           'normal': True,
                           'reading': 'Vertices',
                           'status': 'IRRELEVANT',
                           'typ': 'Int',
                           'value': '',
                           'values': ['3', '4']}}}
