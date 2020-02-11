# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) relative to the user interface and to the API exposed by the web server.


## [Unreleased]
### API

* add 'relevant' field, remove 'IRRELEVANT' value in Get /eval response
* remove 'ct', 'cf' from /eval Request

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

* [Issue #2](https://gitlab.com/krr/autoconfigz3/issues/2)

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
* improve minization of real terms for theories with strict inequalities (by repeatedly calling minimize)
