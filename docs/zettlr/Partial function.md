## TODO
* [ ] rename
	* [X] Subtype to Type
	* [ ] problem to Theory
* [ ] align function names in TypeDeclaration, SymbolDeclaration, Type
    * they should look-up theory.interpretations[ ] !
    * [x] extension(interpretations, extensions) -> (superset, filter(expr))  (instead of range(); only for predicates or types)
        * [x]  change signature of range()
    * [ ] is_defined(expr, interpretations?) (instead of has_in_domain(expr))
* [ ] filter model generation
    * [ ] domain(interpretations)

- [x] represent empty vs infinite superset
- [x] type.extension is a list of list
- [x] use function for filter in interpret
- [x] remove TypeDeclaration.range
- [x] remove SymbolDeclaration.in_domain
- [x] proper product of filter
- [x] use interpretations in extensions (beware of circularity !)
- [ ] allow predicate in signature
	- [x] SymbolDeclaration.translate(): need to find the type of a unary predicate
	- [x] SymbolDeclaration.contains_element()
	- [x] n-ary quantification in LivingBeing
	- [x] interpretation also defines the domain
	- [x] use extension in model expand
	- [x] use extension in propagate
	- [x] exclude similar models
- [ ] take ":>=" into account (for predicates)
- [x] improve contains_element, has_element
- [x] IC: z3 sort expected

## Call tree

```mermaid
flowchart TD
	Symbol_has_element["Symbol<br/>has_element()"] --> TypeDecl_check_bounds["TypeDecl<br/>contains_element()"];
	SymbolInterpretation_interpret["SymbolInterp<br/>interpret()"] --> SymbolDeclaration_has_in_domain["SymbolDecl<br/>has_in_domain()"];
	SymbolInterpretation_interpret --> SymbolDeclaration_has_in_range["SymbolDecl<br/>has_in_range()"];
	SymbolDeclaration_has_in_domain --> Symbol_has_element;
	SymbolDeclaration_has_in_range --> Symbol_has_element;
	Enumeration_contains --> Symbol_has_element;
	Definition_get_instantiables["Definition<br/>get_instantiables()"] --> Subtype_extension["Subtype<br/>extension()"];
	Symbol_has_element --> Subtype_extension;
	SymbolDeclaration_interpret["SymbolDecl<br/>interpret()"] --> Subtype_extension;
	Constructor_interpret["Constructor<br/>interpret()"] --> Subtype_extension;
	AQuantification_interpret["AQuant<br/>interpret()"] --> Subtype_extension;
	AppliedSymbol_interpret[AppliedSymbol<br/>interpret] --> Enumeration_contains;
	TypeDeclaration_interpret[TypeDeclaration<br/>interpret] --> Enumeration_extensionE[Enumeration<br/>extensionE] --> Symbol_has_element;
	SymbolDeclaration_interpret --> TypeDecl_check_bounds -.-> Subtype_extension;
```
