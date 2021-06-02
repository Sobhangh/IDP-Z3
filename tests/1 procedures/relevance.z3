
-- original ---------------------------------
vocabulary {
    type num := {1,2}
    f : num → num
    p: () -> Bool
}

theory {
    !x in num: f(x)=f(x).
    f(1)=1 => p().
}

display {
    goal(`p).
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'f',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'f': {'__rank': 9999,
       'f(1)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(1)',
                'relevant': True,
                'status': 'UNKNOWN',
                'typ': 'Int',
                'value': '',
                'values': ['1', '2']},
       'f(1) = 1': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'f(1) = 1',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'f(1) = 2': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'f(1) = 2',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'f(2)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(2)',
                'relevant': False,
                'status': 'UNKNOWN',
                'typ': 'Int',
                'value': '',
                'values': ['1', '2']},
       'f(2) = 1': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'f(2) = 1',
                    'relevant': False,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'f(2) = 2': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'f(2) = 2',
                    'relevant': False,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       '∀x ∈ num : f(x) = f(x)': {'environmental': False,
                                  'is_assignment': False,
                                  'normal': False,
                                  'reading': '∀x ∈ num : f(x) = f(x)',
                                  'relevant': False,
                                  'status': 'UNIVERSAL',
                                  'typ': 'Bool',
                                  'value': True}},
 'p': {'__rank': 9999,
       'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
