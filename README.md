# GRAMÁTICA LL(1)

---

## ¿QUÉ ES?



---

## EJECUCIÓN

Requisitos: Python 3 (utiliza librerías estándar `sys` y `math`, no necesita paquetes adicionales).

- Clonar el repositorio en el dispositivo
  ```bash
  git clone https://github.com/DavidAvendanoUSA/Diseno-Gramatica-LL-1-
  ```
- Cambiar el directorio a la carpeta donde se descargó el repositorio
  ```bash
  cd "ruta_archivo"
  ```
- Ejecutar pasando como argumento el archivo de prueba (por ejemplo, los archivos en `gramatica/`):
  ```bash
  python main.py gramatica/ll1_prueba_1.txt
  ```


- PRUEBA 1:
  <img width="1126" height="639" alt="image" src="https://github.com/user-attachments/assets/72d59d77-3ee9-4773-a12a-7ddffb6e31c0" />

- PRUEBA 2:
  <img width="1128" height="641" alt="image" src="https://github.com/user-attachments/assets/63e680ea-4989-4669-97b3-8148418ffd21" />
  
- PRUEBA 3:
  <img width="1127" height="648" alt="image" src="https://github.com/user-attachments/assets/10a95240-e425-4529-aa34-4cf9b4371261" />

---

## GRAMÁTICA *gramatica.py*


---

## LEXER *lexer.py*



---

## PARSER *parser.py*

El parser es descendente recursivo.
  - Left-to-right: lee tokens de izquierda a derecha
  - Leftmost derivation: expande el símbolo más a la izquierda
  - 1: solo mira 1 token adelante para decidir qué producción usar

Estructura:
  1. Una función por cada no-terminal (Programa, Asignacion, Expresion, etc.)
  2. Cada función devuelve una tupla (nombre_nodo, [hijos])
  3. Las hojas son los tokens del lexer
  4. Cuando hay ε (epsilon), devolvemos tupla con lista vacía

Cómo funciona (ejemplo):
```
Entrada: x = 2 - 3
Tokens: [("id", "x"), ("=", "="), ("numero", "2"), ("-", "-"), ("numero", "3")]

1. programa()
   └─ asignacion()
      └─ consumir("id") → ("id", "x") ✓
      └─ consumir("=") → ("=", "=") ✓
      └─ expresion()
         └─ termino()
            └─ factor()
               └─ consumir("numero") → ("numero", "2") ✓
            └─ termino_prim() → ("TerminoPrim", []) porque próximo es "-"
         └─ expresion_prim()
            ├─ consumir("-") → ("-", "-") ✓
            ├─ termino()
            │  └─ factor()
            │     └─ consumir("numero") → ("numero", "3") ✓
            │  └─ termino_prim() → ("TerminoPrim", [])
            └─ expresion_prim() → ("ExpresionPrim", []) porque no hay más tokens

Resultado:
("Programa", [
  ("Asignacion", [
    ("id", "x"),
    ("=", "="),
    ("Expresion", [
      ("Termino", [
        ("Factor", [("numero", "2")]),
        ("TerminoPrim", [])
      ]),
      ("ExpresionPrim", [
        ("-", "-"),
        ("Termino", [
          ("Factor", [("numero", "3")]),
          ("TerminoPrim", [])
        ]),
        ("ExpresionPrim", [])
      ])
    ])
  ])
])
```

---

## SEMÁNTICA *semantica.py*



---

## MAIN *main.py*



---

## CÓDIGO FUENTE *ll1.txt*



---

## RELACIÓN ENTRE TODOS LOS ARCHIVOS &  CÓMO FUNCIONA


---

## INTEGRANTES
- David Avendaño
- Laura Niño
- Brayan Paredes
