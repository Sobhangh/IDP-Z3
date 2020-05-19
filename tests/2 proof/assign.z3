
-- original ---------------------------------
vocabulary {
    x:int
    y:int
} 
theory {
    x=0.
    ~(x=0)|(x=0).
}
view expanded
-- vocabulary -------------------------------

-- theory -----------------------------------
x == 0

Or(Not(x == 0), x == 0)

-- subtences ------------------------------------
x = 0

-- GUILines ------------------------------------
x
y
x = 0

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  x -> 0
  x = 0
Consequences:
  
Simplified:  
  0 = 0
  false ∨ (true)
Irrelevant:  
  ? y
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'x', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'x': {'__rank': 1,
       'x': {'environmental': False,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Int',
             'value': '0'},
       'x = 0': {'environmental': False,
                 'normal': False,
                 'reading': 'x = 0',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}},
 'y': {'__rank': 9999,
       'y': {'environmental': False,
             'normal': True,
             'reading': 'y',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Int',
             'value': ''}}}
