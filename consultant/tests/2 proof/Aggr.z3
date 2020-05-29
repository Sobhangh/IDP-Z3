
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
sum{c[color] : true : 1} = 3

-- GUILines ------------------------------------
p
sum{c[color] : true : 1} = 3

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  p
Consequences:
  
Simplified:  
  true ⇔ true
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'p',
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
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
