This file describes the web API.

### URL: /meta

This page returns general settings, and is expected to be deprecated.

POST request:

    - "code" : string

POST result:

    - title: string
    - symbols : [ {
        - idpname : string
        - type : string
        - priority : string
        - showOptimize : Bool
        - view: "normal" | "expanded"
        } ]

### URL: /eval

This page performs various inferences.

GET request :

    - active : {            // list of choices made by the user
        - <symbol> : {
            - <atom> : {
                - typ : "Bool" | "Int" | "Real" | <custom type>
                - value: string
                }
            }
        }
    - code : string
    - method : "propagate" | ""modelexpand" | "explain" | "minimize" | "abstract"
    - expanded : [string]
    - value : string // for explain: string of atom, preceded by '~' if negated

GET response :

    - ' Global' : {             // with a leading space to avoid conflict with symbols
        - env_dec: Bool         // true if we separate environmental/decision variables
        - env_done: Bool        // true if all relevant environmental variables are given
    }
    - <symbol> : {
        - <atom> : {            // <symbol> and <atom> are string
            - typ : "Bool" | "Int" | "Real" | <custom type>
            - environmental : Bool // True if not a decision variable
            - value : string    // representation of the value
            - values : []       // optional
            - status : string   // UNKNOWN, GIVEN, UNIVERSAL, ENV_CONSQ, CONSEQUENCE
            - relevant: Bool
            - ct : Bool         // DEPRECATED use value+status instead
            - cf : Bool         // DEPRECATED use value+status instead
            - reading : string  // optional
            - normal : Bool     // false if to be shown in expanded view only
            }
        }









