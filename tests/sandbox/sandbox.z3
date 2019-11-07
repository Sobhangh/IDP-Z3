Or(LipLen == Short, LipLen == Standard)

Or(JacketDesign == Design_230, JacketDesign == Design_400HP)
--
ForAll($LipLen$,
       (LipLen == $LipLen$) ==
       Or(And($LipLen$ == Short, JacketDesign == Design_230)))
