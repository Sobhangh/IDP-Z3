
-- original ---------------------------------
// https://dmcommunity.org/challenge/challenge-july-2018/

vocabulary {
	type Bus_t := { Big, Small }
	type Size_t := { 30..40 }
	type Amount_t := { 0..10 }
	Price:(Bus_t)→ Int
	Size:(Bus_t)→ Size_t
	Amount:(Bus_t)→ Amount_t
	Kids:(Bus_t)→ Int
	TotalPrice: ()→Int
	Kids_amount: ()→Int
}
theory {
	//Amount of Kids
	{
		Kids_amount() = 300 <- true.
	}

	//Calculate Total
	true => TotalPrice() = Amount(Big) * Price(Big) + Amount(Small) * Price(Small).

	//Calculate amount of bus
	!Bus in Bus_t: true => Amount(Bus) = ((Kids(Bus) - 01) - (Kids(Bus) - 01)%Size(Bus))/Size(Bus) + 01.

	//Every kid needs a bus
	Kids_amount() = sum(lambda Bus in Bus_t : Kids(Bus) ).
}


structure {
	Price := { Big → 500, Small → 400 } else 400.
	Size := { Big → 40, Small → 30 } else 30.
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
 'symbols': [{'environmental': False,
              'idpname': 'Price',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Size',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Amount',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Kids',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TotalPrice',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Kids_amount',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Amount': {'Amount(Big)': {'environmental': False,
                            'is_assignment': True,
                            'normal': True,
                            'reading': 'Amount(Big)',
                            'relevant': True,
                            'status': 'UNKNOWN',
                            'typ': 'Int',
                            'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
            'Amount(Small)': {'environmental': False,
                              'is_assignment': True,
                              'normal': True,
                              'reading': 'Amount(Small)',
                              'relevant': True,
                              'status': 'UNKNOWN',
                              'typ': 'Int',
                              'values': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']},
            '∀ Bus ∈ Bus_t: true ⇒ Amount(Bus) = ((Kids(Bus) - 01) - (Kids(Bus) - 01) % Size(Bus)) / Size(Bus) + 01': {'environmental': False,
                                                                                                                       'is_assignment': False,
                                                                                                                       'normal': False,
                                                                                                                       'reading': '∀ '
                                                                                                                                  'Bus '
                                                                                                                                  '∈ '
                                                                                                                                  'Bus_t: '
                                                                                                                                  'true '
                                                                                                                                  '⇒ '
                                                                                                                                  'Amount(Bus) '
                                                                                                                                  '= '
                                                                                                                                  '((Kids(Bus) '
                                                                                                                                  '- '
                                                                                                                                  '01) '
                                                                                                                                  '- '
                                                                                                                                  '(Kids(Bus) '
                                                                                                                                  '- '
                                                                                                                                  '01) '
                                                                                                                                  '% '
                                                                                                                                  'Size(Bus)) '
                                                                                                                                  '/ '
                                                                                                                                  'Size(Bus) '
                                                                                                                                  '+ '
                                                                                                                                  '01',
                                                                                                                       'relevant': False,
                                                                                                                       'status': 'UNIVERSAL',
                                                                                                                       'typ': 'Bool',
                                                                                                                       'value': True}},
 'Kids': {'Kids(Big)': {'environmental': False,
                        'is_assignment': True,
                        'normal': True,
                        'reading': 'Kids(Big)',
                        'relevant': True,
                        'status': 'UNKNOWN',
                        'typ': 'Int'},
          'Kids(Small)': {'environmental': False,
                          'is_assignment': True,
                          'normal': True,
                          'reading': 'Kids(Small)',
                          'relevant': True,
                          'status': 'UNKNOWN',
                          'typ': 'Int'}},
 'Kids_amount': {'Kids_amount()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Kids_amount',
                                   'relevant': True,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Int',
                                   'value': '300'},
                 'Kids_amount() = 300': {'environmental': False,
                                         'is_assignment': True,
                                         'normal': False,
                                         'reading': 'Kids_amount = 300',
                                         'relevant': False,
                                         'status': 'UNIVERSAL',
                                         'typ': 'Bool',
                                         'value': True},
                 'Kids_amount() = sum(lambda Bus ∈ Bus_t : Kids(Bus))': {'environmental': False,
                                                                         'is_assignment': False,
                                                                         'normal': False,
                                                                         'reading': 'Kids_amount = sum(lambda Bus ∈ '
                                                                                    'Bus_t : Kids(Bus))',
                                                                         'relevant': True,
                                                                         'status': 'UNIVERSAL',
                                                                         'typ': 'Bool',
                                                                         'value': True}},
 'Price': {},
 'Size': {},
 'TotalPrice': {'TotalPrice()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TotalPrice',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int'},
                'TotalPrice() = Amount(Big) ⨯ Price(Big) + Amount(Small) ⨯ Price(Small)': {'environmental': False,
                                                                                           'is_assignment': False,
                                                                                           'normal': False,
                                                                                           'reading': 'TotalPrice = '
                                                                                                      'Amount(Big) ⨯ '
                                                                                                      'Price(Big) + '
                                                                                                      'Amount(Small) ⨯ '
                                                                                                      'Price(Small)',
                                                                                           'relevant': True,
                                                                                           'status': 'UNIVERSAL',
                                                                                           'typ': 'Bool',
                                                                                           'value': True}}}
