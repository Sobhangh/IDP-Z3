
-- original ---------------------------------
vocabulary {
    type color := {red, blue}
    type code := {a,b}
    codeOf: (color) → code
    c: ()→color
}

theory {
    { !cl: ! cd in code: codeOf(cl)=cd <- (cl=c() & cd=a) | (cl~=c() & cd=b). }
    codeOf(red)=b.
}

display {
    view() = expanded.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'codeOf',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'c',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'c': {'__rank': 9999,
       'c()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'c',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'color',
               'value': '',
               'values': ['red', 'blue']},
       'red = c()': {'environmental': False,
                     'is_assignment': False,
                     'normal': False,
                     'reading': 'red = c',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Bool'}},
 'codeOf': {'__rank': 9999,
            'codeOf(blue)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'code',
                             'value': '',
                             'values': ['a', 'b']},
            'codeOf(red)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'codeOf(red)',
                            'relevant': True,
                            'status': 'UNIVERSAL',
                            'typ': 'code',
                            'value': 'b',
                            'values': ['b']},
            'codeOf(red) = a': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = a',
                                'relevant': True,
                                'status': 'UNKNOWN',
                                'typ': 'Bool'},
            'codeOf(red) = b': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True}}}
