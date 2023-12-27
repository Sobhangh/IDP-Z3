
-- original ---------------------------------
vocabulary {
	type num := {Jan, Piet}
    t:()→num
    t0: ()→num
    t1: ()→num
}

theory {
    { t()=t0(). t()=t1().}
    t0()=Piet.
}
-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 't',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 't0',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 't1',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 't': {'t()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 't',
               'relevant': False,
               'status': 'UNIVERSAL',
               'typ': 'num',
               'value': 'Piet',
               'values': ['Piet']}},
 't0': {'t0()': {'environmental': False,
                 'is_assignment': True,
                 'normal': True,
                 'reading': 't0',
                 'relevant': False,
                 'status': 'UNIVERSAL',
                 'typ': 'num',
                 'value': 'Piet',
                 'values': ['Piet']},
        't0() = Piet': {'environmental': False,
                        'is_assignment': True,
                        'normal': False,
                        'reading': 't0 = Piet',
                        'relevant': False,
                        'status': 'UNIVERSAL',
                        'typ': 'Bool',
                        'value': True}},
 't1': {'t1()': {'environmental': False,
                 'is_assignment': True,
                 'normal': True,
                 'reading': 't1',
                 'relevant': False,
                 'status': 'UNIVERSAL',
                 'typ': 'num',
                 'value': 'Piet',
                 'values': ['Piet']}}}
