
-- original ---------------------------------
vocabulary {
    type num := {1..4}
    Prime: (num) → Bool
}

theory {
	{ !x : Prime(x) ← !y ∈ num : 1<y & y<x => x % y ~=0.}
}
display {
    goal(`Prime).
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
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
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(2)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(2)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(3)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(3)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True},
           'Prime(4)': {'environmental': False,
                        'is_assignment': False,
                        'normal': True,
                        'reading': 'Prime(4)',
                        'relevant': True,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': False},
           '__rank': 9999}}
