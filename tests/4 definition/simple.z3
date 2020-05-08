
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
Or(b == red, b == blue)

Or(a == red, a == blue)

Or(b == red, b == blue)

Or(c == red, c == blue)

p == Or(q, r)

And((a == red) == p, Not(a == blue))

And((b == red) == (a == red), Not(b == blue))

And(c == red, Not(c == blue))

-- subtences ------------------------------------
b = red
p
q
r
b = blue
a = red
a = blue
c = red
c = blue

-- GUILines ------------------------------------
p
q
r
a
b
c
b = red
b = blue
a = red
a = blue
c = red
c = blue

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: p() ⇔q ∨ r
  Rule:∀$a$[color]: a($a$) ⇔$a$ = red ∧ p
  Rule:∀$b$[color]: b($b$) ⇔$b$ = red ∧ a = red
  Rule:∀$c$[color]: c($c$) ⇔$c$ = red
Universals:  
  
Consequences:
  b = red
  p
  ~b = blue
  a = red
  ~a = blue
  c = red
  ~c = blue
  a -> red
  b -> red
  c -> red
Simplified:  
  true
  true
  true
Irrelevant:  
  ~b = blue
  ~a = blue
  c = red
  ~c = blue
  c -> red


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'r', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'a', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'b', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'},
             {'idpname': 'c', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

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
       'a = blue': {'environmental': False,
                    'normal': False,
                    'reading': 'a = blue',
                    'relevant': False,
                    'status': 'CONSEQUENCE',
                    'typ': 'Bool',
                    'value': False},
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
                    'relevant': False,
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
             'relevant': False,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']},
       'c = blue': {'environmental': False,
                    'normal': False,
                    'reading': 'c = blue',
                    'relevant': False,
                    'status': 'CONSEQUENCE',
                    'typ': 'Bool',
                    'value': False},
       'c = red': {'environmental': False,
                   'normal': False,
                   'reading': 'c = red',
                   'relevant': False,
                   'status': 'CONSEQUENCE',
                   'typ': 'Bool',
                   'value': True}},
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
