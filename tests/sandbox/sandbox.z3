Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)
--
ForAll(c!13,
       (LipLen == c!13) ==
       Or(And(c!13 == Short, JacketDesign == Design_230)))
