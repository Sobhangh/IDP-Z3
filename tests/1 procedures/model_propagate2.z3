
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
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'p': {'__rank': 9999,
       'p()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Int',
               'value': '',
               'values': []},
       'p() < 3': {'environmental': False,
                   'is_assignment': False,
                   'normal': False,
                   'reading': 'p < 3',
                   'relevant': True,
                   'status': 'UNIVERSAL',
                   'typ': 'Bool',
                   'value': True}}}
