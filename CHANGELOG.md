# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) relative to the user interface and to the API exposed by the web server.

## [Unreleased yet]

*

## [0.8.1] - 2021-03-29

* update video tutorial

## [0.8.0] - 2021-03-25

### API
* (breaking) renamed `idp-solver` to `idp-engine`
* (breaking) Issue #45: partial support for dates.  Introduces new Date type, which may conflict with Date type in some vocabularies.
* (breaking) remove `Goal`, `View` as top level statements
* (breaking) IEP 16 (intensional objects).  Use new `$` built-in function to evaluate the symbol to be applied.
* IEP 03: allow enumeration of constructed types in theory/structure block
* IEP 03 : partial support for binary quantification, with unary predicates
* fix #73: improve Python API
* fix #70: Double unary symbol should be parsed
* Fix #72: Empty predicate in structure should be allowed

### Interactive Consultant
* experimental: allow grouping of symbols under headings
* improve Unicode buttons


## [0.7.2] - 2021-02-16

### API
* (breaking) IEP 03: use math notation for signature of predicate and functions
* (breaking) IEP 03: mathematical and CSV syntax for Enumerations
* (breaking) IEP 03: require `()` after constants and propositions
* (breaking) IEP 03: use `in`, `∈` in all quantifications: `!x in Color`
* (breaking) rename ``Symbols` into `Symbol` for consistency
* More verbose error messages + line and col numbers (issue #64)
* support for 'not in' operator
* IEP 09 Unicode: allow 𝔹, ℤ, ℝ symbols for types, and '←' in definitions
* IEP 11: allow multi-symbol declarations in vocabulary
* detect duplicate declarations

### GUI
* fix #23: functionality for showing units in the interface
* fix #59: "Explain" not working in SimpleRegistration
* fix #63: default structures are broken
* add "verify" mode to decision_table


## [0.6.1] - 2021-01-04

Issue #52: use `main` branch instead of `master`

### API
* (breaking) IEP 10: capitalize Bool, Int, Real types

### GUI
* fix issue #57


## [0.5.6] - 2020-12-22
[Access v0.5.6 on Google App Engine](https://20201222t185754-dot-interactive-consultant.ew.r.appspot.com/)

### API
* support [IEP 03 quick syntax changes](https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-03-Quick-syntax-changes):
  * enumerations in theory block
* support [IEP 08 'in' operator](https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-08-'in'-operator)
* better support quantification over symbols
* docs: added an IDP-Z3 developer reference
* publish idp_solver module on [Pypi](https://pypi.org/project/idp-solver/), with command line script
* generation of DMN table for a goal


### GUI
* support for a default structure


## [0.5.5] - 2020-11-19
[Access v0.5.5 on Google App Engine](https://20201119t122325-dot-interactive-consultant.ew.r.appspot.com/)

### API
* changed license to GNU LGPL 3
* add model_check(), model_propagate() to API
* add Problem class to API, with copy(), symbolic_propagate(), propagate(), simplify()
* use poetry for installation
* support [IEP 04 Incomplete enumerations](https://gitlab.com/krr/IDP-Z3/-/wikis/IEP-04-Incomplete-enumerations)
* support `if .. then .. else ..`

### GUI
* support Shebang line
* add buttons to insert UTF codes in editor


## [0.5.4] - 2020-10-06
[Access v0.5.4 on Google App Engine](https://20201006t101829-dot-interactive-consultant.ew.r.appspot.com/)

### API
* web IDE to develop and test knowledge bases
* command line interface to execute an IDP program with a main() block
* type of variables can now be omitted in quantifiers and aggregates (but there is no type inference from numeric expressions)
* (macros) quantification on `Symbols type (except definitions)
* support named vocabulary for structures

### GUI
* fix data entry issues


## [0.5.3] - 2020-09-15
[Access v0.5.3 on Google App Engine](https://20200915t113559-dot-interactive-consultant.ew.r.appspot.com/)

### API
* use IDP3 syntax for 2 theories (environment + decision)
* support simple `display` theory, with `goal`, `relevant`, `expand`, `hide`, `view` and `moveSymbols` predicates
  * `view` in /meta can take the `hidden` value
  * replace `__goals(Term)` by `__relevant(Term)`
* add "environmental" of symbols in /meta's response
* add "is_assignment' to /eval's response

### GUI
* File / New
* File / Help


## [0.5.1] - 2020-05-26
[Access v0.5.1 on Google App Engine](https://20200526t173848-dot-interactive-consultant.ew.r.appspot.com/)

### API
* use informational relevance to compute relevance
* add '__rank' attribute to each symbol, per informational relevance
* new predicate `__goals(Term)`

### GUI
* hosting on Google App Engine
* sort symbols per relevance rank
* File / Share using URL


## [0.5.0] - 2020-04-29

### API
* add ENV_UNIV for universal environmental atoms
* add English annotations to symbols in vocabulary
* fix bug with Fresh_Variable
* not possible anymore to chain implications

### GUI
* improve determination of relevance for theories with definitions


## [0.4.1] - 2020-04-01
### API
* support of relevance for theories with definitions
* fixed error in substraction (0-x incorrectly computed)
* Issue #4: support for string literals as Constructors
* use minimal unsat-core for explain
* now using python 3.8

### GUI
* fix handling of environmental consequences
* avoid duplicates in explain


## [0.4.0] - 2020-03-16
### API
* add EXPANDED status
* use 'relevant' field, not 'RELEVANT' value in Get /eval response
* remove 'ct', 'cf' from /eval Request
* add global variables for environmental vs decision variables
### GUI
* green box around decision symbols
* use transparency for irrelevant symbols, unexpected value of sentences to be verified


## [0.3.2] - 2020-01-30
### Fixed
Various small fixes.


## [0.3.1] - 2020-01-30
### Fixed
* Fixed incorrect port in javascript


## [0.3.0] - 2020-01-30
### API
* add 'status' (UNKNOWN, GIVEN, UNIVERSAL, ...) to the GET response of /eval
* support for separate environment and decision vocabulary, with improved propagation.
    * add 'ENV_CONSQ' status
    * add 'environmental' to the GET response of /eval
### GUI
* Improved color coding of buttons.
* Hide irrelevant sentences / symbols (for theories without definitions).
* More compact symbol panel: header is not shown if only one sentence is shown.
### Fixed
* [Issue #2](https://gitlab.com/krr/IDP-Z3/issues/2)


## [0.2.0] - 2020-01-22
### API
* 'expanded' is now expected on any 'eval' call.  It contains a list of symbol names. The server will determine if any subtences that contain any of those symbols is a consequence of user's input, and ignore the others (for performance reasons).
### GUI
* user's input is used to simplify the theory, before sending it to Z3. This may result in better propagation in some cases.  Later, it will be used to determine relevance.
### Fixed
* 'Check Code' works again.


## [0.1.0] - 2019-12-10
### Added
* 19 nov 2019: REST API: atom in explain is now preceded by '~' if negated
* 9 sept 2019: abstract models: fix bug with checkCode, use given and consequences to simplify them, avoid negations
* GUI: hide symbols starting with '\_'.  Replace '\_' by spaces in symbol names, constructors
* GUI: 2 optimize buttons are now next to entry fields (not in box header).  (Remove "do not optimize" button)
* grammar: "goal <symbol>" forces the goal to be shown expanded
* grammar: "view ('normal' | 'expanded')"  Normal view only shows entry fields for a symbol; expanded view also shows the simplest boolean sub-expressions of the idp theory that contain the symbol ("atomQ").
* docs folder contains documentation, such as python call graphs and description of REST API
* fix Issue #1: show entry fields for all possible combinations of arguments of functions / predicates.
* refactoring:
    * remove 'init' method of /eval
    * simplify REST API
    * reorganize source code file per chronological order of calls
    * remove unused code
* improve minization of Real terms for theories with strict inequalities (by repeatedly calling minimize)
