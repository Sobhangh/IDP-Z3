
-- original ---------------------------------
vocabulary {
p q r s
x:int
}

theory {
    {p <- ~q.}
    p => s.
   x=1.
 
}

-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Not(p), s)

x == 1

p == Not(q)

-- subtences ------------------------------------
p
q
s
x = 1

-- GUILines ------------------------------------
p
q
r
s
x
x = 1

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: p() ⇔~(q)
Universals:  
  x = 1
  x -> 1
Consequences:
  
Simplified:  
  p ⇒ s
  true
Irrelevant:  
  ? r


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 's', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'},
             {'idpname': 'x', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'q': {'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'s': {'environmental': False,
             'normal': True,
             'reading': 's',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'x': {'x': {'environmental': False,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Int',
             'value': '1'},
       'x = 1': {'environmental': False,
                 'normal': False,
                 'reading': 'x = 1',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}}}
