
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
  p
Consequences:
  q
Simplified:  
  false ∨ true
Irrelevant:  
  
Co-constraints:
  true ⇔ true


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'__rank': 1,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}}}
