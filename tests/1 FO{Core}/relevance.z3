
-- original ---------------------------------
vocabulary {
    type num := {1,2}
    f : num → num
    p: () -> Bool
}

theory {
    !x in num: f(x)=f(x).
    f(1)=1 => p().
    goal_symbol := {`p}.
}

display {
    expand := {`p}.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'env_dec': False},
 'f': {'f(1)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(1)',
                'relevant': True,
                'status': 'UNKNOWN',
                'typ': 'num',
                'value': '',
                'values': ['1', '2']},
       'f(1) = 1': {'environmental': False,
                    'is_assignment': True,
                    'normal': False,
                    'reading': 'f(1) = 1',
                    'relevant': True,
                    'status': 'UNKNOWN',
                    'typ': 'Bool'},
       'f(2)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(2)',
                'relevant': False,
                'status': 'UNKNOWN',
                'typ': 'num',
                'value': '',
                'values': ['1', '2']},
       '∀ x ∈ num: f(x) = f(x)': {'environmental': False,
                                  'is_assignment': False,
                                  'normal': False,
                                  'reading': '∀ x ∈ num: f(x) = f(x)',
                                  'relevant': False,
                                  'status': 'UNIVERSAL',
                                  'typ': 'Bool',
                                  'value': True}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
