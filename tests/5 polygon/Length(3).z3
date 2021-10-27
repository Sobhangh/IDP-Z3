
-- original ---------------------------------
vocabulary {

    type sides := {3..4}
    Sides: ()→sides


    type type := {triangle, quadrilateral}
    Type : ()→type

    type side := {1..4}
    Length: (side)→Real

    type subtype :=
        { regular_triangle
        , right_triangle
        , rectangle
        , square
        , irregular}
    Subtype : ()→subtype

    Equilateral:() → Bool
}

theory {
    Sides()=3.

    Subtype()=rectangle => Length(3)=Length(1).

    Equilateral() <=> (∀n in side: Length(n)=Length(1) | Sides() < n).

    Subtype()=rectangle <=> Sides()=4.

}

display {
    view() = expanded.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Sides',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'Type',
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
{' Global': {'active': '{}', 'env_dec': False},
 'Equilateral': {'Equilateral()': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': True,
                                   'reading': 'Equilateral',
                                   'relevant': True,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'}},
 'Length': {'Length(1)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Length(1)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(2)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Length(2)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Length(3)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            'Length(3) = Length(1)': {'environmental': False,
                                      'is_assignment': False,
                                      'normal': False,
                                      'reading': 'Length(3) = Length(1)',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
            'Length(4)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Length(4)',
                          'relevant': False,
                          'status': 'UNKNOWN',
                          'typ': 'Real',
                          'value': ''},
            '∀n ∈ side : Length(n) = Length(1) ∨ Sides() < n': {'environmental': False,
                                                                'is_assignment': False,
                                                                'normal': False,
                                                                'reading': '∀n ∈ side : Length(n) = Length(1) ∨ Sides '
                                                                           '< n',
                                                                'relevant': True,
                                                                'status': 'UNKNOWN',
                                                                'typ': 'Bool'}},
 'Sides': {'Sides()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Sides',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Int',
                       'value': '3',
                       'values': ['3']},
           'Sides() = 3': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 3',
                           'relevant': True,
                           'status': 'UNIVERSAL',
                           'typ': 'Bool',
                           'value': True},
           'Sides() = 4': {'environmental': False,
                           'is_assignment': True,
                           'normal': False,
                           'reading': 'Sides = 4',
                           'relevant': True,
                           'status': 'CONSEQUENCE',
                           'typ': 'Bool',
                           'value': False}},
 'Subtype': {'Subtype()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'Subtype',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'subtype',
                           'value': '',
                           'values': ['regular_triangle', 'right_triangle', 'rectangle', 'square', 'irregular']},
             'Subtype() = rectangle': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'Subtype = rectangle',
                                       'relevant': True,
                                       'status': 'CONSEQUENCE',
                                       'typ': 'Bool',
                                       'value': False}},
 'Type': {'Type()': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Type',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'type',
                     'value': '',
                     'values': ['triangle', 'quadrilateral']}}}
