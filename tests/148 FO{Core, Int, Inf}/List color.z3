(declare-datatypes ((Color 0)) (((red) (blue) (green))))
(declare-datatypes ((List 0)) (((nil) (cons (car Color) (cdr List)))))
(declare-fun a () List)
(declare-fun len (List) Int)
(assert (let ((a!1 (forall ((c!0 List))
             (or (not (or ((_ is (nil () List)) c!0)
                          ((_ is (cons (Color List) List)) c!0)))
                 (= (= 0 (len c!0)) (= c!0 nil)))))
      (a!2 (or (and (= 0 (len a)) (= a nil))
               (exists ((c!1 Int))
                 (let ((a!1 (= (len a) (+ (len (cdr a)) 1))))
                   (and a!1 ((_ is (cons (Color List) List)) a))))))
      (a!3 (and (= 0 (len (cdr a))) (= (cdr a) nil)))
      (a!4 (exists ((c!2 Int))
             (let ((a!1 (+ (len (cdr (cdr a))) 1)))
               (and (= (len (cdr a)) a!1)
                    ((_ is (cons (Color List) List)) (cdr a))))))
      (a!5 (= 0 (len (cdr (cdr a)))))
      (a!7 (exists ((c!3 Int))
             (let ((a!1 (len (cdr (cdr (cdr a))))))
             (let ((a!2 (= (len (cdr (cdr a))) (+ a!1 1))))
               (and a!2 ((_ is (cons (Color List) List)) (cdr (cdr a)))))))))
(let ((a!6 (and a!5 (= (cdr (cdr a)) nil))))
  (and a!1
       (= 2 (len a))
       (or ((_ is (nil () List)) a) ((_ is (cons (Color List) List)) a))
       a!2
       (or a!3 a!4)
       (or a!6 a!7)))))


Model 1
==========
a := cons(blue, cons(blue, nil)).


Model 2
==========
a := cons(blue, cons(green, nil)).


Model 3
==========
a := cons(blue, cons(red, nil)).


Model 4
==========
a := cons(green, cons(blue, nil)).


Model 5
==========
a := cons(green, cons(green, nil)).


Model 6
==========
a := cons(green, cons(red, nil)).


Model 7
==========
a := cons(red, cons(blue, nil)).


Model 8
==========
a := cons(red, cons(green, nil)).


Model 9
==========
a := cons(red, cons(red, nil)).


No more models.
