
-- original ---------------------------------
vocabulary {
    
     Base : real
     Height: real
     p
}

theory {
  p => 15.0 = Base*Base.
  0 < Base.
  p.
  Height = 8.0/3.
}
-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Not(p), Base*Base == 15)

Base > 0

p

Height == 5333333333333333/2000000000000000

-- subtences ------------------------------------
p
15.0 = Base * Base
0 < Base
Height = 8.0 / 3

-- GUILines ------------------------------------
Base
Height
p
15.0 = Base * Base
0 < Base
Height = 8.0 / 3

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  Height -> 2.6666666666666665
  p
  0 < Base
  Height = 8.0 / 3
Consequences:
  Base -> 3.8729833462?
  15.0 = Base * Base
Simplified:  
  true ⇒ false
  0 < 3.8729833462?
  p
  2.6666666666666665 = 2.6666666666666665
Irrelevant:  
  
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [{'idpname': 'Base', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'Height', 'priority': 'core', 'showOptimize': True, 'type': 'function', 'view': 'normal'},
             {'idpname': 'p', 'priority': 'core', 'showOptimize': True, 'type': 'proposition', 'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Base': {'0 < Base': {'environmental': False,
                       'normal': False,
                       'reading': '0 < Base',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          '15.0 = Base * Base': {'environmental': False,
                                 'normal': False,
                                 'reading': '15.0 = Base * Base',
                                 'relevant': True,
                                 'status': 'CONSEQUENCE',
                                 'typ': 'Bool',
                                 'value': True},
          'Base': {'environmental': False,
                   'normal': True,
                   'reading': 'Base',
                   'relevant': True,
                   'status': 'CONSEQUENCE',
                   'typ': 'Real',
                   'value': '3.8729833462'}},
 'Height': {'Height': {'environmental': False,
                       'normal': True,
                       'reading': 'Height',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Real',
                       'value': '2.6666666666666665'},
            'Height = 8.0 / 3': {'environmental': False,
                                 'normal': False,
                                 'reading': 'Height = 8.0 / 3',
                                 'relevant': True,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Bool',
                                 'value': True}},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
