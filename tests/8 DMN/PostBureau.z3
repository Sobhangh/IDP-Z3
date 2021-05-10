
-- original ---------------------------------


vocabulary {
	type Post_Bureau_Risk_Categoryt_t := { LOW, HIGH, VERY_LOW, MEDIUM }
	Credit_Score: ()→Int
	Application_Risk_Score: ()→Int
	Post_Bureau_Risk_Category: ()→Post_Bureau_Risk_Categoryt_t
	Existing_Customer:() → Bool
}
theory {
	//Post Bureau
	{
		Post_Bureau_Risk_Category() = HIGH <- ~(Existing_Customer()) & Application_Risk_Score() < 120 & Credit_Score() < 590.
		Post_Bureau_Risk_Category() = MEDIUM <- ~(Existing_Customer()) & Application_Risk_Score() < 120 & 590 =< Credit_Score() & Credit_Score() =< 610.
		Post_Bureau_Risk_Category() = LOW <- ~(Existing_Customer()) & Application_Risk_Score() < 120 & Credit_Score() > 610.
		Post_Bureau_Risk_Category() = HIGH <- ~(Existing_Customer()) & 120 =< Application_Risk_Score() & Application_Risk_Score() =< 130 & Credit_Score() < 600.
		Post_Bureau_Risk_Category() = MEDIUM <- ~(Existing_Customer()) & 120 =< Application_Risk_Score() & Application_Risk_Score() =< 130 & 600 =< Credit_Score() & Credit_Score() =< 625.
		Post_Bureau_Risk_Category() = LOW <- ~(Existing_Customer()) & 120 =< Application_Risk_Score() & Application_Risk_Score() =< 130 & Credit_Score() > 625.
		Post_Bureau_Risk_Category() = VERY_LOW <- ~(Existing_Customer()) & Application_Risk_Score() > 130.
		Post_Bureau_Risk_Category() = HIGH <- Existing_Customer() & Application_Risk_Score() =< 100 & Credit_Score() < 580.
		Post_Bureau_Risk_Category() = MEDIUM <- Existing_Customer() & Application_Risk_Score() =< 100 & 580 =< Credit_Score() & Credit_Score() =< 600.
		Post_Bureau_Risk_Category() = LOW <- Existing_Customer() & Application_Risk_Score() =< 100 & Credit_Score() > 600.
		Post_Bureau_Risk_Category() = HIGH <- Existing_Customer() & Application_Risk_Score() > 100 & Credit_Score() < 590.
		Post_Bureau_Risk_Category() = MEDIUM <- Existing_Customer() & Application_Risk_Score() > 100 & 590 =< Credit_Score() & Credit_Score() =< 615.
		Post_Bureau_Risk_Category() = LOW <- Existing_Customer() & Application_Risk_Score() > 100 & Credit_Score() > 615.
	}

}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Credit_Score',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Application_Risk_Score',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Post_Bureau_Risk_Category',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Existing_Customer',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Application_Risk_Score': {'Application_Risk_Score()': {'environmental': False,
                                                         'is_assignment': True,
                                                         'normal': True,
                                                         'reading': 'Application_Risk_Score',
                                                         'relevant': False,
                                                         'status': 'UNKNOWN',
                                                         'typ': 'Int',
                                                         'value': ''},
                            '__rank': 9999},
 'Credit_Score': {'Credit_Score()': {'environmental': False,
                                     'is_assignment': True,
                                     'normal': True,
                                     'reading': 'Credit_Score',
                                     'relevant': False,
                                     'status': 'UNKNOWN',
                                     'typ': 'Int',
                                     'value': ''},
                  '__rank': 9999},
 'Existing_Customer': {'Existing_Customer()': {'environmental': False,
                                               'is_assignment': False,
                                               'normal': True,
                                               'reading': 'Existing_Customer',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Bool'},
                       '__rank': 9999},
 'Post_Bureau_Risk_Category': {'Post_Bureau_Risk_Category()': {'environmental': False,
                                                               'is_assignment': True,
                                                               'normal': True,
                                                               'reading': 'Post_Bureau_Risk_Category',
                                                               'relevant': False,
                                                               'status': 'UNKNOWN',
                                                               'typ': 'Post_Bureau_Risk_Categoryt_t',
                                                               'value': '',
                                                               'values': ['LOW', 'HIGH', 'VERY_LOW', 'MEDIUM']},
                               'Post_Bureau_Risk_Category() = HIGH': {'environmental': False,
                                                                      'is_assignment': True,
                                                                      'normal': False,
                                                                      'reading': 'Post_Bureau_Risk_Category = HIGH',
                                                                      'relevant': False,
                                                                      'status': 'UNKNOWN',
                                                                      'typ': 'Bool'},
                               'Post_Bureau_Risk_Category() = LOW': {'environmental': False,
                                                                     'is_assignment': True,
                                                                     'normal': False,
                                                                     'reading': 'Post_Bureau_Risk_Category = LOW',
                                                                     'relevant': False,
                                                                     'status': 'UNKNOWN',
                                                                     'typ': 'Bool'},
                               'Post_Bureau_Risk_Category() = MEDIUM': {'environmental': False,
                                                                        'is_assignment': True,
                                                                        'normal': False,
                                                                        'reading': 'Post_Bureau_Risk_Category = MEDIUM',
                                                                        'relevant': False,
                                                                        'status': 'UNKNOWN',
                                                                        'typ': 'Bool'},
                               'Post_Bureau_Risk_Category() = VERY_LOW': {'environmental': False,
                                                                          'is_assignment': True,
                                                                          'normal': False,
                                                                          'reading': 'Post_Bureau_Risk_Category = '
                                                                                     'VERY_LOW',
                                                                          'relevant': False,
                                                                          'status': 'UNKNOWN',
                                                                          'typ': 'Bool'},
                               '__rank': 9999}}
