This file describes the web API.

### URL: /meta

This page returns the list of symbols.

POST request:

```json
    - "code" : string 											   // source code in FO(ID)
```

POST result:

```json
    - title: string           // title of the page
    - symbols : [ {           // list of predicates/functions, each one corresponding to a box on the page
        - idpname : string    // name of the predicate/function in the FO(ID) vocabulary
        - type : string       // "Bool" | "Int" | "Real" | <custom type>
        - priority : string   // (not used)
        - reading  : string   // English reading of the symbol
        - shortinfo: string   // short description of the symbol
        - longinfo : string   // long description of the symbol
        - showOptimize : Bool // true if the optimize button should be shown for this symbol
        - view: string        // "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default
        - environmental: Bool // true if not declared in the decision vocabulary
        } ]
```

### URL: /eval

This page performs various inferences.

GET request :

```json
    - active : {                 // list of choices made by the user
        - <symbol> : string {
            - <atom/term> : string {
                - typ : string   // "Bool" | "Int" | "Real" | <custom type>
                - value: string  // value entered by the user
                }
            }
        }
    - code : string              // source code in FO(ID)
    - method : string            // name of the inference to be made:
                                 //   "propagate"   find propagated values
                                 //   "modelexpand" find a model of the theory
                                 //   "explain"     give an explanation for a propagated value
                                 //   "minimize"    find a model that minimizes a term
                                 //   "abstract"    find abstract representations of all models

    - expanded : [string]        // list of symbols in expanded view
    - value : string             // for explain: string of propagated value to be explained, preceded by '~' if negated
```

GET response :

```json
    - ' Global' : {             // with a leading space to avoid conflict with symbols
        - env_dec: Bool         // true if the theory separates environmental/decision variables
    }
    - <symbol> : string {
        - '__rank' : integer    // rank of the symbol, per informational relevance
        - <atom/term> : string {
            - typ : string      // "Bool" | "Int" | "Real" | <custom type>
            - environmental : Bool // True if atom/term does not contain a decision variable
            - value : string    // representation of the value of the atom/term, if any
            - values : []       // list of possible values for the atom/term (from its type)
            - status : string   // UNKNOWN     : unknown value
                                // GIVEN       : given by the user
                                // ENV_UNIV    : immediate consequence of the environmental theory
                                // UNIVERSAL   : immediate consequence of the theory
                                // ENV_CONSQ   : value propagated from inputs and environmental theory
                                // CONSEQUENCE : value obtained by propagation of inputs
                                // EXPANDED    : value obtained by model expansion
            - relevant: Bool
            - reading : string  // English reading of the atom/term
            - normal : Bool     // false if to be shown in expanded view only
            }
        }
    - '*laws*' : [
        law : string            // laws used to obtain the value to be explained
    ]
```








