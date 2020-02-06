
-- theory
(cSID == b) == And(Depth >= 263/125, Depth <= 619/250)

(cSID == c) == And(Depth >= 346/125, Depth <= 3391/1000)

(cSID == d) == And(Depth >= 2147/500, Depth <= 2603/500)

(cSID == e) == And(Depth >= 2737/500, Depth <= 3343/500)

(cSID == f) == And(Depth >= 1039/125, Depth <= 2687/250)

-- atoms
Depth
cSID
cSID = b
2.104 ≤ Depth ≤ 2.476
cSID = c
2.768 ≤ Depth ≤ 3.391
cSID = d
4.294 ≤ Depth ≤ 5.206
cSID = e
5.474 ≤ Depth ≤ 6.686
cSID = f
8.312 ≤ Depth ≤ 10.748

-- case
Type:        
  
Definitions: 
  
Universals:  
  
Consequences:
  
Simplified:  
  (cSID = b) ⇔ (2.104 ≤ Depth ≤ 2.476)
  (cSID = c) ⇔ (2.768 ≤ Depth ≤ 3.391)
  (cSID = d) ⇔ (4.294 ≤ Depth ≤ 5.206)
  (cSID = e) ⇔ (5.474 ≤ Depth ≤ 6.686)
  (cSID = f) ⇔ (8.312 ≤ Depth ≤ 10.748)
Irrelevant:  
  


-- propagation
{'Depth': {'2.104 ≤ Depth ≤ 2.476': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'normal': False,
                                     'reading': '2.104 ≤ Depth ≤ 2.476',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '2.768 ≤ Depth ≤ 3.391': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'normal': False,
                                     'reading': '2.768 ≤ Depth ≤ 3.391',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '4.294 ≤ Depth ≤ 5.206': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'normal': False,
                                     'reading': '4.294 ≤ Depth ≤ 5.206',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '5.474 ≤ Depth ≤ 6.686': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'normal': False,
                                     'reading': '5.474 ≤ Depth ≤ 6.686',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '8.312 ≤ Depth ≤ 10.748': {'cf': False,
                                      'ct': False,
                                      'environmental': True,
                                      'normal': False,
                                      'reading': '8.312 ≤ Depth ≤ 10.748',
                                      'relevant': True,
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Depth': {'environmental': True,
                     'normal': True,
                     'reading': 'Depth',
                     'relevant': True,
                     'status': 'UNKNOWN',
                     'typ': 'Real',
                     'value': ''}},
 'cSID': {'cSID': {'environmental': False,
                   'normal': True,
                   'reading': 'cSID',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'csid',
                   'value': '',
                   'values': ['b', 'c', 'd', 'e', 'f']},
          'cSID = b': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'normal': False,
                       'reading': 'cSID = b',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = c': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'normal': False,
                       'reading': 'cSID = c',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = d': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'normal': False,
                       'reading': 'cSID = d',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = e': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'normal': False,
                       'reading': 'cSID = e',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = f': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'normal': False,
                       'reading': 'cSID = f',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}}}
