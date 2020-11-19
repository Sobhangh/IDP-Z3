–-
title: IEP 05 Man and Max aggregate
tags: #IEP
   ID: 20201119092538
–

- [x] preliminary : `Substitute.py\AQuantification` expand outermost quantifier before innermost ones
* [ ]  modify Idp/idp.tx syntax file to accommodate min/max
* [ ]  modify `Substitute.py\AQuantification` :
    * [ ]  use Fresh_Variable.**init**() to create a new Fresh_Variable of appropriate type
        * [ ]  the name is the code of the aggregate `min{...}`
    * [ ]  store that variable in self.simpler
    * [ ]  build the 2 co-constraints (using make() functions as in Idp/**init**.py : Rule.compute())
    * [ ]  set co_constraint to the conjunction of these 2 constraints
* [ ]  modify Expression.py\\Fresh_Variable: process co-constraints in .collect()
* [ ]  add test cases in `tests/3 arithmetic`: simple, complex, with environment/decision variables
* [ ]  update sphinx documentation
* [ ]  close [issue # 10 on gitlab](https://gitlab.com/krr/autoconfigz3/-/issues/10)