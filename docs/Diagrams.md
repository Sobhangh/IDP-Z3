
---
Datamodel
---

Datamodel for type checking:

```{mermaid}
erDiagram
    Declaration |o--o{ SetName : domains
    Declaration |o--|| SetName: codomain
    Declaration |o--o{ Expression: decl
    VarDeclaration |o--|| SetName: subtype
    SetName }o--|| Declaration: decl
    SetName |o--o{ SetName: concept_domains
    SetName |o--o| SetName: codomain
    SetName ||--o{ Expression: type
    SetName ||--o| SetName: root_set
    Constructor }o--o{ SetName : domains
    Constructor }o--|| SetName : codomain
    Constructor |o--o| Declaration: concept_decl
    Constructor |o--o{ Expression: decl
    Declaration ||--o{ Constructor: constructors

    Declaration {
        List[SetName] domains "Sets defining the domain of the symbol"
        SetName codomain "Set defining the codomain of the symbol"
        List[Constructor] constructors "only for `constructured from` enumerations"
    }
    VarDeclaration {
        SetName subtype
    }
    SetName {
        Declaration decl "Declaration of the set name"
        SetName root_set "root of the set in the type hierarchy"
        List[SetName] concept_domains "only for subset of Concept"
        SetName codomain "only for subset of Concept"
    }
    Expression {
        SetName type "type of the expression"
        Declaration-Constructor decl "only for (un)applied symbol"
    }
    Constructor {
        List[SetName] domains "empty for identifiers"
        SetName codomain  "type of the constructor"
        Constructor concept_decl "only for Concept identifiers"
    }
```

