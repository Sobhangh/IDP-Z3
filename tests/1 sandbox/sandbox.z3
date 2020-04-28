
-- original ---------------------------------
vocabulary {
    p q
}
theory {
  { p.}
  ~p|q.
}
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Not(p), q)

p

-- subtences ------------------------------------
p
q

-- GUILines ------------------------------------
p
q

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: p() ⇔true
Universals:  
  
Consequences:
  p
  q
Simplified:  
  true
Irrelevant:  
  p


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
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
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}}}
