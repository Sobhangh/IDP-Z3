This file describes the web API.

### URL: /run

This page returns the output of running an IDP program with a procedure block.

POST request:

```json
    - "code" : string         // source code in FO(ID)
```

POST result:

```json
    string                    // stdout of running the program
```

### URL: /meta

This page returns the list of symbols.

POST request:

```json
    - "code" : string         // source code in FO(ID)
```

POST result:

```json
    - symbols : [ {           // list of predicates/functions, each one corresponding to a box on the page
        - idpname : string    // name of the predicate/function in the FO(ID) vocabulary
        - type : string       // "Bool" | "Int" | "Real" | "Date" | <custom type>
        - priority : string   // (not used)
        - reading  : string   // English reading of the symbol
        - shortinfo: string   // short description of the symbol
        - longinfo : string   // long description of the symbol
        - showOptimize : Bool // true if the optimize button should be shown for this symbol
        - view: string        // "hidden" | "normal" | "expanded" whether the symbol box should show atoms that contain that symbol, by default
        - environmental: Bool // true if declared in environment vocabulary
        - values : [string]   // possible values for the symbol
        } ]
    - optionalPropagation: Bool // use propagation toggle button in the IC.
    - manualPropagation: Bool // deactivate automatic propagation in the IC.
    - optionalRelevance: Bool // use propagation toggle button in the IC.
    - manualRelevance: Bool   // deactivate automatic relevancy in the IC.
    - valueinfo : string // format identical to <symbol> in /eval response // information about the values for the symbols for the gui
    - laws : [(string,string)] // laws in the theory. First element is id, second is natural description.
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
                - status: string // GIVEN       : given by the user, fixed for now
                }
            }
        }
    - previous_active : {    // list of assignments from last full propagation
        - <symbol> : string {
            - <atom/term> : string {
                - typ : string   // "Bool" | "Int" | "Real" | <custom type>
                - value: string  // value entered by the user
                - status: string // UNKNOWN     : unknown value
                                 // GIVEN       : given by the user
                                 // DEFAULT     : part of a given default structure (only after meta call)
                                 // EXPANDED    : value obtained by model expansion (only after optimize / expand call)
                                 // UNIVERSAL   : immediate consequence of the theory
                                 // CONSEQUENCE : value obtained by propagation of inputs
                                 // ENV_CONSQ   : value obtained by propagation of inputs on environmental theory
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
    - value : string             // for explain: string of propagated atom to be explained,
                                 //    preceded by '~' if negated
    - field : string             // for propagate: string of the applied symbol
                                 //    for which the user wants to know
                                 //    the range of possible values
```

GET response :

```json
    - ' Global' : {             // with a leading space to avoid conflict with symbols
        - active: string        // list of entries made by the user
        - env_dec: Bool         // true if the theory separates environmental/decision variables
    }
    - <symbol> : string {
        - <atom/term> : string {
            - typ : string      // "Bool" | "Int" | "Real" | <custom type>
            - environmental : Bool // True if atom/term does not contain a decision variable
            - value : string    // representation of the value of the atom/term, if any
            - values : []       // list of possible values for the atom/term (from its type)
            - status : string   // UNKNOWN     : unknown value
                                // GIVEN       : given by the user
                                // DEFAULT     : part of a given default structure (only after meta call)
                                // EXPANDED    : value obtained by model expansion (only after optimize / expand call)
                                // UNIVERSAL   : immediate consequence of the theory
                                // CONSEQUENCE : value obtained by propagation of inputs
                                // ENV_CONSQ   : value obtained by propagation of inputs on environmental theory
            - relevant: Bool
            - reading : string  // English reading of the atom/term
            - normal : Bool     // false if to be shown in expanded view only
            - is_assignment : Bool // true if the atom assigns a value to a symbol
            }
        }
    - 'laws' : [
        law : string            // laws used to obtain the value to be explained
    ]
```








