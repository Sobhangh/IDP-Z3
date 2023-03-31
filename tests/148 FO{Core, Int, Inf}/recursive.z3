(declare-datatypes ((List 0)) (((nil) (cons (car Int) (cdr List)))))
(declare-fun a () List)
(define-funs-rec ( ( increasing ((x!1 List)) Bool)
                   ( negative ((x!1 List)) Bool)
                   ( len ((x!1 List)) Int))
                 ( (let ((a!1 (and ((_ is (cons (Int List) List)) x!1)
                                   ((_ increasing 0) (cdr x!1))
                                   ((_ is (cons (Int List) List)) (cdr x!1))
                                   (> (car x!1) (car (cdr x!1))))))
                     (or a!1
                         (and ((_ is (cons (Int List) List)) x!1)
                              ((_ is (nil () List)) (cdr x!1)))
                         (= x!1 nil)))
                   (or (and ((_ is (cons (Int List) List)) x!1)
                            (> 0 (car x!1))
                            ((_ negative 0) (cdr x!1)))
                       ((_ is (nil () List)) x!1))
                   (ite ((_ is (cons (Int List) List)) x!1)
                        (+ ((_ len 0) (cdr x!1)) 1)
                        0)))
(assert (and (= 2 ((_ len 0) a))
     ((_ negative 0) a)
     ((_ increasing 0) a)
     (or ((_ is (nil () List)) a) ((_ is (cons (Int List) List)) a))
     true
     true
     true))


Model 1
==========
a := cons(-1, cons(-2, nil)).


Model 2
==========
a := cons(-103185, cons(-103186, nil)).


Model 3
==========
a := cons(-28996, cons(-28997, nil)).


Model 4
==========
a := cons(-31433, cons(-31434, nil)).


Model 5
==========
a := cons(-39, cons(-40, nil)).


Model 6
==========
a := cons(-40288, cons(-40289, nil)).


Model 7
==========
a := cons(-52085, cons(-52086, nil)).


Model 8
==========
a := cons(-60450, cons(-60451, nil)).


Model 9
==========
a := cons(-7758, cons(-7759, nil)).


Model 10
==========
a := cons(-92735, cons(-92736, nil)).


More models may be available.  Change the max argument to see them.
