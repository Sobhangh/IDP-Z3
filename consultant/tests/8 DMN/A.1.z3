
-- original ---------------------------------


vocabulary {
	price: real
	age: real
	priority
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
{'symbols': [{'environmental': False,
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
         'age': {'environmental': False,
                 'normal': True,
                 'reading': 'age',
                 'relevant': False,
                 'status': 'UNKNOWN',
                 'typ': 'Real',
                 'value': ''}},
 'price': {'__rank': 9999,
           'price': {'environmental': False,
                     'normal': True,
                     'reading': 'price',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'Real',
                     'value': ''}},
 'priority': {'__rank': 9999,
              'priority': {'environmental': False,
                           'normal': True,
                           'reading': 'priority',
                           'relevant': False,
                           'status': 'UNKNOWN',
                           'typ': 'Bool'}}}
