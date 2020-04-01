
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
And((LipLen == Short) == (JacketDesign == Design_230),
    Not(LipLen == Standard))

-- subtences ------------------------------------


-- GUILines ------------------------------------
LipLen
JacketDesign

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀['$LipLen$'][]: LipLen($LipLen$) ⇔($LipLen$ = Short) ∧ (JacketDesign = Design_230)
Universals:  
  
Consequences:
  LipLen = Short
  JacketDesign = Design_230
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'LipLen', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'JacketDesign', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}]}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'JacketDesign': {'JacketDesign': {'environmental': False,
                                   'normal': True,
                                   'reading': 'JacketDesign',
                                   'relevant': True,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'jaDes',
                                   'value': 'Design_230',
                                   'values': ['Design_230', 'Design_400HP']}},
 'LipLen': {'LipLen': {'environmental': False,
                       'normal': True,
                       'reading': 'LipLen',
                       'relevant': True,
                       'status': 'CONSEQUENCE',
                       'typ': 'lipLen',
                       'value': 'Short',
                       'values': ['Short', 'Standard']}}}
