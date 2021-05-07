
-- original ---------------------------------
vocabulary {
    f:(Int)→Int
}

theory {
    f(1)>=2.
}
display { view() = expanded. }
-- meta -------------------------------------
{'optionalPropagation': False,
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
       'f(1) ≥ 2': {'environmental': False,
                    'is_assignment': False,
                    'normal': False,
                    'reading': 'f(1) ≥ 2',
                    'relevant': True,
                    'status': 'UNIVERSAL',
                    'typ': 'Bool',
                    'value': True}}}
