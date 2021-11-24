
-- original ---------------------------------


vocabulary {
	type Advertised_Objectst_t := { Toys, Cars, Videogames }
	Advertised_Objects: ()→Advertised_Objectst_t
	Age: ()→Int
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
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
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
 'Advertised_Objects': {'Advertised_Objects()': {'environmental': False,
                                                 'is_assignment': True,
                                                 'normal': True,
                                                 'reading': 'Advertised_Objects',
                                                 'relevant': True,
                                                 'status': 'UNKNOWN',
                                                 'typ': 'Advertised_Objectst_t',
                                                 'value': '',
                                                 'values': ['Toys', 'Cars', 'Videogames']}},
 'Age': {'Age()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Age',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int',
                   'value': ''}}}
