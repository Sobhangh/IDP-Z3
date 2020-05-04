
-- original ---------------------------------
vocabulary {
    p l r rd i
}
theory {
  { i <- rd.}
  { p <- l | r.}
  { r <- rd.} 
  r.
}
goal p
-- vocabulary -------------------------------

-- theory -----------------------------------
r

Or(p, Not(p))

i == rd

p == Or(l, r)

r == rd

-- subtences ------------------------------------
r
rd
p
l

-- GUILines ------------------------------------
p
l
r
rd
i

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: i() ⇔rd
  Rule:∀: p() ⇔l ∨ r
  Rule:∀: r() ⇔rd
Universals:  
  r
Consequences:
  rd
  p
  i
Simplified:  
  true
  true
Irrelevant:  
  ? l
  i


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'l', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'r', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'rd', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'i', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'i': {'i': {'environmental': False,
             'normal': True,
             'reading': 'i',
             'relevant': False,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'l': {'l': {'environmental': False,
             'normal': True,
             'reading': 'l',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'rd': {'rd': {'environmental': False,
               'normal': True,
               'reading': 'rd',
               'relevant': True,
               'status': 'CONSEQUENCE',
               'typ': 'Bool',
               'value': True}}}
