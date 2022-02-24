
-- original ---------------------------------
vocabulary {

     Base : () -> Real
     Height: () -> Real
     p: () -> Bool
}

theory {
  p() => 15.0 = Base()*Base().
  0 < Base().
  p().
  Height() = 8.0/3.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
 'Base': {'0 < Base()': {'environmental': False,
                         'is_assignment': False,
                         'normal': False,
                         'reading': '0 < Base',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Bool',
                         'value': True},
          '15.0 = Base() ⨯ Base()': {'environmental': False,
                                     'is_assignment': False,
                                     'normal': False,
                                     'reading': '15.0 = Base ⨯ Base',
                                     'relevant': True,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': True},
          'Base()': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Base',
                     'relevant': True,
                     'status': 'UNIVERSAL',
                     'typ': 'Real',
                     'value': '3.8729833462'}},
 'Height': {'Height()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'Height',
                         'relevant': True,
                         'status': 'UNIVERSAL',
                         'typ': 'Real',
                         'value': '2.6666666666666665'},
            'Height() = 8.0 / 3': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': False,
                                   'reading': 'Height = 8.0 / 3',
                                   'relevant': True,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Bool',
                                   'value': True}},
 'p': {'p()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'p',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}}}
