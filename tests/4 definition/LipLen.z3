
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
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'active': '{}', 'env_dec': False},
 'JacketDesign': {'JacketDesign()': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'JacketDesign',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'jaDes',
                                     'value': '',
                                     'values': ['Design_230', 'Design_400HP']}},
 'LipLen': {'LipLen()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'LipLen',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'lipLen',
                         'value': '',
                         'values': ['Short', 'Standard']}}}
