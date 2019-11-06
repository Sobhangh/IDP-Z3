Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)
--
ForAll([cout],
       (LipLen == [cout]) ==
       Or(And([cout] == Short, JacketDesign == Design_230)))
