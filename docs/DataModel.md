
---
Datamodels
---

For typing:

```{mermaid}
erDiagram
    Declaration ||--o{ Declaration : base_decl
    Declaration |o--o{ Set : sorts
    Declaration |o--|| Set: out
    Set }o--|| Declaration: decl
    Set |o--o{ Set: ins
    Set |o--o| Set: out
    Set |o--o{ Expression: type

    Declaration {
        Declaration base_decl
        List[Set] sorts
        Set out
    }
    Set {
        Declaration decl
        List[Set] ins
        Set out
    }
    Expression {
        Set type
    }
```

