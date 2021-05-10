
-- original ---------------------------------


vocabulary {
	Output_AND:() → Bool
	Output_OR:() → Bool
	A:() → Bool
	B:() → Bool
}
theory {
	//AND
	{
		Output_AND() <- A() & B().
	}

	//OR
	{
		Output_OR() <- A().
		Output_OR() <- B().
	}

}


structure {
}

-- meta -------------------------------------
{'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'Output_AND',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Output_OR',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'A',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'B',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'A': {'A()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'A',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'},
       '__rank': 9999},
 'B': {'B()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'B',
               'relevant': False,
               'status': 'UNKNOWN',
               'typ': 'Bool'},
       '__rank': 9999},
 'Output_AND': {'Output_AND()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'Output_AND',
                                 'relevant': False,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'},
                '__rank': 9999},
 'Output_OR': {'Output_OR()': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'Output_OR',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
               '__rank': 9999}}
