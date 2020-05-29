
-- original ---------------------------------
vocabulary {
    p
    q
    r
    s
    t
} 
theory {
    {q <-r.}
    {p <- ~q.}
    p|~p. r.
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(p, Not(p))

r

q == r

p == Not(q)

-- subtences ------------------------------------
p
q
r

-- GUILines ------------------------------------
p
q
r
s
t

-- case -------------------------------------
Type:        
  
Definitions: 
  Rule:∀: q() ⇔r
  Rule:∀: p() ⇔~(q)
Universals:  
  r
Consequences:
  ~p
  q
Simplified:  
  false ∨ true
  r
Irrelevant:  
  ? s
  ? t
Co-constraints:
  false ⇔ false
  true ⇔ true


-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'p',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'},
             {'environmental': False,
              'idpname': 'r',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'__rank': 1,
       'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': False}},
 'q': {'__rank': 1,
       'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}},
 'r': {'__rank': 1,
       'r': {'environmental': False,
             'normal': True,
             'reading': 'r',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
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
