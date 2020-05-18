
-- original ---------------------------------
vocabulary {
    Works(real)
    type temp = {0; 1; 2}
    p q
}
theory {
   p <=> (!t[temp]: 1 < t < 3 => 0 < t < 3).
   q <=> (!t[real]: 1 < t < 3 => 0 < t < 3).
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p

(ForAll(c!6,
        Or(Not(And(c!6 > 1, c!6 < 3)),
           And(c!6 > 0, c!6 < 3)))) ==
q

-- subtences ------------------------------------
p
∀t[temp] : 1 < t < 3 ⇒ 0 < t < 3
q
∀t[real] : 1 < t < 3 ⇒ 0 < t < 3

-- GUILines ------------------------------------
p
q
∀t[temp] : 1 < t < 3 ⇒ 0 < t < 3
∀t[real] : 1 < t < 3 ⇒ 0 < t < 3

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  p
Consequences:
  q
  ∀t[real] : 1 < t < 3 ⇒ 0 < t < 3
Simplified:  
  true ⇔ (true)
  true ⇔ (true)
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'},
             {'idpname': 'q', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}},
 'q': {'q': {'environmental': False,
             'normal': True,
             'reading': 'q',
             'relevant': True,
             'status': 'CONSEQUENCE',
             'typ': 'Bool',
             'value': True}}}
