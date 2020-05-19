
-- original ---------------------------------
vocabulary {
    p
    q
    r
    s
} 

theory {
    { p <- q | r. }
    p|s.
    q.
}
goal b
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(p, s)

q

p == Or(q, r)

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
  Rule:∀: p() ⇔q ∨ r
Universals:  
  q
Consequences:
  p
Simplified:  
  
Irrelevant:  
  p
  q
  ? r
  ? s
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'r', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 's', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': False,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'q': {'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': False,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'s': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
