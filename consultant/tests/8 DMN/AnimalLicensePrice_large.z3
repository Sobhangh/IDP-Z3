
-- original ---------------------------------


vocabulary {
	type Animal_Typet_t constructed from { Dog } 
	type Interaction_Reasont_t constructed from { Register } 
	Animal_Type: Animal_Typet_t
	Total: int
	Interaction_Reason: Interaction_Reasont_t
	Age: int
	Sterilized
	Half_Price_Reg
	Free_Renewal
	ViciousDog
	Sterilization_Applicable
	Vet_Certificate
	Microchipped
	Fee_Discount_for_Sterilization
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
{'optionalPropagation': False,
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
 'Age': {'Age': {'environmental': False,
                 'is_assignment': True,
                 'normal': True,
                 'reading': 'Age',
                 'relevant': False,
                 'status': 'UNKNOWN',
                 'typ': 'Int',
                 'value': ''},
         '__rank': 9999},
 'Animal_Type': {'Animal_Type': {'environmental': False,
                                 'is_assignment': True,
                                 'normal': True,
                                 'reading': 'Animal_Type',
                                 'relevant': False,
                                 'status': 'UNIVERSAL',
                                 'typ': 'Animal_Typet_t',
                                 'value': 'Dog',
                                 'values': ['Dog']},
                 '__rank': 9999},
 'Fee_Discount_for_Sterilization': {'Fee_Discount_for_Sterilization': {'environmental': False,
                                                                       'is_assignment': False,
                                                                       'normal': True,
                                                                       'reading': 'Fee_Discount_for_Sterilization',
                                                                       'relevant': False,
                                                                       'status': 'UNKNOWN',
                                                                       'typ': 'Bool'},
                                    '__rank': 9999},
 'Free_Renewal': {'Free_Renewal': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': True,
                                   'reading': 'Free_Renewal',
                                   'relevant': False,
                                   'status': 'CONSEQUENCE',
                                   'typ': 'Bool',
                                   'value': False},
                  '__rank': 9999},
 'Half_Price_Reg': {'Half_Price_Reg': {'environmental': False,
                                       'is_assignment': False,
                                       'normal': True,
                                       'reading': 'Half_Price_Reg',
                                       'relevant': False,
                                       'status': 'UNKNOWN',
                                       'typ': 'Bool'},
                    '__rank': 9999},
 'Interaction_Reason': {'Interaction_Reason': {'environmental': False,
                                               'is_assignment': True,
                                               'normal': True,
                                               'reading': 'Interaction_Reason',
                                               'relevant': False,
                                               'status': 'UNIVERSAL',
                                               'typ': 'Interaction_Reasont_t',
                                               'value': 'Register',
                                               'values': ['Register']},
                        '__rank': 9999},
 'Microchipped': {'Microchipped': {'environmental': False,
                                   'is_assignment': False,
                                   'normal': True,
                                   'reading': 'Microchipped',
                                   'relevant': False,
                                   'status': 'UNKNOWN',
                                   'typ': 'Bool'},
                  '__rank': 9999},
 'Sterilization_Applicable': {'Sterilization_Applicable': {'environmental': False,
                                                           'is_assignment': False,
                                                           'normal': True,
                                                           'reading': 'Sterilization_Applicable',
                                                           'relevant': False,
                                                           'status': 'CONSEQUENCE',
                                                           'typ': 'Bool',
                                                           'value': True},
                              '__rank': 9999},
 'Sterilized': {'Sterilized': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'Sterilized',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
                '__rank': 9999},
 'Total': {'Total': {'environmental': False,
                     'is_assignment': True,
                     'normal': True,
                     'reading': 'Total',
                     'relevant': False,
                     'status': 'UNKNOWN',
                     'typ': 'Int',
                     'value': ''},
           '__rank': 9999},
 'Vet_Certificate': {'Vet_Certificate': {'environmental': False,
                                         'is_assignment': False,
                                         'normal': True,
                                         'reading': 'Vet_Certificate',
                                         'relevant': False,
                                         'status': 'UNKNOWN',
                                         'typ': 'Bool'},
                     '__rank': 9999},
 'ViciousDog': {'ViciousDog': {'environmental': False,
                               'is_assignment': False,
                               'normal': True,
                               'reading': 'ViciousDog',
                               'relevant': False,
                               'status': 'UNKNOWN',
                               'typ': 'Bool'},
                '__rank': 9999}}
