
-- original ---------------------------------
vocabulary {

     Base : Real
     Height: Real
     p
}

theory {
  p => 15.0 = Base*Base.
  0 < Base.
  p.
  Height = 8.0/3.
}
-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Base',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Height',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Base': {'0 < Base': {'environmental': False,
                       'is_assignment': False,
                       'normal': False,
                       'reading': '0 < Base',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          '15.0 = Base * Base': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': False,
                                 'reading': '15.0 = Base * Base',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
          'Base': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Base',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Real',
                   'value': '3.8729833462'},
          '__rank': 1},
 'Height': {'Height': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Height',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Real',
                       'value': '2.6666666666666665'},
            'Height = 8.0 / 3': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': False,
                                 'reading': 'Height = 8.0 / 3',
                                 'relevant': True,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True},
            '__rank': 1},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
