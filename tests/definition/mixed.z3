
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
  Rule:∀[][]: p() ⇔~(q)
Universals:  
  x = 1
Consequences:
  x = 1
Simplified:  
  p ⇒ s
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'p', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'q', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 's', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}, {'idpname': 'x', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'normal'}]}

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
             'status': 'CONSEQUENCE',
             'typ': 'Int',
             'value': '1'},
       'x = 1': {'environmental': False,
                 'normal': False,
                 'reading': 'x = 1',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}}}
