
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue, green}
    p: () → Bool
    q: (color) → Bool
}
theory {
    p <=> (?c[color]: c~=red).
    ?c[color]: q(c).
}
display {
    view = expanded.
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'__rank': 1,
       'q(blue)': {'environmental': False,
                   'is_assignment': False,
                   'normal': True,
                   'reading': 'q(blue)',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Bool'},
       'q(green)': {'environmental': False,
                    'is_assignment': False,
                    'normal': True,
                    'reading': 'q(green)',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'q(red)': {'environmental': False,
                  'is_assignment': False,
                  'normal': True,
                  'reading': 'q(red)',
                  'relevant': True,
                  'status': 'UNKNOWN',
                  'typ': 'Bool'},
       '∃c[color] : q(c)': {'environmental': False,
                            'is_assignment': False,
                            'normal': False,
                            'reading': '∃c[color] : q(c)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'Bool',
                            'value': True}}}
