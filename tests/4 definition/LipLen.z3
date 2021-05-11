
-- original ---------------------------------
vocabulary {
    type lipLen := {Short, Standard}
    type jaDes := {Design_230, Design_400HP}
    LipLen: () →lipLen
    JacketDesign: ()→jaDes
}

theory {
    {
        LipLen() = Short <- JacketDesign() = Design_230.
        LipLen() = Standard <- JacketDesign() = Design_400HP.
    }
}
-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'LipLen',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'JacketDesign',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'JacketDesign': {'JacketDesign()': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'JacketDesign',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'jaDes',
                                     'value': '',
                                     'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign() = Design_230': {'environmental': False,
                                                  'is_assignment': True,
                                                  'normal': False,
                                                  'reading': 'JacketDesign = Design_230',
                                                  'relevant': False,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'},
                  'JacketDesign() = Design_400HP': {'environmental': False,
                                                    'is_assignment': True,
                                                    'normal': False,
                                                    'reading': 'JacketDesign = Design_400HP',
                                                    'relevant': False,
                                                    'status': 'UNKNOWN',
                                                    'typ': 'Bool'},
                  '__rank': 9999},
 'LipLen': {'LipLen()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'LipLen',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'lipLen',
                         'value': '',
                         'values': ['Short', 'Standard']},
            'LipLen() = Short': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': False,
                                 'reading': 'LipLen = Short',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'},
            'LipLen() = Standard': {'environmental': False,
                                    'is_assignment': True,
                                    'normal': False,
                                    'reading': 'LipLen = Standard',
                                    'relevant': False,
                                    'status': 'UNKNOWN',
                                    'typ': 'Bool'},
            '__rank': 9999}}
