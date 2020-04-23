
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
    }
}

-- vocabulary -------------------------------

-- theory -----------------------------------
Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)

And((LipLen == Short) == (JacketDesign == Design_230),
    Not(LipLen == Standard))

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
  Rule:∀$LipLen$[lipLen]: LipLen($LipLen$) ⇔($LipLen$ = Short) ∧ (JacketDesign = Design_230)
Universals:  
  
Consequences:
  LipLen = Short
  ~LipLen = Standard
  JacketDesign = Design_230
  ~JacketDesign = Design_400HP
  LipLen = Short
  JacketDesign = Design_230
Simplified:  
  
Irrelevant:  
  LipLen = Short
  ~LipLen = Standard
  JacketDesign = Design_230
  ~JacketDesign = Design_400HP


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
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']},
                  'JacketDesign = Design_230': {'environmental': False,
                                                'normal': False,
                                                'reading': 'JacketDesign = Design_230',
                                                'relevant': False,
                                                'status': 'CONSEQUENCE',
                                                'typ': 'Bool',
                                                'value': True},
                  'JacketDesign = Design_400HP': {'environmental': False,
                                                  'normal': False,
                                                  'reading': 'JacketDesign = Design_400HP',
                                                  'relevant': False,
                                                  'status': 'CONSEQUENCE',
                                                  'typ': 'Bool',
                                                  'value': False}},
 'LipLen': {'LipLen': {'environmental': False,
                       'normal': True,
                       'reading': 'LipLen',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']},
            'LipLen = Short': {'environmental': False,
                               'normal': False,
                               'reading': 'LipLen = Short',
                               'relevant': False,
                               'status': 'CONSEQUENCE',
                               'typ': 'Bool',
                               'value': True},
            'LipLen = Standard': {'environmental': False,
                                  'normal': False,
                                  'reading': 'LipLen = Standard',
                                  'relevant': False,
                                  'status': 'CONSEQUENCE',
                                  'typ': 'Bool',
                                  'value': False}}}
