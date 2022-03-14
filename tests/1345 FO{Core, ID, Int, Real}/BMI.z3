weight() -> 80
No more consequences.
['Male', 'Female']

bmi() -> 0.003125
riskLevel() -> Low
weight() -> 80
No more consequences.

bmi() -> 0.003125
? BMILevel()
? sex()
riskLevel() -> Low
weight() -> 80
weight() = 80
Not riskLevel() = Increased
Not BMILevel() = Overweight
? BMILevel() = Severely_Underweight
bmi() < 18.5
bmi() = weight() / (25600)
? sex() = Male
? BMILevel() = Underweight
? sex() = Female
Not 18.5 ≤ bmi()
Not BMILevel() = Normal
Not 25 ≤ bmi()
Not BMILevel() = Obese_I
Not 30 ≤ bmi()
bmi() ≤ 34.9
Not BMILevel() = Obese_II
Not 35 ≤ bmi()
bmi() ≤ 39.9
Not BMILevel() = Extreme_Obesity
Not bmi() ≥ 40
Not riskLevel() = High
Not riskLevel() = Very_High
Not riskLevel() = Extremely_High
riskLevel() = Low

Low risk if neither Overweight, Obese_I, Obese_II nor Extreme_obesity
bmi() = $bmi$ ⇔ $bmi$ = weight() / (25600)
definition of BMILevel
weight() = 80

(declare-datatypes ((BMILevelt_t 0)) (((Obese_II) (Obese_I) (Normal) (Severely_Underweight) (Underweight) (Overweight) (Extreme_Obesity))))
(declare-datatypes ((riskLevelt_t 0)) (((High) (Very_High) (Low) (Increased) (Extremely_High))))
(declare-datatypes ((sext_t 0)) (((Male) (Female))))
(declare-fun BMILevel () BMILevelt_t)
(declare-fun riskLevel () riskLevelt_t)
(declare-fun waist () Real)
(declare-fun sex () sext_t)
(declare-fun weight () Real)
(declare-fun bmi () Real)
(assert (let ((a!1 (and (= BMILevel Overweight) (= sex Male) (>= (to_real 102) waist)))
      (a!2 (and (= BMILevel Overweight) (= sex Male) (< (to_real 102) waist)))
      (a!3 (and (= BMILevel Overweight) (= sex Female) (>= (to_real 88) waist)))
      (a!4 (and (= BMILevel Overweight) (= sex Female) (< (to_real 88) waist)))
      (a!5 (and (= BMILevel Obese_I) (= sex Male) (>= (to_real 102) waist)))
      (a!6 (and (= BMILevel Obese_I) (= sex Male) (< (to_real 102) waist)))
      (a!7 (and (= BMILevel Obese_I) (= sex Female) (>= (to_real 88) waist)))
      (a!8 (and (= BMILevel Obese_I) (= sex Female) (< (to_real 88) waist)))
      (a!9 (not (or (= BMILevel Overweight)
                    (= BMILevel Obese_I)
                    (= BMILevel Obese_II)
                    (= BMILevel Extreme_Obesity))))
      (a!10 (and (<= (/ 37.0 2.0) bmi) (>= (/ 249.0 10.0) bmi) (= sex Male)))
      (a!11 (and (<= (/ 37.0 2.0) bmi) (>= (/ 249.0 10.0) bmi) (= sex Female)))
      (a!12 (and (<= (to_real 25) bmi) (>= (/ 299.0 10.0) bmi) (= sex Male)))
      (a!13 (and (<= (to_real 25) bmi) (>= (/ 299.0 10.0) bmi) (= sex Female)))
      (a!14 (and (= BMILevel Obese_I)
                 (and (<= (to_real 30) bmi) (>= (/ 349.0 10.0) bmi))))
      (a!15 (and (= BMILevel Obese_II)
                 (and (<= (to_real 35) bmi) (>= (/ 399.0 10.0) bmi))))
      (a!17 (= (= BMILevel Obese_II)
               (and (<= (to_real 35) bmi) (>= (/ 399.0 10.0) bmi))))
      (a!18 (= (= BMILevel Obese_I)
               (and (<= (to_real 30) bmi) (>= (/ 349.0 10.0) bmi))))
      (a!20 (forall ((c!0 Real))
              (= (= bmi c!0) (= c!0 (/ weight (to_real 25600)))))))
(let ((a!16 (or (and (= BMILevel Severely_Underweight)
                     (and (> (/ 37.0 2.0) bmi) (= sex Male)))
                (and (= BMILevel Underweight)
                     (and (> (/ 37.0 2.0) bmi) (= sex Female)))
                (and (= BMILevel Underweight) a!10)
                (and (= BMILevel Normal) a!11)
                (and (= BMILevel Normal) a!12)
                (and (= BMILevel Overweight) a!13)
                a!14
                a!15
                (and (= BMILevel Extreme_Obesity) (<= (to_real 40) bmi))))
      (a!19 (= (= BMILevel Underweight)
               (or false
                   (and (> (/ 37.0 2.0) bmi) (= sex Female))
                   a!10
                   false
                   false
                   false
                   false
                   false
                   false))))
  (and (= (to_real 80) weight)
       (or (= BMILevel Obese_II)
           (= BMILevel Obese_I)
           (= BMILevel Normal)
           (= BMILevel Severely_Underweight)
           (= BMILevel Underweight)
           (= BMILevel Overweight)
           (= BMILevel Extreme_Obesity))
       (or (= sex Male) (= sex Female))
       (or (= riskLevel High)
           (= riskLevel Very_High)
           (= riskLevel Low)
           (= riskLevel Increased)
           (= riskLevel Extremely_High))
       (or (and (= riskLevel Increased) a!1)
           (and (= riskLevel High) a!2)
           (and (= riskLevel Increased) a!3)
           (and (= riskLevel High) a!4)
           (and (= riskLevel High) a!5)
           (and (= riskLevel Very_High) a!6)
           (and (= riskLevel High) a!7)
           (and (= riskLevel Very_High) a!8)
           (and (= riskLevel Very_High) (= BMILevel Obese_II))
           (and (= riskLevel Extremely_High) (= BMILevel Extreme_Obesity))
           (and (= riskLevel Low) a!9))
       a!16
       (= bmi (/ weight (to_real 25600)))
       a!17
       a!18
       (= (= BMILevel Normal)
          (or false false false a!11 a!12 false false false false))
       (= (= BMILevel Severely_Underweight)
          (and (> (/ 37.0 2.0) bmi) (= sex Male)))
       a!19
       (= (= BMILevel Overweight) a!13)
       (= (= BMILevel Extreme_Obesity) (<= (to_real 40) bmi))
       a!20
       (= (= riskLevel High)
          (or false a!2 false a!4 a!5 false a!7 false false false false))
       (= (= riskLevel Very_High)
          (or false
              false
              false
              false
              false
              a!6
              false
              a!8
              (= BMILevel Obese_II)
              false
              false))
       (= (= riskLevel Low) a!9)
       (= (= riskLevel Increased)
          (or a!1 false a!3 false false false false false false false false))
       (= (= riskLevel Extremely_High) (= BMILevel Extreme_Obesity))))))

