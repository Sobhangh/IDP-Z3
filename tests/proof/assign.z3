
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
  x = 0
  x = 0
Consequences:
  
Simplified:  
  
Irrelevant:  
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'x', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'expanded'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'x': {'x': {'environmental': False,
             'normal': True,
             'reading': 'x',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Int',
             'value': ''},
       'x = 0': {'environmental': False,
                 'normal': False,
                 'reading': 'x = 0',
                 'relevant': True,
                 'status': 'UNIVERSAL',
                 'typ': 'Bool',
                 'value': True}},
 'y': {'y': {'environmental': False,
             'normal': True,
             'reading': 'y',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Int',
             'value': ''}}}
