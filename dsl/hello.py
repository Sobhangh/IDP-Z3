from configcase import ConfigCase
from dsl.DSLClasses import *

model: File = meta.model_from_file('example.h')

c = ConfigCase()

model.translate(c)
