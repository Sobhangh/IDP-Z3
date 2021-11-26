weight() -> 80
No more consequences.
['Male', 'Female']

bmi() -> 0.003125
riskLevel() -> Low
weight() -> 80
No more consequences.

Low risk if neither Overweight, Obese_I, Obese_II nor Extreme_obesity
bmi() = $bmi$ ⇔ $bmi$ = weight() / (length() ⨯ length())
length() = 160
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Severely_Underweight ∧ (bmi() < 18.5 ∧ sex() = Male)
weight() = 80
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Underweight ∧ (bmi() < 18.5 ∧ sex() = Female)
