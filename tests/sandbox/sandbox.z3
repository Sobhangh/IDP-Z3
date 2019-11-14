Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)
--
ForAll(c!15,
       (LipLen == c!15) ==
       Or(And(c!15 == Short, JacketDesign == Design_230)))
