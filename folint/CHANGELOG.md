# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
- Fix false positives in structure.
- Multiple minor refactors (see https://gitlab.com/krr/IDP-Z3/-/merge_requests/291)

## [1.0.3] - 2022-09-28
- Various minor bugs


## [1.0.2] - 2022-08-02
### Fixed
- Various bugs related to contructed types
- Disabled the extra style checks for the procedure
- Removed style rule "No space after quantifier"
- Bug where unused or untyped variables would cause the program to crash
- Comments outside the IDP blocks don't throw warnings anymore
- In the structure, symbols no longer throw errors when their types are also defined in the structure.
- Increased verbosity of some warnings and errors

## [1.0.1] - 2022-06-27
### Fixed
- Fix bug: `display` was not recognised for indentation
- Fix bug: annotations are no longer style checked

## [1.0.0] - 2022-06-26
### Added
- 1.0.0 release of FOLint, big thanks to [Lars Vermeulen](https://github.com/larsver) who started this project during his master's thesis.
