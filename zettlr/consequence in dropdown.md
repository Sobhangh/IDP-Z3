consequence in dropdown
=
20200408162211

problem: consequences not shown in dropdown when atom does not occur in the theory
* is_visible in Case() looks for AppliedSymbol, Symbol, but not comparisons
* → need to identify Assignments from Comparison

Options:
* enumerate all possible assignments and add them to guilines as visible
    * but propagate only looks at assignments → add them to assignments too [[20200408193022]] merge case.GuiLines and .assignments
* use SymbolDeclaration.typeConstraints to add all possible assignments to GuiLines ? 
    * Deprecated → add them to assignments ?
    * also, won't work for range 0..10
- [x] detect Assignments in code, and make them visible
    * but won't work for year calculations in registration application

Performance issue ?

Where to detect assignments ?
* in Annotate ?  yes
    * but will not work for range declarations with computations (e.g. a ≠ b+1 will not exclude values-), e.g. registration !
    * alternative is to evaluate all instances, but that could be expensive
* in update_regs ?


#icanalysis