
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
 
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p == Or(q, r)

And((a == red) == p, (a == blue) == False)

And((b == red) == (a == red), (b == blue) == False)

And((c == red) == True, (c == blue) == False)

-- atoms ------------------------------------
p
q
r
a
b
c

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][]: p() ⇔q ∨ r
  Rule:∀['$a$'][]: a($a$) ⇔($a$ = red) ∧ p
  Rule:∀['$b$'][]: b($b$) ⇔($b$ = red) ∧ (a = red)
  Rule:∀['$c$'][]: c($c$) ⇔($c$ = red)
Universals:  
  
Consequences:
  p
  a = red
  b = red
  c = red
Simplified:  
  
Irrelevant:  
  


-- propagation ------------------------------
{' Global': {'env_dec': False},
 'a': {'a': {'environmental': False,
             'normal': True,
             'reading': 'a',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']}},
 'b': {'b': {'environmental': False,
             'normal': True,
             'reading': 'b',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'color',
             'value': 'red',
             'values': ['red', 'blue']}},
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
