.. _IDP:

.. role:: raw-html(raw)
   :format: html

The FO(:raw-html:`&#183`) Language
==================================

Overview
------------

The FO(:raw-html:`&#183`) language is used to create knowledge bases.
An IDP-Z3 program contains an FO(:raw-html:`&#183`) knowledge base and instructions to perform tasks on it.
It is made of the following blocks of code:

vocabulary
    specify the types, predicates, functions and constants used to describe the problem domain.

theory
    specify the definitions and constraints satisfied by any solutions.

structure
    (optional) specify the interpretation of some predicates, functions and constants.

display
    (optional) configure the user interface of the :ref:`interactive_consultant`.

main
    (optional) executable procedure in the context of the knowledge base


The basic skeleton of an IDP-Z3 program for the Interactive Consultant is as follows:

.. code::

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

.. include:: IDPLanguage/shebang.inc
.. include:: IDPLanguage/vocabulary.inc
.. include:: IDPLanguage/theory.inc
.. include:: IDPLanguage/structure.inc
.. include:: IDPLanguage/main.inc
.. include:: IDPLanguage/IDP3.inc
.. include:: IDPLanguage/summary.inc
