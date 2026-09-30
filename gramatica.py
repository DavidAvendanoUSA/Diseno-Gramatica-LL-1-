GRAMATICA = {
    "Programa": [
        ["Asignacion"]
    ],

    "Asignacion": [
        ["id", "=", "Expresion"]
    ],

    "Expresion": [
        ["Termino", "ExpresionPrim"]
    ],

    "ExpresionPrim": [
        ["+", "Termino", "ExpresionPrim"],
        ["-", "Termino", "ExpresionPrim"],
        ["ε"]
    ],

    "Termino": [
        ["Factor", "TerminoPrim"]
    ],

    "TerminoPrim": [
        ["*", "Factor", "TerminoPrim"],
        ["/", "Factor", "TerminoPrim"],
        ["%", "Factor", "TerminoPrim"],
        ["ε"]
    ],

    "Factor": [
        ["numero"],
        ["id"],
        ["-", "Factor"],
        ["abs", "(", "Expresion", ")"],
        ["sin", "(", "Expresion", ")"],
        ["cos", "(", "Expresion", ")"],
        ["tan", "(", "Expresion", ")"],
        ["arctan", "(", "Expresion", ")"],
        ["(", "Expresion", ")"]
    ]
}
