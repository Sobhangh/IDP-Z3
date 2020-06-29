The IDP Language
================

Overview
------------

The IDP language is used to create knowledge bases.  
An IDP program is made of the following blocks of code:

vocabulary
    specify the types, predicates, functions and constants used to describe the problem domain.

theory
    specify the definitions and constraints satisfied by any solutions.

structure
    (optional) specify fixed interpretations of some predicates, functions and constants

display
    (optional) configure the user interface of the Interactive Consultant


The skeleton of an IDP program is thus as follows:

.. code-block::

    vocabulary {
        // here comes the specification of the vocabulary
    }

    theory {
        // here comes the definitions and constraints
    }

    structure {
        // here comes the interpretation of some symbols
    }

    display {
        // here comes the configuration of the user interface
    }

Everything between ``//`` and the end of the line is a comment.

.. include:: vocabulary.rst
.. include:: theory.rst