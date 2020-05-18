
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
  true ⇒ (r ∨ s)
  p
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'r', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 's', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

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
