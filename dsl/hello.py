from textx import metamodel_from_file
hello_meta = metamodel_from_file('hello.tx')
example_hello_model = hello_meta.model_from_file('example.h')

print(example_hello_model.__dict__)