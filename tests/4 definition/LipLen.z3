
-- original ---------------------------------
vocabulary {
    type lipLen constructed from {Short, Standard}
    type jaDes constructed from {Design_230, Design_400HP}
    LipLen: lipLen
    JacketDesign: jaDes
}

theory {
    {        
        LipLen = Short <- JacketDesign = Design_230.
        LipLen = Standard <- JacketDesign = Design_400HP.
    }
}
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)

And((LipLen == Short) == (JacketDesign == Design_230),
    (LipLen == Standard) == (JacketDesign == Design_400HP))

-- subtences ------------------------------------
LipLen = Short
LipLen = Standard
JacketDesign = Design_230
JacketDesign = Design_400HP

-- GUILines ------------------------------------
LipLen
JacketDesign
LipLen = Short
LipLen = Standard
JacketDesign = Design_230
JacketDesign = Design_400HP

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀$LipLen$[lipLen]: LipLen($LipLen$) ⇔$LipLen$ = Short ∧ JacketDesign = Design_230 ∨ $LipLen$ = Standard ∧ JacketDesign = Design_400HP
Universals:  
  
Consequences:
  
Simplified:  
  
Irrelevant:  
  ? LipLen = Short
  ? LipLen = Standard
  ? JacketDesign = Design_230
  ? JacketDesign = Design_400HP
  ? LipLen
  ? JacketDesign
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'LipLen', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'JacketDesign',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'JacketDesign': {'JacketDesign': {'environmental': False,
                                   'normal': True,
                                   'reading': 'JacketDesign',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'jaDes',
                                   'value': '',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'environmental': False,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'relevant': False,
                                                'status': 'UNKNOWN',
                                                'typ': 'Bool'},
                  'JacketDesign = Design_400HP': {'environmental': False,
                                                  'normal': False,
                                                  'reading': 'JacketDesign = Design_400HP',
                                                  'relevant': False,
                                                  'status': 'UNKNOWN',
                                                  'typ': 'Bool'}},
 'LipLen': {'LipLen': {'environmental': False,
                       'normal': True,
                       'reading': 'LipLen',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'lipLen',
                       'value': '',
                       'values': ['Short', 'Standard']},
            'LipLen = Short': {'environmental': False,
                               'normal': False,
                               'reading': 'LipLen = Short',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
            'LipLen = Standard': {'environmental': False,
                                  'normal': False,
                                  'reading': 'LipLen = Standard',
                                  'relevant': False,
                                  'status': 'UNKNOWN',
                                  'typ': 'Bool'}}}
