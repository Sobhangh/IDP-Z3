
-- original ---------------------------------
vocabulary {
    p
    q
    r
    s
    t
} 

theory {
    {p <- q.}
    {q <- r.}
    {r <- s.}
    {s <- t.}
}
goal p
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p == q

q == r

r == s

s == t

-- goal -----------------------------------
And(p == q, q == r, r == s, s == t)

-- subtences ------------------------------------
p
q
r
s
t

-- GUILines ------------------------------------
p
q
r
s
t

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀[][]: p() ⇔q
  Rule:∀[][]: q() ⇔r
  Rule:∀[][]: r() ⇔s
  Rule:∀[][]: s() ⇔t
Universals:  
  
Consequences:
  
Simplified:  
  
Irrelevant:  
  


-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': False,
             'reading': 'p',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'q': {'q': {'environmental': False,
             'normal': False,
             'reading': 'q',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 'r': {'r': {'environmental': False,
             'normal': False,
             'reading': 'r',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 's': {'s': {'environmental': False,
             'normal': False,
             'reading': 's',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}},
 't': {'t': {'environmental': False,
             'normal': True,
             'reading': 't',
             'relevant': True,
             'status': 'UNKNOWN',
             'typ': 'Bool'}}}
