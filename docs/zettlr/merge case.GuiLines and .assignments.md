Merge case.GuiLines and .assignments
=
20200408193022

Currently:
* GuiLines: vocabulary.terms + [[subtences]]
* Assignments: subtences + given

Problems:
* is_visible must be determine up-front
    * propage creates new Assignment → visible info is lost, unless it  is copied
* GuiLines used in inferences

TODO:
* Assignment() create with visible

#refactoring