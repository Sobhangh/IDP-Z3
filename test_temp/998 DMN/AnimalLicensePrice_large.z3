
-- original ---------------------------------


vocabulary {
	type Animal_Typet_t := { Dog }
	type Interaction_Reasont_t := { Register }
	Animal_Type: ()→Animal_Typet_t
	Total: ()→Int
	Interaction_Reason: ()→Interaction_Reasont_t
	Age: ()→Int
	Sterilized:() → Bool
	Half_Price_Reg:() → Bool
	Free_Renewal:() → Bool
	ViciousDog:() → Bool
	Sterilization_Applicable:() → Bool
	Vet_Certificate:() → Bool
	Microchipped:() → Bool
	Fee_Discount_for_Sterilization:() → Bool
}
theory {
	//DogLicensePrice
	{
		Total() = 40 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & ~(Vet_Certificate()) & ~(Fee_Discount_for_Sterilization()) & ~(ViciousDog()) & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 20 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & ~(Vet_Certificate()) & ~(Fee_Discount_for_Sterilization()) & ~(ViciousDog()) & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 143 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & ~(Vet_Certificate()) & ~(Fee_Discount_for_Sterilization()) & ViciousDog() & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 134 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & ~(Vet_Certificate()) & ~(Fee_Discount_for_Sterilization()) & ViciousDog() & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 23 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 11.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 126.0 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ViciousDog() & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 114.50 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ViciousDog() & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 23 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 11.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 126 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ViciousDog() & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 114.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & ~(Microchipped()) & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ViciousDog() & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 17 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 8.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 120 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ViciousDog() & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 111.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & ~(Sterilized()) & Sterilization_Applicable() & Vet_Certificate() & Fee_Discount_for_Sterilization() & ViciousDog() & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 17 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 8.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ~(ViciousDog()) & Half_Price_Reg() & ~(Free_Renewal()).
		Total() = 120 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ViciousDog() & ~(Half_Price_Reg()) & ~(Free_Renewal()).
		Total() = 111.5 <- Animal_Type() = Dog & Interaction_Reason() = Register & Age() >= 6 & Microchipped() & Sterilized() & Sterilization_Applicable() & ~(Vet_Certificate()) & Fee_Discount_for_Sterilization() & ViciousDog() & Half_Price_Reg() & ~(Free_Renewal()).
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
              'idpname': 'Animal_Type',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Total',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Interaction_Reason',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Age',
              'priority': 'core',
              'showOptimize': True,
              'type': 'function',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Sterilized',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Half_Price_Reg',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Free_Renewal',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'ViciousDog',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Sterilization_Applicable',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Vet_Certificate',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Microchipped',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'},
             {'environmental': False,
              'idpname': 'Fee_Discount_for_Sterilization',
              'priority': 'core',
              'showOptimize': True,
              'type': 'proposition',
              'view': 'normal'}],
 'title': 'Interactive Consultant'}

-- propagation ------------------------------
{' Global': {'env_dec': False},
 'Age': {'Age()': {'environmental': False,
                   'is_assignment': True,
                   'normal': True,
                   'reading': 'Age',
                   'relevant': True,
                   'status': 'UNKNOWN',
                   'typ': 'Int'}},
 'Animal_Type': {'Animal_Type()': {'environmental': False,
                                   'is_assignment': True,
                                   'normal': True,
                                   'reading': 'Animal_Type',
                                   'relevant': False,
                                   'status': 'UNIVERSAL',
                                   'typ': 'Animal_Typet_t',
                                   'value': 'Dog',
                                   'values': ['Dog']}},
 'Fee_Discount_for_Sterilization': {'Fee_Discount_for_Sterilization()': {'environmental': False,
                                                                         'is_assignment': False,
                                                                         'normal': True,
                                                                         'reading': 'Fee_Discount_for_Sterilization',
                                                                         'relevant': True,
                                                                         'status': 'UNKNOWN',
                                                                         'typ': 'Bool'}},
 'Free_Renewal': {'Free_Renewal()': {'environmental': False,
                                     'is_assignment': False,
                                     'normal': True,
                                     'reading': 'Free_Renewal',
                                     'relevant': False,
                                     'status': 'UNIVERSAL',
                                     'typ': 'Bool',
                                     'value': False}},
 'Half_Price_Reg': {'Half_Price_Reg()': {'environmental': False,
                                         'is_assignment': False,
                                         'normal': True,
                                         'reading': 'Half_Price_Reg',
                                         'relevant': True,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'}},
 'Interaction_Reason': {'Interaction_Reason()': {'environmental': False,
                                                 'is_assignment': True,
                                                 'normal': True,
                                                 'reading': 'Interaction_Reason',
                                                 'relevant': False,
                                                 'status': 'UNIVERSAL',
                                                 'typ': 'Interaction_Reasont_t',
                                                 'value': 'Register',
                                                 'values': ['Register']}},
 'Microchipped': {'Microchipped()': {'environmental': False,
                                     'is_assignment': False,
                                     'normal': True,
                                     'reading': 'Microchipped',
                                     'relevant': True,
                                     'status': 'UNKNOWN',
                                     'typ': 'Bool'}},
 'Sterilization_Applicable': {'Sterilization_Applicable()': {'environmental': False,
                                                             'is_assignment': False,
                                                             'normal': True,
                                                             'reading': 'Sterilization_Applicable',
                                                             'relevant': False,
                                                             'status': 'UNIVERSAL',
                                                             'typ': 'Bool',
                                                             'value': True}},
 'Sterilized': {'Sterilized()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'Sterilized',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}},
 'Total': {'Total()': {'environmental': False,
                       'is_assignment': True,
                       'normal': True,
                       'reading': 'Total',
                       'relevant': True,
                       'status': 'UNKNOWN',
                       'typ': 'Int'}},
 'Vet_Certificate': {'Vet_Certificate()': {'environmental': False,
                                           'is_assignment': False,
                                           'normal': True,
                                           'reading': 'Vet_Certificate',
                                           'relevant': True,
                                           'status': 'UNKNOWN',
                                           'typ': 'Bool'}},
 'ViciousDog': {'ViciousDog()': {'environmental': False,
                                 'is_assignment': False,
                                 'normal': True,
                                 'reading': 'ViciousDog',
                                 'relevant': True,
                                 'status': 'UNKNOWN',
                                 'typ': 'Bool'}}}
