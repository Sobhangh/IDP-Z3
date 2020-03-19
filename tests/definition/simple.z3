
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
p == Or(Or(q, r))

ForAll(c!34, (a == c!34) == Or(And(c!34 == red, p)))

ForAll(c!35, (b == c!35) == Or(And(c!35 == red, a == red)))

ForAll(c!36, (c == c!36) == Or(c!36 == red))

-- atoms ------------------------------------
p
q
r
a
b
c
a = red

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][[]]: p() ⇔q ∨ r
  Rule:∀[][[]]: a(red) ⇔($a$ = red) ∧ p
  Rule:∀[][[]]: b(red) ⇔($b$ = red) ∧ (a = red)
  Rule:∀[][[]]: c(red) ⇔($c$ = red)
Universals:  
  
Consequences:
  p
  a = red
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
