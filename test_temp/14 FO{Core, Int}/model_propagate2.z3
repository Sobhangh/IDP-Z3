
-- original ---------------------------------
vocabulary  {
    type T:={1..5}
    p :  () → T
}
theory  {
    p()<3.
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
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Int',
               'values': ['1', '2', '3', '4', '5']},
       'p() < 3': {'environmental': False,
                   'is_assignment': False,
                   'normal': False,
                   'reading': 'p < 3',
                   'relevant': False,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True}}}
