  Not HasRating(BE001) ≤ 77
⇒ Not Eligible(BE001)

  Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
∧ Not AssetSubClass(BE001) = ABS
⇒ Eligible(BE001)

  Country(BE001) in {Aus, Bel, Can, Den, Est, Fin, Fra, Ger, Hon, Ire, Isr, Ita, Jap, Lux, Net, New, Nor, Por, Sin, Slo, Sou, Spa, Swe, Swi, UniK, UniS}
∧ Issuer_Type(BE001) = Sovereign
⇒ Eligible(BE001)

  Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
⇒ Not Eligible(BE001)

  Issuer(BE001) in {AfricanDevelopmentBank, AsianDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank}
∧ Issuer_Type(BE001) = Supra
⇒ Eligible(BE001)

  Issuer(BE001) in {FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, GovernmentNationalMortgageAssociation}
∧ Not Issuer(BE001) in {AfricanDevelopmentBank, AsianDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank}
∧ Not AssetSubClass(BE001) = ABS
⇒ Eligible(BE001)

