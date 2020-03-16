
-- theory
Or(Not(p), Base*Base == 16)

Base > 0

p

-- atoms
Base
p
16.0 = (Base * Base)
0 < Base

-- case
Type:        
  
Definitions: 
  
Universals:  
  p
  0 < Base
Consequences:
  16.0 = (Base * Base)
  Base = 4
Simplified:  
  
Irrelevant:  
  


-- propagation
{' Global': {'env_dec': False},
 'Base': {'0 < Base': {'environmental': False,
                       'normal': False,
                       'reading': '0 < Base',
                       'relevant': True,
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          '16.0 = (Base * Base)': {'environmental': False,
                                   'normal': False,
                                   'reading': '16.0 = (Base * Base)',
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
                   'value': '4'}},
 'p': {'p': {'environmental': False,
             'normal': True,
             'reading': 'p',
             'relevant': True,
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
