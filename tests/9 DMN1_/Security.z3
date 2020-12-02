  Not HasRating(BE001) ≤ 77
∧ Not Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
⇒ Not Eligible(BE001)

  Not HasRating(BE001) ≤ 77
∧ AssetSubClass(BE001) = ABS
⇒ Not Eligible(BE001)

  Not AssetSubClass(BE001) = ABS
∧ Issuer(BE001) in {ALBERTA, BRITISHCOLUMBIA, MANITOBA, NEWBRUNSWICK, NEWBRUNsELEC, NEWFOUNDLAND, NOVASCOTIA, ONTARIO, PRINCEEDWARDISLD, QUEBEC, SASKATCHEWAN, TORONTO}
⇒ Eligible(BE001)

  Issuer(BE001) in {FederalHomeLoanMortgageCorporation, FederalNationalMortgageAssociation, GovernmentNationalMortgageAssociation}
∧ Not AssetSubClass(BE001) = ABS
⇒ Eligible(BE001)

  Issuer_Type(BE001) = Supra
∧ Issuer(BE001) in {AfricanDevelopmentBank, AsianDevelopmentBank, BankForInternationalSettlements, CaribbeanDevelopmentBank, CouncilOfEuropeDevelopmentBank, EuropeanBankForReconstructionAndDevelopment, EuropeanCentralBank, EuropeanInvestmentBank, EuropeanInvestmentFund, InterAmericanDevelopmentBank, InternationalBankForReconstructionAndDevelopment, InternationalFinanceCorporation, InternationalMonetaryFund, MultilateralInvestmentGuaranteeAgency, NordicInvestmentBank}
⇒ Eligible(BE001)

  Issuer_Type(BE001) = Sovereign
∧ Country(BE001) in {Aus, Bel, Can, Den, Est, Fin, Fra, Ger, Hon, Ire, Isr, Ita, Jap, Lux, Net, New, Nor, Por, Sin, Slo, Sou, Spa, Swe, Swi, UniK, UniS}
⇒ Eligible(BE001)

  
⇒ Not Eligible(BE001)

end of DMN table
