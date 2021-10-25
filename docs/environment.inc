.. index:: environment

Environment
-----------
Often, some elements of a problem instance are under the control of the user (possibly indirectly), while others are not.

To capture this difference, the FO(.) language allows the creation of 2 vocabularies and 2 theories.
The first one is called 'environment', the second 'decision'.
Hence, a more advanced skeleton of an IDP-Z3 program is:

.. code::

    vocabulary environment {
        // here comes the specification of the vocabulary to describe the environment
    }

    vocabulary decision {
        extern vocabulary environment
        // here comes the specification of the vocabulary to describe the decisions and their consequences
    }

    theory environment:environment {
        // here comes the definitions and constraints satisfied by any environment possibly faced by the user
    }

    theory decision:decision {
        // here comes the definitions and constraints to be satisfied by any solution
    }

    structure environment:environment {
        // here comes the interpretation of some environmental symbols
    }

    structure decision:decision {
        // here comes the interpretation of some decision symbols
    }

    display {
        // here comes the configuration of the user interface
    }
