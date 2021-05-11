
-- original ---------------------------------


vocabulary {
	price: ()→Real
	age: ()→Real
	priority:() → Bool
}
theory {
	//Calculate Price Decision
	{
		price() = 0 <- age() < 2 & ~(priority()).
		price() = 10 <- age() < 2 & priority().
		price() = 20 <- 3 =< age() & age() =< 16 & ~(priority()).
		price() = 30 <- 3 =< age() & age() =< 16 & priority().
		price() = 40 <- age() >= 16 & ~(priority()).
		price() = 50 <- age() >= 16 & priority().
	}

}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'price',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'age',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'priority',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'age': {'__rank': 9999,
         'age()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'age',
                   'relevant': False,
                   'status': 'UNKNOWN',
                   'typ': 'Real',
                   'value': ''}},
 'price': {'__rank': 9999,
           'price()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'price',
                       'relevant': False,
                       'status': 'UNKNOWN',
                       'typ': 'Real',
                       'value': ''}},
 'priority': {'__rank': 9999,
              'priority()': {'environmental': False,
                             'is_assignment': False,
                             'normal': True,
                             'reading': 'priority',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Bool'}}}
