Merge case.GuiLines and .assignments
=
20200408193022

Currently:
* GuiLines: vocabulary.terms + [[subtences]]
* Assignments: vocabulary.terms + subtences + given

Problems:
* is_visible must be determine up-front
    * propage creates new Assignment → visible info is lost, unless it is copied
* GuiLines used in inferences

TODO:
- [x] Assignments are (expr → value) where value can be of any type (not just boolean)
- [x] do not create new Assignments in propagate, update them !
- [ ] Assignment() create with visible

#refactoring