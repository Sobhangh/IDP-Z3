weight() -> 80
No more consequences.
['Male', 'Female']

bmi() -> 0.00249680097375238
riskLevel() -> Low
weight() -> 80
No more consequences.

length() = 179
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Severely_Underweight ∧ (bmi() < 18.5 ∧ sex() = Male)
BMILevel() = $BMILevel$ ⇐ $BMILevel$ = Underweight ∧ (bmi() < 18.5 ∧ sex() = Female)
bmi() = $bmi$ ⇔ $bmi$ = weight() / (length() ⨯ length())
Low risk if neither Overweight, Obese_I, Obese_II nor Extreme_obesity
weight() = 80
