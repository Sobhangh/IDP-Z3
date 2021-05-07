
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
{'optionalPropagation': False,
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
 'amount': {'__rank': 9999,
            'amount()': {'environmental': False,
                         'is_assignment': True,
                         'normal': True,
                         'reading': 'amount',
                         'relevant': False,
                         'status': 'UNKNOWN',
                         'typ': 'Int',
                         'value': ''}},
 'discount': {'__rank': 9999,
              'discount()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'discount',
                             'relevant': False,
                             'status': 'UNKNOWN',
                             'typ': 'Int',
                             'value': ''}}}
