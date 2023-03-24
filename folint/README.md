FOLint 
======

FOLint is a linting tool for [FO(·)](https://fo-dot.readthedocs.io/en/latest/FO-dot.html).
Its functionality can be split up in four parts:

* Detection of syntax errors
* Detection of type errors
* Detection of typical formalization errors
* Enforcing a style guide

This project was initially started by Lars Vermeulen during his master thesis: https://github.com/larsver/folint


Installation
------------

```
pip install folint
```

CLI usage
---------

```
folint file.idp
```

FOLint in editors
-----------------

FOLint can be integrated in many editors. 
A collection of guides are kept in the folint-in-editors folder.


Build new version
-----------------

```
python setup.py bdist_wheel sdist
```

Don't forget to update the version number of FOLint + the version number of IDP in the dependency!


Appendix: Full list of functionality
------------------------------------

For a full list, see "Vermeulen, L. (2022). Statische Code Analyse voor FO(·). KU Leuven. Faculteit Industriële Ingenieurswetenschappen."

Type Checking
=============

* Typing of comparisons (`f = g`, `f > g`, …)
* Typing of mathematical operators (`x + y`, `x - y`, …)
* Warning for untyped quantifiers
* Verifying the types of the elements in symbol interpretations

Common mistake checking
=======================

* Warning when using a conjunction with universal quantification (e.g., `!x in Person: age(x) > 18 & adult(x)`)
* Warning when using an implication with existential quantification (e.g., `?x in Person: driving_license(x) => sober(x)`)
* Worning when variable is only on one side of an equivalence (e.g., `!x,y: phi(x) <=> psi(x, y)`)

Style guide
===========

* Use brackets with negated `in` statement
* Warn against redundant brackets
* Naming conventions: Type starting with capital letter, other symbols in snake_case
* Highlight unused quantification variables
* Warn when not using `pretty_print`

Other
=====

* Wrong number of arguments for predicate/function
* Wrong number of arguments for `model_check` or using unknown block names
* Checking if types are defined in voc or struct
* Checking totality of functions
* Checking for duplicate entries in interpretations
* Checking corretness of entries in interpretations
* Other minor linting such as "no double spaces", "spaces around connectives", ...
