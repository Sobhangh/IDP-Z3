
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
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': '2.104 ≤ Depth ≤ 2.476',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '2.768 ≤ Depth ≤ 3.391': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': '2.768 ≤ Depth ≤ 3.391',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '4.294 ≤ Depth ≤ 5.206': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': '4.294 ≤ Depth ≤ 5.206',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '5.474 ≤ Depth ≤ 6.686': {'cf': False,
                                     'ct': False,
                                     'environmental': True,
                                     'irrelevant': False,
                                     'normal': False,
                                     'reading': '5.474 ≤ Depth ≤ 6.686',
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'},
           '8.312 ≤ Depth ≤ 10.748': {'cf': False,
                                      'ct': False,
                                      'environmental': True,
                                      'irrelevant': False,
                                      'normal': False,
                                      'reading': '8.312 ≤ Depth ≤ 10.748',
                                      'status': 'UNKNOWN',
                                      'typ': 'Bool'},
           'Depth': {'environmental': True, 'normal': True, 'reading': 'Depth', 'typ': 'Real', 'value': ''}},
 'cSID': {'cSID': {'environmental': False,
                   'normal': True,
                   'reading': 'cSID',
                   'typ': 'csid',
                   'value': '',
                   'values': ['b', 'c', 'd', 'e', 'f']},
          'cSID = b': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': 'cSID = b',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = c': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': 'cSID = c',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = d': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': 'cSID = d',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = e': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': 'cSID = e',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'},
          'cSID = f': {'cf': False,
                       'ct': False,
                       'environmental': False,
                       'irrelevant': False,
                       'normal': False,
                       'reading': 'cSID = f',
                       'status': 'UNKNOWN',
                       'typ': 'Bool'}}}
