
-- original ---------------------------------


vocabulary {
	K
	O
	L
	Q
	R
	M
	N
	P
}
theory {
	//AND C
	{
		O() <- K() & L().
	}

	//OR E
	{
		R() <- O().
		R() <- Q().
		R() <- O() & Q().
	}

	//XOR A
	{
		N() <- K() & ~(L()).
		N() <- ~(K()) & L().
	}

	//XOR B
	{
		P() <- ~(N()) & M().
		P() <- N() & ~(M()).
	}

	//AND D
	{
		Q() <- N() & M().
	}

}


structure {
}

-- meta -------------------------------------
{'symbols': [{'environmental': False,
              'idpname': 'K',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'O',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'L',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Q',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'R',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'M',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'N',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'P',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'K': {'K': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'K',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'L': {'L': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'L',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'M': {'M': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'M',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'N': {'N': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'N',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'O': {'O': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'O',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'P': {'P': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'P',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'Q': {'Q': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'Q',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999},
 'R': {'R': {'environmental': False,
             'is_assignment': False,
             'normal': True,
             'reading': 'R',
             'relevant': False,
             'status': 'UNKNOWN',
             'typ': 'Bool'},
       '__rank': 9999}}
