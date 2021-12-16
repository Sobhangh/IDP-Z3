
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
{' Global': {'env_dec': False},
 'c': {'c()': {'environmental': False,
               'is_assignment': True,
               'normal': True,
               'reading': 'c',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'color',
               'value': 'blue',
               'values': ['blue']},
       'red = c()': {'environmental': False,
                     'is_assignment': False,
                     'normal': False,
                     'reading': 'red = c',
                     'relevant': True,
                     'status': 'UNIVERSAL',
                     'typ': 'Bool',
                     'value': False}},
 'codeOf': {'codeOf(blue)': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'codeOf(blue)',
                             'relevant': False,
                             'status': 'UNIVERSAL',
                             'typ': 'code',
                             'value': 'a',
                             'values': ['a']},
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
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': False},
            'codeOf(red) = b': {'environmental': False,
                                'is_assignment': True,
                                'normal': False,
                                'reading': 'codeOf(red) = b',
                                'relevant': True,
                                'status': 'UNIVERSAL',
                                'typ': 'Bool',
                                'value': True}}}
