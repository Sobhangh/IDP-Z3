
-- original ---------------------------------
vocabulary {
    p q r s
}
theory {
    p => q & (r|s).
    p.
}
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Not(p), And(q, Or(r, s)))

p

-- subtences ------------------------------------
p
q
r
s

-- GUILines ------------------------------------
p
q
r
s

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  p
Consequences:
  q
Simplified:  
  (((r ∨ s)))
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'p', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'q', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'r', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 's', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}]}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'s': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
