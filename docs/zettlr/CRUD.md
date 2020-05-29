–-
title: CRUD
tags: #documentation
Date: 20200519215126
–-

|                                     | sub_exprs | simpler | value | co_constraint |
|-------------------------------------|-----------|---------|-------|---------------|
| __eq__                              | R         | R       | R     |               |
| str                                 | R         | R       | R     |               |
| annotate                            | R         | R       | R     |               |
| expand_quantifiers                  | U         | C       | C     |               |
| instantiate                         | U         | C       | C     | U             |
| interpret                           | U         | C       | C     | C             |
| instantiate_definition              | U         | C       | C     | U             |
| substitute                          | U         | U       | C     | U             |
| implicant                           | R         | R       | R     | R             |
| collect, subtences, unknown_symbols | R         | R       |       | R             |
| co_constraints                      | R         |         |       | R             |
| has_decision                        | R         |         |       |               |
