
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue, green}
    p
} 
theory {
    p <=> (∀c[color]: c=red).
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
Not(p)

-- subtences ------------------------------------
p
∀c[color] : c = red

-- GUILines ------------------------------------
p
∀c[color] : c = red

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  ~p
Consequences:
  
Simplified:  
  true
Irrelevant:  
  ? ∀c[color] : c = red


-- meta -------------------------------------
{'symbols': [{'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': False}}}
