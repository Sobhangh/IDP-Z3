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
                - ct : Bool     // certainly true
                - cf : Bool     // certainly false
                }  
            }
        }
    - code : string
    - method : "propagate" | ""modelexpand" | "explain" | "minimize" | "abstract"
    - expanded : [string]  // for propagate
    - value : string // for explain: string of atom, preceded by '~' if negated

GET response for "propagate" :

    - <symbol> : { 
        - <atom> : {            // <symbol> and <atom> are string
            - typ : "Bool" | "Int" | "Real" | <custom type>
            - value : string    // representation of the value
            - values : []       // optional
            - ct : Bool         // for Bool
            - cf : Bool         // for Bool
            - reading : string  // optional
            - normal : Bool     // false if to be shown in expanded view only
            }
        } 









    