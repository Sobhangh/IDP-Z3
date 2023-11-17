
---
Datamodels
---

For typing:

```{mermaid}
erDiagram
    Declaration ||--o{ Declaration : base_decl
    Declaration |o--o{ Set_ : sorts
    Declaration |o--|| Set_: out
    Declaration |o--|| Set_: type
    Set_ }o--|| Declaration: decl
    Set_ |o--o{ Set_: ins
    Set_ |o--o| Set_: out
    Set_ |o--o{ Expression: type

    Declaration {
        Declaration base_decl
        List[Set_] sorts
        Set_ out
        Set_ type
    }
    Set_ {
        Declaration decl
        List[Set_] ins
        Set_ out
    }
    Expression {
        Set_ type
    }
```

