from configcase import ConfigCase
from dsl.DSLClasses import *

model: File = idpparser.model_from_file('example.h')

c = ConfigCase()

model.translate(c)

print(c.mk_solver())
print(c.mk_solver().check())
print(c.model())

print(c.relevantVals)
print(c.initialisationlist())