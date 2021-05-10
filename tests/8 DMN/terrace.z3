
-- original ---------------------------------


vocabulary {
	Temperature: ()→Int
	Rain_Probability: ()→Int
	Prepare_Terrace:() → Bool
}
theory {
	//Prepare Terrace
	{
		Prepare_Terrace() <- Temperature() >= 20 & Rain_Probability() < 50.
	}

}


structure {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Temperature',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Rain_Probability',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Prepare_Terrace',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Prepare_Terrace': {'Prepare_Terrace()': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': True,
                                           'reading': 'Prepare_Terrace',
                                           'relevant': False,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'},
                     '__rank': 9999},
 'Rain_Probability': {'Rain_Probability()': {'environmental': False,
                                             'is_assignment': True,
                                             'normal': True,
                                             'reading': 'Rain_Probability',
                                             'relevant': False,
                                             'status': 'UNKNOWN',
                                             'typ': 'Int',
                                             'value': ''},
                      '__rank': 9999},
 'Temperature': {'Temperature()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Temperature',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Int',
                                   'value': ''},
                 '__rank': 9999}}
