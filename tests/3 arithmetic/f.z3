
-- original ---------------------------------
vocabulary {
    f:(Int)→Int
}

theory {
    f(1)>=2.
}
display { view() = expanded. }
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'f',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'f': {'__rank': 9999,
       'f(1)': {'environmental': False,
                'is_assignment': True,
                'normal': True,
                'reading': 'f(1)',
                'relevant': True,
                'status': 'UNKNOWN',
                'typ': 'Int',
                'value': ''},
       'f(1) ≥ 2': {'environmental': False,
                    'is_assignment': False,
                    'normal': False,
                    'reading': 'f(1) ≥ 2',
                    'relevant': True,
                    'status': 'UNIVERSAL',
                    'typ': 'Bool',
                    'value': True}}}
