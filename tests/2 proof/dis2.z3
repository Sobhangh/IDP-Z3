
-- original ---------------------------------
vocabulary {
    p
    q
    r
    s
    t
} 
theory {
    p.
    ~p|q.
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p

Or(Not(p), q)

-- subtences ------------------------------------
p
q

-- GUILines ------------------------------------
p
q
r
s
t

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  p
Consequences:
  q
Simplified:  
  true
  true
Irrelevant:  
  ? r
  ? s
  ? t


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'}],
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
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'s': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 't': {'t': {'environmental': False,
             'normal': True,
             'reading': 't',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
