
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
{'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 's',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 9999,
       'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': False,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'q': {'__rank': 9999,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': False,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'r': {'__rank': 9999,
       'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'__rank': 9999,
       's': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
