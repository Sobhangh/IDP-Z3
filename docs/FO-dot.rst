.. _FO-dot:

.. role:: raw-html(raw)
   :format: html

The FO[:raw-html:`&#183`] Language
==================================

Overview
--------

The FO[:raw-html:`&#183`] (aka FO-dot) language is used to create knowledge bases.
It is described in the `FO-dot standard <https://fo-dot.readthedocs.io/en/latest/FO-dot.html>`_.
This document presents the implementation in IDP-Z3.


An FO-dot knowledge base is a text file containing the following blocks of code:

vocabulary
    specify the types, predicates, functions and constants used to describe the problem domain.

theory
    specify the definitions and axioms satisfied by any solutions.

structure
    (optional) specify the interpretation of some predicates, functions and constants.


The basic skeleton of an FO-dot knowledge base is as follows:

.. code::

    vocabulary {
        // here comes the specification of the vocabulary
    }

    theory {
        // here comes the definitions and axioms
    }

    structure {
        // here comes the interpretation of some symbols
    }


Everything between ``//`` and the end of the line is a comment.

.. include:: IDPLanguage/shebang.inc
.. include:: IDPLanguage/vocabulary.inc
.. include:: IDPLanguage/theory.inc
.. include:: IDPLanguage/structure.inc
.. include:: IDPLanguage/IDP3.inc
