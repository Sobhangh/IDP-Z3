
-- original ---------------------------------
vocabulary {
    type color := {red, blue, green}
    p, q : () → 𝔹
    r: color -> Int
    val: () -> Int
}

theory {
    if p(),
    then val() = 2 +(if q() then 1 else 0)
    and for all color c: 0 =< r(c).
    p().
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
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'val',
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
               'relevant': False,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'q': {'q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'q',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'r': {'r(blue)': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'r(blue)',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int'},
       'r(green)': {'environmental': False,
                    'is_assignment': True,
                    'normal': True,
                    'reading': 'r(green)',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Int'},
       'r(red)': {'environmental': False,
                  'is_assignment': True,
                  'normal': True,
                  'reading': 'r(red)',
                  'relevant': True,
                  'status': 'UNKNOWN',
                  'typ': 'Int'},
       '∀ c ∈ color: 0 ≤ r(c)': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': False,
                                 'reading': '∀ c ∈ color: 0 ≤ r(c)',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True}},
 'val': {'val()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'val',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int'},
         'val() = 2 + (if q() then 1 else 0)': {'environmental': False,
                                                'is_assignment': False,
                                                'normal': False,
                                                'reading': 'val = 2 + (if q then 1 else 0)',
                                                'relevant': True,
                                                'status': 'UNIVERSAL',
                                                'typ': 'Bool',
                                                'value': True}}}
