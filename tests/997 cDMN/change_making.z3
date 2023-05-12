
-- original ---------------------------------
// https://dmcommunity.org/challenge/challenge-feb-2015/

vocabulary {
	TotalMoney: ()→Int
	TotalCoins: ()→Int
	OneCent: ()→Int
	TwoCent: ()→Int
	FiveCent: ()→Int
	TenCent: ()→Int
	TwentyCent: ()→Int
	FiftyCent: ()→Int
	OneEuro: ()→Int
	TwoEuro: ()→Int
}
theory {
	//Total amount of Money
	{
		TotalMoney() = 567 <- true.
	}

	//Calculation of change
	TotalMoney() = sum(lambda : OneCent() * 01 )+sum(lambda : TwoCent() * 02 )+sum(lambda : FiveCent() * 05 )+sum(lambda : TenCent() * 10 )+sum(lambda : TwentyCent() * 20 )+sum(lambda : FiftyCent() * 50 )+sum(lambda : OneEuro() * 100 )+sum(lambda : TwoEuro() * 200 ).
	//Amount of coins
	TotalCoins() = sum(lambda : OneCent() )+sum(lambda : TwoCent() )+sum(lambda : FiveCent() )+sum(lambda : TenCent() )+sum(lambda : TwentyCent() )+sum(lambda : FiftyCent() )+sum(lambda : OneEuro() )+sum(lambda : TwoEuro() ).
}


structure {
}

-- meta -------------------------------------
{'manualPropagation': False,
 'manualRelevance': False,
 'optionalPropagation': False,
 'optionalRelevance': False,
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
{' Global': {'env_dec': False},
 'FiftyCent': {'FiftyCent()': {'environmental': False,
                               'is_assignment': True,
                               'normal': True,
                               'reading': 'FiftyCent',
                               'relevant': True,
                               'status': 'UNKNOWN',
                               'typ': 'Int'}},
 'FiveCent': {'FiveCent()': {'environmental': False,
                             'is_assignment': True,
                             'normal': True,
                             'reading': 'FiveCent',
                             'relevant': True,
                             'status': 'UNKNOWN',
                             'typ': 'Int'}},
 'OneCent': {'OneCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'OneCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int'}},
 'OneEuro': {'OneEuro()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'OneEuro',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int'}},
 'TenCent': {'TenCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TenCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int'}},
 'TotalCoins': {'TotalCoins()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TotalCoins',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int'},
                'TotalCoins() = sum(lambda  : OneCent()) + sum(lambda  : TwoCent()) + sum(lambda  : FiveCent()) + sum(lambda  : TenCent()) + sum(lambda  : TwentyCent()) + sum(lambda  : FiftyCent()) + sum(lambda  : OneEuro()) + sum(lambda  : TwoEuro())': {'environmental': False,
                                                                                                                                                                                                                                                               'is_assignment': False,
                                                                                                                                                                                                                                                               'normal': False,
                                                                                                                                                                                                                                                               'reading': 'TotalCoins '
                                                                                                                                                                                                                                                                          '= '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'OneCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwoCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'FiveCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TenCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwentyCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'FiftyCent) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'OneEuro) '
                                                                                                                                                                                                                                                                          '+ '
                                                                                                                                                                                                                                                                          'sum(lambda  '
                                                                                                                                                                                                                                                                          ': '
                                                                                                                                                                                                                                                                          'TwoEuro)',
                                                                                                                                                                                                                                                               'relevant': True,
                                                                                                                                                                                                                                                               'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                               'typ': 'Bool',
                                                                                                                                                                                                                                                               'value': True}},
 'TotalMoney': {'TotalMoney()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TotalMoney',
                                 'relevant': True,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Int',
                                 'value': '567'},
                'TotalMoney() = 567': {'environmental': False,
                                       'is_assignment': True,
                                       'normal': False,
                                       'reading': 'TotalMoney = 567',
                                       'relevant': False,
                                       'status': 'UNIVERSAL',
                                       'typ': 'Bool',
                                       'value': True},
                'TotalMoney() = sum(lambda  : OneCent() ⨯ 01) + sum(lambda  : TwoCent() ⨯ 02) + sum(lambda  : FiveCent() ⨯ 05) + sum(lambda  : TenCent() ⨯ 10) + sum(lambda  : TwentyCent() ⨯ 20) + sum(lambda  : FiftyCent() ⨯ 50) + sum(lambda  : OneEuro() ⨯ 100) + sum(lambda  : TwoEuro() ⨯ 200)': {'environmental': False,
                                                                                                                                                                                                                                                                                                         'is_assignment': False,
                                                                                                                                                                                                                                                                                                         'normal': False,
                                                                                                                                                                                                                                                                                                         'reading': 'TotalMoney '
                                                                                                                                                                                                                                                                                                                    '= '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'OneCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '01) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwoCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '02) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'FiveCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '05) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TenCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '10) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwentyCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '20) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'FiftyCent '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '50) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'OneEuro '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '100) '
                                                                                                                                                                                                                                                                                                                    '+ '
                                                                                                                                                                                                                                                                                                                    'sum(lambda  '
                                                                                                                                                                                                                                                                                                                    ': '
                                                                                                                                                                                                                                                                                                                    'TwoEuro '
                                                                                                                                                                                                                                                                                                                    '⨯ '
                                                                                                                                                                                                                                                                                                                    '200)',
                                                                                                                                                                                                                                                                                                         'relevant': True,
                                                                                                                                                                                                                                                                                                         'status': 'UNIVERSAL',
                                                                                                                                                                                                                                                                                                         'typ': 'Bool',
                                                                                                                                                                                                                                                                                                         'value': True}},
 'TwentyCent': {'TwentyCent()': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'TwentyCent',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Int'}},
 'TwoCent': {'TwoCent()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TwoCent',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int'}},
 'TwoEuro': {'TwoEuro()': {'environmental': False,
                           'is_assignment': True,
                           'normal': True,
                           'reading': 'TwoEuro',
                           'relevant': True,
                           'status': 'UNKNOWN',
                           'typ': 'Int'}}}
