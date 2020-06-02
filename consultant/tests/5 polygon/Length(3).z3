
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

display {
    view = expanded.
}
-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'Sides',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Length',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Subtype',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Equilateral',
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
                                 'typ': 'Bool'},
                 '__rank': 1},
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
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
            'Length(4)': {'environmental': False,
                          'normal': True,
                          'reading': 'Length(4)',
                          'relevant': False,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            '__rank': 1,
            '∀n[side] : Length(n) = Length(1) ∨ Sides < n': {'environmental': False,
                                                             'normal': False,
                                                             'reading': '∀n[side] : Length(n) = Length(1) ∨ Sides < n',
                                                             'relevant': True,
                                                             'status': 'UNKNOWN',
                                                             'typ': 'Bool'}},
 'Sides': {'Sides': {'environmental': False,
                     'normal': True,
                     'reading': 'Sides',
                     'relevant': True,
                     'status': 'UNIVERSAL',
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
                         'value': False},
           '__rank': 1},
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
                                  'typ': 'Bool'},
             '__rank': 1},
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
                              'typ': 'Bool'},
          '__rank': 9999}}
