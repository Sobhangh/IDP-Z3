
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
{'Base': {'0 < Base': {'cf': False,
                       'ct': True,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': '0 < Base',
                       'status': 'UNIVERSAL',
                       'typ': 'Bool',
                       'value': True},
          '16.0 = (Base * Base)': {'cf': False,
                                   'ct': True,
                                   'environmental': False,
                                   'irrelevant': False,
                                   'normal': False,
                                   'reading': '16.0 = (Base * Base)',
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': True},
          'Base': {'environmental': False,
                   'normal': True,
                   'reading': 'Base',
                   'status': 'CONSEQUENCE',
                   'typ': 'Real',
                   'value': '4'}},
 'p': {'p': {'cf': False,
             'ct': True,
             'environmental': False,
             'irrelevant': False,
             'normal': True,
             'reading': 'p',
             'status': 'UNIVERSAL',
             'typ': 'Bool',
             'value': True}}}
