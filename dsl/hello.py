from textx import metamodel_from_file

from configcase import ConfigCase


def handleModel(model):
    handleVoc(model.voc)
    handleTheo(model.theo)


def handleVoc(model):
    for i in model.declaration:
        handleDeclaration(i)


def handleTheo(model):
    for i in model.constraint:
        handleConstraint(i)
    pass


def handleDeclaration(i):
    print(i)
    print(str(type(i)) == 'SymbolDeclaration')
    print(str(type(i)))
    pass


def handleConstraint(i):
    pass


hello_meta = metamodel_from_file('hello.tx', memoization=True)

model = hello_meta.model_from_file('example.h')

c = ConfigCase()
handleModel(model)
