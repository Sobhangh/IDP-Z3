
-- original ---------------------------------
vocabulary {
    type num := {1..4}
    Prime: (num) → Bool
}

theory {
	{ !x : Prime(x) ← !y ∈ num : 1<y & y<x => x % y ~=0.}
}
display {
    goal_symbol := {`Prime}.
    expand := {`Prime}.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Prime',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Prime': {'Prime(1)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(1)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False}}}
