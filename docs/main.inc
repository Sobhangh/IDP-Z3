.. index:: main block

Main block
----------

UNDER CONSTRUCTION

The *main block* consists of python-like statements to be executed by the IDP-Z3 executable or the Web IDE, in the context of the knowledge base.
It takes the following form:

.. code-block::

    procedure main() {
        // here comes the python-like code to be executed
    }

The following functions are available:

print(...)
    Prints the arguments on stdout

model_expand(blocks, max=10)
    Returns a list of models for the theory obtained by merging `blocks` (a list of theories and structures).
    The result is limited to `max` elements (10 by default), or unlimited if `max` is 0.

    For example, `print(model_expand([T, S]))` will print (up to) 10 models of theory T with structure S.

