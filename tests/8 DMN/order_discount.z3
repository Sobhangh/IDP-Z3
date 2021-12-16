
-- original ---------------------------------


vocabulary {
	amount: ()→Int
	discount: ()→Int
}
theory {
	//Order Discount
	{
		discount() = 0 <- amount() < 500.
		discount() = 2 <- 500 =< amount() & amount() =< 999.
		discount() = 3 <- 1000 =< amount() & amount() =< 1999.
		discount() = 5 <- 2000 =< amount() & amount() =< 4999.
		discount() = 8 <- amount() >= 5000.
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
              'idpname': 'amount',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'discount',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'amount': {'amount()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'amount',
                         'relevant': True,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''}},
 'discount': {'discount()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'discount',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Int',
                             'value': ''}}}
