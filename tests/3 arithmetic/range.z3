
-- original ---------------------------------
vocabulary  {
    type date = {2015; 2016}
    Start_Dt_Dwelling_For_Social_Rent : date
}
theory {
}

-- vocabulary -------------------------------

-- theory -----------------------------------
Or(Start_Dt_Dwelling_For_Social_Rent == 2015,
   Start_Dt_Dwelling_For_Social_Rent == 2016)

-- subtences ------------------------------------
Start_Dt_Dwelling_For_Social_Rent = 2015
Start_Dt_Dwelling_For_Social_Rent = 2016

-- GUILines ------------------------------------
Start_Dt_Dwelling_For_Social_Rent
Start_Dt_Dwelling_For_Social_Rent = 2015
Start_Dt_Dwelling_For_Social_Rent = 2016

-- case -------------------------------------
Type:        
  
Definitions: 
  
Universals:  
  
Consequences:
  
Simplified:  
  
Irrelevant:  
  ? Start_Dt_Dwelling_For_Social_Rent = 2015
  ? Start_Dt_Dwelling_For_Social_Rent = 2016
  ? Start_Dt_Dwelling_For_Social_Rent
Co-constraints:
  


-- meta -------------------------------------
{'symbols': [], 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Start_Dt_Dwelling_For_Social_Rent': {'Start_Dt_Dwelling_For_Social_Rent': {'environmental': False,
                                                                             'normal': True,
                                                                             'reading': 'Start_Dt_Dwelling_For_Social_Rent',
                                                                             'relevant': False,
                                                                             'status': 'UNKNOWN',
                                                                             'typ': 'Int',
                                                                             'value': '',
                                                                             'values': ['2015', '2016']},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2015': {'environmental': False,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2015',
                                                                                    'relevant': False,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'},
                                       'Start_Dt_Dwelling_For_Social_Rent = 2016': {'environmental': False,
                                                                                    'normal': False,
                                                                                    'reading': 'Start_Dt_Dwelling_For_Social_Rent '
                                                                                               '= 2016',
                                                                                    'relevant': False,
                                                                                    'status': 'UNKNOWN',
                                                                                    'typ': 'Bool'}}}
