# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) relative to the user interface and to the API exposed by the web server.

## [0.10.7] - 2023-05-04

The main new features in this release are:
* new syntax for aggregates (MR !294)

Contributors (alphabetical): Pierre Carbonnelle, Simon Vandevelde.

### IDP-Z3
* MR !304: show line number for internal error in python code
* MR !305: IEP 27 `if` in sum / min / max aggregates
* issue #271: Incomplete interpretation of set of integers (+ MR !310)

### Interactive Consultant and Web IDE
* MR !302: incorrect linter error for partial interpretation of function
* issue #268: Open FLAIR link in new tab
* issue #273: Access to documentation is broken


## [0.10.4] - 2023-04-17

The main new features in this release are:
* support for recursive data types (#185)

This release has new package dependencies: please run `poetry install` to update.

Contributors (alphabetical): Pierre Carbonnelle, Simon Vandevelde.

### IDP-Z3
* MR !294: `are necessary and sufficient conditions for`
* issue #185: support for recursive datatypes
* issue #249: regression of performance with new Z3 solver
* issue #254: Improve type checking on inequalities
* issue #255: Line numbers are wrong
* issue #257: Error messages for uninterpreted types
* issue #262: "ground" in error messages

### Interactive Consultant and Web IDE
* MR !300: improve loading time in IC
* MR !301: access proper version of documentation
* issue #252: incorrect relevance with if-then-else
* issue #258: Disable (certain) style warnings


## [0.10.3] - 2023-03-24

The main new features in this release are:
* Support for co-inductive definitions (MR !279)
* connectives in English (MR !290)
* automated testing of the IC using Cypress  (See README.md for installation) (#242)

This release has new package dependencies: please run `poetry install` to update.

Contributors (alphabetical): Pierre Carbonnelle, Simon Vandevelde.

### IDP-Z3
* MR !279: Support co-inductive definitions
* MR !280: various small improvements
* MR !284: Refactor Expression.simpler for better performance
* MR !290: English connectives in formula
* issue #235: range interpretation of predicate is not respected
* issue #236: Incorrect nested quantification over infinite domain
* issue #238: Fix FOLint issues in structure
* issue #240: internal error with quantification over infinite domain
* issue #246: error with chained inequalities

### Interactive Consultant and Web IDE
* MR !282: improve display of ⇒ in the editor.
* MR !289: use narrower numeric field
* issue #192: access to gist temporarily disabled
* issue #241: Environmental verification error in the Covid example
* issue #245: Fix bugs in the Save functionality
* issue #242: Can't retract assertion in Polygon (+ Cypress)
* issue #247: issues with Date field


## [0.10.2] - 2022-12-19

Contributors (alphabetical): Pierre Carbonnelle.

### IDP-Z3
* issue #234: Syntax Error `AConjunction` object has no attribute `symbol`

### Interactive Consultant and Web IDE
* issue #233: IDE should show irrelevant propositions in models


## [0.10.1] - 2022-12-14

Breaking change:
* MR !275: The symbol for partial interpretation is now `>>` or `⊇` (instead of `:>=` or `:⊇`).

Contributors (alphabetical): Pierre Carbonnelle, Simon Vandevelde.

### IDP-Z3

* issue #213: Expanding an empty theory results in 10 empty models
* issue #216: Internal error due to incorrect type constraint
* issue #218: binary quantification over infinite domain
* issue #219: declared variable in binary quantification
* issue #220: Value added twice to predicate output
* issue #221: Error in Min/max aggregate
* issue #224: Error when quantifying over subset of constructed type with infinite domains
* issue #225: Error in type inference for `min/max` aggregate
* issue #226: Failure of type inference over infinite domain
* issue #228: Expansion inference should better respect the `timeout_seconds` parameter
* issue #229: colon ':' in reading before quantor gives error in IC
* MR !271: support for empty type
* MR !275: allow `≜` for `:=`

### Interactive Consultant and Web IDE

* issue #123: show Theory in plain English
* issue #210: use latest grammar in folint
* issue #217: issue with dropdown in IC
* issue #227: respect spaces in IDE output
* issue #230: maximum recursion depth exceeded with inductive definition
* issue #231: Incorrect behavior when entering negative numbers
* issue #232: Should be able to minimize over a range
* MR !270: add support for slider below numeric field
* MR !275: allow `≜` for `:=`


## [0.10.0] - 2022-10-07

This release uses the poetry 1.2.  If you use poetry, you need to update it.

> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --uninstall
> curl -sSL https://install.python-poetry.org | python3 -

This release has new package dependencies: please run `poetry install` to update.

Breaking changes:
* FO[Sugar] now use `¬f(x) is enumerated` and `¬f(x) in {...}` (instead of `f(x) is not enumerated` and `f(x) not in {...}`)
* FO[Sugar] partial function interpretations must use `:>=` instead of `:=`.
* `timeout` parameter in API is now `timeout_seconds`

Contributors (alphabetical): Pierre Carbonnelle, Simon Vandevelde, WhereIsW4ldo.

### IDP-Z3
* (breaking) #186: FO[Sugar] negation of `is enumerated` and `in {...}`
* (breaking) !217: FO[PF] Unary predicates in type signature (+ partial interpretetations)
* (breaking) !218: `timeout` parameter in API is now `timeout_seconds`
* fix #55: add `minimize` and `maximize` functions in `main` block
* fix #120: FO[Infinite] Enumerate predicate over infinite domain
* fix #187: `Internal error` with `explain()`
* fix #188: Incorrect solver result during explain inference
* fix #190: presentation of false propositions in models
* fix #194: Decision table returns whether timeout was reached
* fix #195: add version flag to CLI
* fix #196: Can't change default real value
* fix #199: remove the predicates of types
* fix #204: improve API for minimizing model
* fix #208: Incorrect "Too many variables in head of rules of a definition"
* fix #211: Incorrect model for constant of type Concept
* MR !214: support for `#TODAY(y,m,d)`
* MR !225: allow `--no-dev` install in poetry
* MR !243: Improve performance
* MR !244: Declaration of variables ([IEP24](https://gitlab.com/krr/IDP-Z3/-/wikis/IEP%2024%20Variable%20declarations))

### Interactive Consultant and Web IDE
* fix #169: IC: need to better handle rationals
* fix #202: Various IDE improvements
* fix #205: could not run Web IDE on Windows
* fix #207: error in environmental consequences
* MR !228: Integrate FOLint linter into the editors
* MR !236: Add "File / Save..." button to IC and Web IDE


## [0.9.2] - 2022-02-10

Highlights of the breaking changes:
* A `.` is now required after a symbol interpretation in a theory or structure, e.g. `color := {red, blue, green}.`. The string output of some API methods also has a `.` after an enumeration.
* use `import` to include a vocabulary in another.
* `Concept` must always be followed by a type signature, in vocabulary and in quantifications. The introspection functions are not supported anymore (`arity, input_domain, output_domain`)

### IDP-Z3
* (breaking) fix #182: Require a `.` after a symbol interpretation in a theory or structure
* fix #181: Should detect error in `∀c in q[()->Bool]:`
* fix #183: should check domain and range in enumerations
* fix #184: nested Concept subtypes
* (breaking) MR !206: 'import' vocabulary

### Other
* MR #207: add analytics to www.idp-z3.be, with user consent



## [0.9.1] - 2022-01-25

Highlights of the breaking changes:
* `model_expand` API is now a regular function, not an iterator
* API functions do not accept a list of theories anymore (e.g., `model_check([T,S])`.  Use `model_check(T,S)` instead)
* the `goal` and `relevant`predicates are not accepted in the `display` block. Use an enumeration of `goal_symbol` instead.
* use an enumeration for `expand` in the display block

Contributors (alphabetical): Benjamin Callewaert, Jo Devriendt, Pierre Carbonnelle, Simon Vandevelde.

### API
* (Breaking) MR !184: add `Theory.determine_relevance(self)` to the official API
* (breaking) MR !193: minor public API changes
* fix #163: improve performance by avoiding unnecessary copying
* fix #170: reduce the need for parenthesis in expressions (annotations, if..then..else)
* fix #177: Incorrect translation of `$(c)(Adhesive()) is enumerated`
* fix #179: duplicate declaration of `_max`
* MR !181: support Python 3.10
* MR !183: add enable_law and disable_law to the API
* MR !188: print models in uniform format to structure
* MR !196: add `Theory.to_smt_lib` API
* MR !198: Performance: replace applied symbols by their interpretation, if known

### Interactive Consultant
* fix #125: Bug in relevance for Registration
* Web-MR !50: open local file with `/?file=spec.idp`
* MR !171, !180: refactor inferences to use a stateful solver, for performance.
* MR !186: switching between reading and formula view now works for explanations too.
* MR !187: fix regression where unsatisfiable theories were not explained in the IC.
* MR !183: allow to disable axioms
* MR !190: add Covid example
* MR !201: allow switching from IDE to IC, and vice-versa


## [0.9.0] - 2021-12-16

Highlights of the breaking changes:
* `sum{x in T: p(x): t(x)}` is now `sum(lambda x in T: t(x))`
* `Symbol` is now `Concept`
* `Problem(T,S)` is now `Theory(T,S)`

Contributors (alphabetical): Jo Devriendt, Pierre Carbonnelle, Simon Vandevelde.

### API
* (breaking) MR !152: IEP 22 change syntax of sum aggregate to sum(lambda <quantee>: expr)
* (breaking) MR !154: built-in type is "Concept" (not "Symbol")
* (breaking) MR !170: add timeout parameter to model expansion/optimisation and improve performance
* (breaking) MR !178: rename `Problem` class to `Theory`
* (breaking) MR !179: `optimize` does not return a full model anymore; it only returns the optimized value
* fix #5: do not allow arithmetic operations on constructors
* fix #132, #136: Improve error message for mis-applied symbol
* fix #137: support of functions from Concept to Concept
* fix #146: "Context mismatch" when performing abstract model expansion
* fix #152: Error in binary quantification in aggregate
* fix #156: Concept: error when using several vocabularies
* fix #161: Improve "Duplicate declaration of..." error
* MR !145: Improve performance of explain
* MR !153: improve performance in case of large interpretations for symbols that do not occur in the theory
* MR !158: allow signature in quantification: `!x in Concept[T1->T2]: ..`
* MR !172: IEP 05: Min and Max aggregates over anonymous function
* MR !176: remove ENV_UNIV status code
* MR !177: Allow `Concept[T->T]` in symbol declarations

### Interactive Consultant
* MR !147: allow the user to edit system choices after model expansion / optimisation
* MR !155: allow to disable optimization buttons for certain symbols
* MR !158: button in editor to check that the `$(..)(..)` are well-guarded;
* MR !160: IC should refuse theories without models
* web MR !40: Enable resizing the IDE editor window
* web MR !41: Support of touch devices
* web MR !42: stabilize the progress spinner
* fix #139: IC should detect and explain theories without models
* fix #147: incorrect reasoning about environmental consequences
* fix #151: Error in dropdown using Glue Select
* fix #160: Irrelevant boxes should show the title
* fix #167: Incorrect display of numeric value 1 in inconsistency panel
* fix #180: Incorrect explanation when a proposition is false by default


## [0.8.4] - 2021-09-30

Contributors (alphabetical): Jo Devriendt, Matthias Van der Hallen, Pierre Carbonnelle, Simon Vandevelde.

### API
* MR !124: add `duration()` API to allow measurement of time of processing in the `main` block.
* MR !126: improve performance by simplifying `abs` when possible
* (breaking) MR !132: `Problem.formula()`returns a Z3 object, for performance
* MR !141: improve performance of definitions containing other defined terms
* MR !142: more efficient inferences for large models
* MR !143: API: `IDP.from_file()` should return an IDP instance, not None
* Fix #49: improve command line interface
* fix #119: improve error message when too many variables in head of rule.
* fix #126: error in inductive definitions
* fix #127: error in definition with aggregates
* fix #128: fix enumerations that mix integer and real, or range over dates
* fix #130: error when using conflicting web sessions
* fix #134: incorrect printing of the result of `Problem.optimize` in main block

### Interactive Consultant
* MR !124: show the overall time of execution of each run in the IDE
* MR !138: improve speed of opening a drop-down
* MR !140: manual / optional Relevance
* web MR !29: "Print" view + dynamic horizontal sizing of consultant
* web MR !30: ctrl-S in editor runs the code
* Added info on API endpoint to docs


## [0.8.3] - 2021-08-18

Run `poetry install` to get the correct dependencies.

Contributors (alphabetical): Jo Devriendt, Matthias Van der Hallen, Pierre Carbonnelle, Simon Vandevelde.

### API
* Merge !90: add `IDP.from_file` and `IDP.from_str` to Python API
* Merge !93: improve speed by caching z3 translations
* Merge !98: Improve performance for theories with large structures
* Merge !99: implement IEP 15 Inductive definitions
* (breaking) Merge 101: simplify `get_range` API
* Merge !103: support alternative "batch" propagation algorithm (not faster)
* Merge !105: "directional propagation" to improve performance for a sequence of assert+propagate
* Merge !106: improve performance of Problem.simplify()
* Merge !117, !119: improve performance of Problem._from_model()
* Merge !118: allow unicode characters in non-logic symbols
* fix #88: Explanations should be rule-specific when possible
* fix #104: implications, equivalences are binary connectives, not n-ary.
* fix #105: Do not require parenthesis around quantification
* fix #111: Missing law in explanation when between brackets
* fix #116: Constructors on infinite domains
* fix #118: Incorrect models for definitions over infinite domains
* fix #121: Definitions over constructors with infinite domains

### Interactive Consultant
* fix #91: empty box in top right of IC
* fix #98: Incorrect relevance with definitions
* Merge 101: improve performance of IC (propagate dropdowns on request)
* fix #112: Don't repeat the symbol name for symbol tiles with a header
* fix #17 (web-IDP-Z3): When no model can be found, an explanation is shown.
* fix #113: Prettify not working correctly for ~=

## [0.8.2] - 2021-06-02

Contributors (alphabetical): Jo Devriendt, Matthias Van der Hallen, Pierre Carbonnelle, Simon Vandevelde.

### API
* (breaking) Merge !82: Problem must be created with `extended=True` for `decision_table()` API
* Merge !87: add `get_range` to Problem API
* Merge !88: add `abs` built-in function
* fix #90: error in `sum` aggregate
* fix #74: Incorrect propagation when a symbol is defined twice
* Merge !99: implement IEP 15 Inductive definitions

### Interactive Consultant
* Merge !85: improve performance of IC (better use of cache)
* fix #75: default structure not working in Registration application
* fix #89: `constructed from` types create error in IC
* fix #93: incorrect parsing of `main()` block in IDE
* fix #94: incorrect relevance when symbol starts with underscore
* fix #95: Incorrect relevance with quantified formula


## [0.8.1] - 2021-05-11

Contributors (alphabetical):  Jo Devriendt, Matthias Van der Hallen, Pierre Carbonnelle, Simon Vandevelde

### API
* (breaking) fix #85: use `pretty_print( )` in `procedure main()` block, instead of `print()`
* (breaking) Merge !77: consistently represent propositions and constants with `()` in Python API
* Merge !66: allow `⨯` for arithmetic product (IEP 09)
* Merge !68: support for N-ary constructors (IEP 06)
* Merge !70: improve binary quantification (IEP 03)
* Merge !75: add `Problem.explain()` to API
* Merge !78: add `assert_(code, value)` to Problem API
* fix #77: `in` operator does not work in some definitions
* fix #80: infinite loop for recursive definitions
* fix #81: Spill-over of structures
* fix #82: allow number and date ranges in structures
* fix #83: same symbol defined in multiple definitions
* fix #84: infinite loop when instantiating co_constraint

### Interactive Consultant

* Merge !67: add manual propagation button to interface
* Merge !66: add "toUnicode" button in editor
* fix #76: optionalPropagation and moveSymbols no longer working
* fix #75: default structure seems broken
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
