
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
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'f',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
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
                'typ': 'Int'},
       'f(1) ≥ 2': {'environmental': False,
                    'is_assignment': False,
                    'normal': False,
                    'reading': 'f(1) ≥ 2',
                    'relevant': False,
                    'status': 'UNIVERSAL',
                    'typ': 'Bool',
                    'value': True}}}
