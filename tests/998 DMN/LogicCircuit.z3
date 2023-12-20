
-- original ---------------------------------


vocabulary {
	K:() → Bool
	O:() → Bool
	L:() → Bool
	Q:() → Bool
	R:() → Bool
	M:() → Bool
	N:() → Bool
	P:() → Bool
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
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
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
 'K': {'K()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'K',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'L': {'L()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'L',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'M': {'M()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'M',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'N': {'N()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'N',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'O': {'O()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'O',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'P': {'P()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'P',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'Q': {'Q()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'Q',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}},
 'R': {'R()': {'environmental': False,
               'is_assignment': False,
               'normal': True,
               'reading': 'R',
               'relevant': True,
               'status': 'UNKNOWN',
               'typ': 'Bool'}}}
