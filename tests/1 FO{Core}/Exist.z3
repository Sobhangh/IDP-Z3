
-- original ---------------------------------
vocabulary {
    type color := {red, blue, green}
    p: () → Bool
    q: (color) → Bool
    var c in color
}
theory {
    p() <=> ?c in color: c~=red.
    ?c: q(c).
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
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'q': {'q(blue)': {'environmental': False,
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
       '∃c ∈ None : q(c)': {'environmental': False,
                            'is_assignment': False,
                            'normal': False,
                            'reading': '∃c ∈ None : q(c)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'Bool',
                            'value': True}}}
