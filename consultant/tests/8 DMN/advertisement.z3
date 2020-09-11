
-- original ---------------------------------


vocabulary {
	type Advertised_Objectst_t constructed from { Toys, Cars, Videogames } 
	Advertised_Objects: Advertised_Objectst_t
	Age: int
}
theory {
	//Advertisement Decision
	{
		Advertised_Objects() = Cars <- Age() > 18.
		Advertised_Objects() = Videogames <- Age() > 12 & ~((Age() > 18)).
		Advertised_Objects() = Toys <- true & ~((Age() > 18)|(Age() > 12)).
	}

}


structure {
}

-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'Advertised_Objects',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Age',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Advertised_Objects': {'Advertised_Objects': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': True,
                                               'reading': 'Advertised_Objects',
                                               'relevant': False,
                                               'status': 'UNKNOWN',
                                               'typ': 'Advertised_Objectst_t',
                                               'value': '',
                                               'values': ['Toys', 'Cars', 'Videogames']},
                        'Advertised_Objects = Cars': {'environmental': False,
                                                      'is_assignment': True,
                                                      'normal': False,
                                                      'reading': 'Advertised_Objects = Cars',
                                                      'relevant': False,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Advertised_Objects = Toys': {'environmental': False,
                                                      'is_assignment': True,
                                                      'normal': False,
                                                      'reading': 'Advertised_Objects = Toys',
                                                      'relevant': False,
                                                      'status': 'UNKNOWN',
                                                      'typ': 'Bool'},
                        'Advertised_Objects = Videogames': {'environmental': False,
                                                            'is_assignment': True,
                                                            'normal': False,
                                                            'reading': 'Advertised_Objects = Videogames',
                                                            'relevant': False,
                                                            'status': 'UNKNOWN',
                                                            'typ': 'Bool'},
                        '__rank': 9999},
 'Age': {'Age': {'environmental': False,
                 'is_assignment': True,
                 'normal': True,
                 'reading': 'Age',
                 'relevant': False,
                 'status': 'UNKNOWN',
                 'typ': 'Int',
                 'value': ''},
         '__rank': 9999}}
