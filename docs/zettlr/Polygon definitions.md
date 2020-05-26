–-
title: Polygon definitions
tags: #analysis 
   ID: 20200525120420
–-
trying to use [definitions in the polygon theory](https://autoconfigparam.herokuapp.com/?gist=63b233676f9c465847c01901edf110b7&file=Polygon_definitions.idp)


Issues:
* some definitions are circular : one can compute the number of sides from the Type, and vice-versa.  But we cannot enter such dual definitions because of co-recursivity
* many quantified atoms missing in GUI → relevance is incorrect

Options
- [x] add `__goals()`  for defined symbols, so that co-constraints is added
- [x] [ ] problem with `__goals(Subtype)`: 
- [x] Expr.no_fresh_vars_before_expansion flag