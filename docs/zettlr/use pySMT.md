20200328102421

[website](https://pypi.org/project/PySMT/), [documentation](https://pysmt.readthedocs.io/en/latest/)

Benefits
* to be independent of solvers + portfolio approach
* has nice simplifiers and substituters
* for dReal ?  [delta-sat breaks many assumptions](https://github.com/pysmt/pysmt/issues/330), installation is difficult 

Todo:
* add annotations to expression (is_subtence, reading, ...) for relevance
* add inductive definitions : [[20200327114743]] SMT-LIB+

Options for annotations:
* modify 'substitute in pySMT
* use pySMT only at translate stage, after simplification

#analysis #refactoring #research
