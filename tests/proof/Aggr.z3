
-- original ---------------------------------
vocabulary {
    type color constructed from {red, blue, green}
    p
} 
theory {
    p <=> sum{c[color] : true : 1} = 3.
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
p

-- subtences ------------------------------------
p

-- GUILines ------------------------------------
p

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  p <= {'p ⇔ ((sum{c[color] : true : 1}) = 3)', 'c = green', 'c = blue', 'c = red', '(sum{c[color] : true : 1}) = 3'}
Consequences:
  
Simplified:  
  
Irrelevant:  
  


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
             'value': True}}}
