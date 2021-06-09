
-- original ---------------------------------
// https://dmcommunity.org/challenge/challenge-feb-2015/

vocabulary {
	type Number_t := { 0..1000 }
	TotalMoney: ()→Number_t
	TotalCoins: ()→Number_t
	OneCent: ()→Number_t
	TwoCent: ()→Number_t
	FiveCent: ()→Number_t
	TenCent: ()→Number_t
	TwentyCent: ()→Number_t
	FiftyCent: ()→Number_t
	OneEuro: ()→Number_t
	TwoEuro: ()→Number_t
}
theory {
	//Total amount of Money
	{
		TotalMoney() = 567 <- true.
	}

	//Calculation of change
	TotalMoney() = sum{ : true: OneCent() * 01 }+sum{ : true: TwoCent() * 02 }+sum{ : true: FiveCent() * 05 }+sum{ : true: TenCent() * 10 }+sum{ : true: TwentyCent() * 20 }+sum{ : true: FiftyCent() * 50 }+sum{ : true: OneEuro() * 100 }+sum{ : true: TwoEuro() * 200 }.
	//Amount of coins
	TotalCoins() = sum{ : true: OneCent() }+sum{ : true: TwoCent() }+sum{ : true: FiveCent() }+sum{ : true: TenCent() }+sum{ : true: TwentyCent() }+sum{ : true: FiftyCent() }+sum{ : true: OneEuro() }+sum{ : true: TwoEuro() }.
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'optionalPropagation': False,
 'symbols': [{'environmental': False,
              'idpname': 'TotalMoney',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TotalCoins',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'OneCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TwoCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'FiveCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TenCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TwentyCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'FiftyCent',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'OneEuro',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'TwoEuro',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'active': '{}', 'env_dec': False},
 'FiftyCent': {'FiftyCent()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'FiftyCent',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int',
                               'value': '',
                               'values': []},
               '__rank': 9999},
 'FiveCent': {'FiveCent()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'FiveCent',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Int',
                             'value': '',
                             'values': []},
              '__rank': 9999},
 'OneCent': {'OneCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'OneCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': []},
             '__rank': 9999},
 'OneEuro': {'OneEuro()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'OneEuro',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': []},
             '__rank': 9999},
 'TenCent': {'TenCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TenCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': []},
             '__rank': 9999},
 'TotalCoins': {'TotalCoins()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TotalCoins',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int',
                                 'value': '',
                                 'values': []},
                'TotalCoins() = sum{ : true : OneCent()} + sum{ : true : TwoCent()} + sum{ : true : FiveCent()} + sum{ : true : TenCent()} + sum{ : true : TwentyCent()} + sum{ : true : FiftyCent()} + sum{ : true : OneEuro()} + sum{ : true : TwoEuro()}': {'environmental': False,
                                                                                                                                                                                                                                                               'is_assignment': False,
                                                                                                                                                                                                                                                               'normal': False,
                                                                                                                                                                                                                                                               'reading': 'TotalCoins '
                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'OneCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwoCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'FiveCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TenCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwentyCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'FiftyCent} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'OneEuro} '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum{ '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'true '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwoEuro}',
                                                                                                                                                                                                                                                               'relevant': True,
                                                                                                                                                                                                                                                               'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                               'typ': 'Bool',
                                                                                                                                                                                                                                                               'value': True},
                '__rank': 9999},
 'TotalMoney': {'TotalMoney()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TotalMoney',
                                 'relevant': True,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Int',
                                 'value': '567',
                                 'values': ['567']},
                'TotalMoney() = 567': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'TotalMoney = 567',
                                       'relevant': True,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
                'TotalMoney() = sum{ : true : OneCent() ⨯ 01} + sum{ : true : TwoCent() ⨯ 02} + sum{ : true : FiveCent() ⨯ 05} + sum{ : true : TenCent() ⨯ 10} + sum{ : true : TwentyCent() ⨯ 20} + sum{ : true : FiftyCent() ⨯ 50} + sum{ : true : OneEuro() ⨯ 100} + sum{ : true : TwoEuro() ⨯ 200}': {'environmental': False,
                                                                                                                                                                                                                                                                                                         'is_assignment': False,
                                                                                                                                                                                                                                                                                                         'normal': False,
                                                                                                                                                                                                                                                                                                         'reading': 'TotalMoney '
                                                                                                                                                                                                                                                                                                                    '= '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'OneCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '01} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwoCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '02} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'FiveCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '05} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TenCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '10} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwentyCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '20} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'FiftyCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '50} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'OneEuro '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '100} '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum{ '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'true '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwoEuro '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '200}',
                                                                                                                                                                                                                                                                                                         'relevant': True,
                                                                                                                                                                                                                                                                                                         'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                                                                         'typ': 'Bool',
                                                                                                                                                                                                                                                                                                         'value': True},
                '__rank': 9999},
 'TwentyCent': {'TwentyCent()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TwentyCent',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int',
                                 'value': '',
                                 'values': []},
                '__rank': 9999},
 'TwoCent': {'TwoCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TwoCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': []},
             '__rank': 9999},
 'TwoEuro': {'TwoEuro()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TwoEuro',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int',
                           'value': '',
                           'values': []},
             '__rank': 9999}}
