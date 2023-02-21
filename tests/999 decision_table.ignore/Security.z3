  Not HasRating(BE001) ≤ 77
⇒ Not Eligible(BE001)

  Not Issuer(BE001) in {GovernmentNationalMortgageAssociation, FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, AfricanDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank, BRITISHCOLUMBIA, TORONTO, MANITOBA, NEWBRUNsELEC, NEWBRUNSWICK, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, ALBERTA, QUEBEC, SASKATCHEWAN}
∧ Issuer_Type(BE001) = Supra
⇒ Not Eligible(BE001)

  Not Issuer(BE001) in {GovernmentNationalMortgageAssociation, FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, BRITISHCOLUMBIA, TORONTO, MANITOBA, NEWBRUNsELEC, NEWBRUNSWICK, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, ALBERTA, QUEBEC, SASKATCHEWAN}
∧ Not Issuer_Type(BE001) in {Supra, Sovereign}
⇒ Not Eligible(BE001)

  Country(BE001) in {Aus, Bel, Can, Den, Est, Fin, Fra, Ger, Hon, Ire, Isr, Ita, Jap, Lux, Net, New, Nor, Por, Sin, Slo, Sou, Spa, Swe, Swi, UniK, UniS}
∧ Issuer_Type(BE001) = Sovereign
⇒ Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) in {GovernmentNationalMortgageAssociation, FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation}
⇒ Eligible(BE001)

  Issuer(BE001) in {GovernmentNationalMortgageAssociation, FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation}
⇒ Not Eligible(BE001)

  Issuer(BE001) in {AfricanDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank}
∧ Issuer_Type(BE001) = Supra
⇒ Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) in {GovernmentNationalMortgageAssociation, FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, BRITISHCOLUMBIA, TORONTO, MANITOBA, NEWBRUNsELEC, NEWBRUNSWICK, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, ALBERTA, QUEBEC, SASKATCHEWAN}
⇒ Eligible(BE001)

⇒ Not Eligible(BE001)

end of decision table
