
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
    (~(p)|(p)).
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p

Or(Not(p), p)

-- subtences ------------------------------------
p

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
  
Simplified:  
  p
  (true)
Irrelevant:  
  ? q
  ? r
  ? s
  ? t
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'}],
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
 'q': {'__rank': 9999,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
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
             'typ': 'Bool'}},
 't': {'__rank': 9999,
       't': {'environmental': False,
             'normal': True,
             'reading': 't',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
