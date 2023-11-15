
-- original ---------------------------------
vocabulary {
    type color := {red, blue, green}
    p: () → Bool
    q: (color) → Bool
    var c in color
    c2: () -> Bool
}
theory {
    p() <=> ?c in color: c~=red.
    ?c: q(c).
    !c1: ?c3:q(c3).
    c2().
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
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'c2',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'c2': {'c2()': {'environmental': False,
                 'is_assignment': False,
                 'normal': True,
                 'reading': 'c2',
                 'relevant': False,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': False,
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
       '∀ c1: ∃ c3: q(c3)': {'environmental': False,
                             'is_assignment': False,
                             'normal': False,
                             'reading': '∀ c1: ∃ c3: q(c3)',
                             'relevant': False,
                             'status': 'UNIVERSAL',
                             'typ': 'Bool',
                             'value': True},
       '∃ c: q(c)': {'environmental': False,
                     'is_assignment': False,
                     'normal': False,
                     'reading': '∃ c: q(c)',
                     'relevant': False,
                     'status': 'UNIVERSAL',
                     'typ': 'Bool',
                     'value': True}}}
