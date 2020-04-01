
-- original ---------------------------------
vocabulary {
    p
    q
    r
    type color constructed from {red, blue}
    a : color
    b : color
    c : color
} 

theory {
    { p <- q | r. }
    { a=red <- p. }
    { b=red <- a=red. }
    { c=red. }
}
goal b
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p == Or(q, r)

And((a == red) == p, Not(a == blue))

And((b == red) == (a == red), Not(b == blue))

And(c == red, Not(c == blue))

-- goal -----------------------------------
And(And(a == red, p),
    p == Or(q, r),
    Or((b == red) == (a == red), Not(b == blue)))

-- subtences ------------------------------------
a = red
p
q
r
b = red
b = blue

-- GUILines ------------------------------------
p
q
r
a
b
c
a = red
b = red
b = blue

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][]: p() ⇔q ∨ r
  Rule:∀['$a$'][]: a($a$) ⇔($a$ = red) ∧ p
  Rule:∀['$b$'][]: b($b$) ⇔($b$ = red) ∧ (a = red)
  Rule:∀['$c$'][]: c($c$) ⇔($c$ = red)
Universals:  
  
Consequences:
  a = red
  p
  b = red
  ~b = blue
  a = red
  b = red
  c = red
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'title': 'Interactive Consultant', 'symbols': [{'idpname': 'p', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'q', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'r', 'type': 'proposition', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'a', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'b', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}, {'idpname': 'c', 'type': 'function', 'priority': 'core', 'showOptimize': True, 'view': 'expanded'}]}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'a': {'a': {'environmental': False,
             'normal': True,
             'reading': 'a',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']},
       'a = red': {'environmental': False,
                   'normal': False,
                   'reading': 'a = red',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': True}},
 'b': {'b': {'environmental': False,
             'normal': True,
             'reading': 'b',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']},
       'b = blue': {'environmental': False,
                    'normal': False,
                    'reading': 'b = blue',
                    'relevant': True,
                    'status': 'CONSEQUENCE',
                    'typ': 'Bool',
                    'value': False},
       'b = red': {'environmental': False,
                   'normal': False,
                   'reading': 'b = red',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': True}},
 'c': {'c': {'environmental': False,
             'normal': True,
             'reading': 'c',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']}},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'q': {'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'r': {'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
