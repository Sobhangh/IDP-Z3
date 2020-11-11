–-
title: consequence in dropdown
tags: #analysis
Date: 20200408162211
–-

problem: consequences not shown in dropdown when atom does not occur in the theory
* is_visible in State() looks for AppliedSymbol, Symbol, but not comparisons
* → need to identify Assignments from Comparison

Options:
- [x] add SymbolDeclaration.typeConstraints to the theory 
    * also for ranges with less than 20 elements
- [x] detect Assignments in code, and make them visible
    * but won't work for year calculations in registration application
- [ ] enumerate all possible assignments and add them to guilines as visible
    * but propagate only looks at assignments → add them to assignments too [[Merge state.GuiLines and .assignments]] 

Performance issue ?

Where to detect assignments ?
* in Annotate ?  yes
    * but will not work for range declarations with computations (e.g. a ≠ b+1 will not exclude values-), e.g. registration !
    * alternative is to evaluate all instances, but that could be expensive
* in update_regs ?


