(declare-datatypes ((List 0)) (((nil) (cons (car Int) (cdr List)))))
(declare-fun a () List)
(define-funs-rec ( ( member ((x!1 Int) (x!2 List)) Bool)
                   ( positive ((x!1 List)) Bool)
                   ( len ((x!1 List)) Int)
                   ( increasing ((x!1 List)) Bool))
                 ( (or (and ((_ is (cons (Int List) List)) x!2)
                            ((_ member 0) x!1 (cdr x!2)))
                       (and ((_ is (cons (Int List) List)) x!2)
                            (= (car x!2) x!1)))
                   (or (and ((_ is (cons (Int List) List)) x!1)
                            (< 0 (car x!1))
                            ((_ positive 0) (cdr x!1)))
                       ((_ is (nil () List)) x!1))
                   (ite ((_ is (cons (Int List) List)) x!1)
                        (+ ((_ len 0) (cdr x!1)) 1)
                        0)
                   (let ((a!1 (and ((_ is (cons (Int List) List)) x!1)
                                   ((_ increasing 0) (cdr x!1))
                                   ((_ is (cons (Int List) List)) (cdr x!1))
                                   (< (car x!1) (car (cdr x!1))))))
                     (or a!1
                         (and ((_ is (cons (Int List) List)) x!1)
                              ((_ is (nil () List)) (cdr x!1)))
                         ((_ is (nil () List)) x!1)))))
(assert (and (= 2 ((_ len 0) a))
     ((_ positive 0) a)
     ((_ increasing 0) a)
     ((_ member 0) 1 a)
     ((_ member 0) 3 a)
     (or ((_ is (nil () List)) a) ((_ is (cons (Int List) List)) a))
     true
     true
     true
     true))


Model 1
==========
a := cons(1, cons(3, nil)).


More models may be available.  Change the max argument to see them.
