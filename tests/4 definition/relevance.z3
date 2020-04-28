
-- original ---------------------------------
vocabulary {
    p q1 q2 r s
}
theory {
  { s <- r.}
  { p <- q1 | q2.}
  { q1 <- r.} 
  q1.
}
goal p
-- vocabulary -------------------------------

-- theory -----------------------------------
q1

s == r

p == Or(q1, q2)

q1 == r

-- goal -----------------------------------
And(p == Or(q1, q2), q1 == r)

-- subtences ------------------------------------
q1
r
p
q2

-- GUILines ------------------------------------
p
q1
q2
r
s

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: s() ⇔r
  Rule:∀: p() ⇔q1 ∨ q2
  Rule:∀: q1() ⇔r
Universals:  
  q1
Consequences:
  r
  p
  s
Simplified:  
  true
Irrelevant:  
  s


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q1', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'q2', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'r', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 's', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'q1': {'q1': {'environmental': False,
               'normal': True,
               'reading': 'q1',
               'relevant': True,
               'status': 'UNIVERSAL',
               'typ': 'Bool',
               'value': True}},
 'q2': {'q2': {'environmental': False,
               'normal': True,
               'reading': 'q2',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 's': {'s': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': False,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}}}
