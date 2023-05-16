gebeurtenis() -> huwelijk
gebeurtenis_datum() -> #2023-05-10
persoon() -> zelf
? begrafenis_datum()
? nodige_tijd()
dagen_verlet() -> 2
? opgenomen(#2023-05-08)
? opgenomen(#2023-05-09)
? opgenomen(#2023-05-10)
? opgenomen(#2023-05-11)
? opgenomen(#2023-05-12)
van_toepassing(1)
Not van_toepassing(4)
Not van_toepassing(15)
gebeurtenis_datum() = #2023-05-10
gebeurtenis() = huwelijk
persoon() = zelf
dagen_verlet() = 2
Not gebeurtenis() = overlijden
Not dagen_verlet() = 10
Not #{dag ∈ opgenomen : dag ≤ begrafenis_datum()} = 3
? #2023-05-08 ≤ begrafenis_datum()
? #2023-05-09 ≤ begrafenis_datum()
? #2023-05-10 ≤ begrafenis_datum()
? #2023-05-11 ≤ begrafenis_datum()
? #2023-05-12 ≤ begrafenis_datum()
Not gebeurtenis() = familieraad
Not dagen_verlet() = (if nodige_tijd() > 1 then 1 else nodige_tijd())
? nodige_tijd() > 1
#{dag ∈ opgenomen : true} ≤ dagen_verlet()
∃ x ∈ Clause: van_toepassing(x)
Not dagen_verlet() = 0
