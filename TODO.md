
reduce differences with idp:
    - support recursive constructors
    - support type hierarchy
    - type inference
    - avoid need to annotate well-founded definitions
    - support well-founded definitions of several symbols (mutually inductive)
    - support several wf definitions in theory

performance:
    - improve quantifier expansion (use grounding techniques)
    - avoid unnecessary quantifier in body when head arguments are not expressions

Nice To Have
    - IntsInRange: add restrictive