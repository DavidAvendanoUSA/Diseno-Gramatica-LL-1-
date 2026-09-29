# GRAMÁTICA LL(1)

Un compilador simple que implementa un analizador léxico, sintáctico y semántico para evaluar expresiones matemáticas con soporte para funciones trigonométricas.

---

## Requisitos y Ejecución

**Requisitos:** Python 3 (utiliza librerías estándar `sys` y `math`, no requiere instalar paquetes adicionales con pip).

- Clonar el repositorio en el dispositivo
  ```bash
  git clone https://github.com/DavidAvendanoUSA/Diseno-Gramatica-LL-1-
  ```
- Cambiar el directorio a la carpeta donde se descargó el repositorio
  ```bash
  cd "ruta_carpeta"
  ```
- Ejecutar pasando como argumento el archivo de prueba (por ejemplo, los archivos en `gramatica/`):
  ```bash
  python main.py gramatica/ll1_prueba_1.txt
  ```

- **Resultados de pruebas:**

  - PRUEBA 1:
    <img width="1126" height="639" alt="image" src="https://github.com/user-attachments/assets/72d59d77-3ee9-4773-a12a-7ddffb6e31c0" />

  - PRUEBA 2:
    <img width="1128" height="641" alt="image" src="https://github.com/user-attachments/assets/63e680ea-4989-4669-97b3-8148418ffd21" />
    
  - PRUEBA 3:
    <img width="1127" height="648" alt="image" src="https://github.com/user-attachments/assets/10a95240-e425-4529-aa34-4cf9b4371261" />

---

## GRAMÁTICA *gramatica.py*

Define formalmente las reglas sintácticas del lenguaje en forma de diccionario.

**Estructura:**
```
Programa → Asignacion
Asignacion → id = Expresion
Expresion → Termino ExpresionPrim
ExpresionPrim → + Termino ExpresionPrim | - Termino ExpresionPrim | ε
Termino → Factor TerminoPrim
TerminoPrim → * Factor TerminoPrim | / Factor TerminoPrim | % Factor TerminoPrim | ε
Factor → numero | id | abs(Expresion) | sin(Expresion) | cos(Expresion) | tan(Expresion) | (Expresion)
```

**Características:**
- Define la precedencia de operadores: `+` y `-` tienen menor precedencia que `*`, `/` y `%`
- Permite funciones trigonométricas: `abs()`, `sin()`, `cos()`, `tan()`
- Soporta paréntesis para agrupar expresiones
- Utiliza `ε` (epsilon) para representar producciones vacías

---

## LEXER *lexer.py*

Analiza el código fuente carácter por carácter y genera una lista de tokens.

**Función principal:** `lexer(codigo)`

**Proceso:**
1. Ignora espacios en blanco
2. Reconoce números: cadenas de dígitos consecutivos → token `("numero", "valor")`
3. Reconoce identificadores y palabras clave: inician con letra o `_` → token `("id", "nombre")`
4. Reconoce operadores y símbolos: `+ - * / % = ( )` → token `(símbolo, símbolo)`
5. Descarta caracteres desconocidos

**Ejemplo:**
```
Entrada: x = 2 + 3
Salida: [("id", "x"), ("=", "="), ("numero", "2"), ("+", "+"), ("numero", "3")]
```

---

## PARSER *parser.py*

Realiza un análisis sintáctico descendente recursivo (recursive descent).

**Características:**
- **Left-to-right:** lee tokens de izquierda a derecha
- **Leftmost derivation:** expande el símbolo más a la izquierda
- **LL(1):** solo mira 1 token adelante para decidir qué producción usar

**Estructura:**
1. Una función por cada no-terminal (Programa, Asignacion, Expresion, etc.)
2. Cada función devuelve una tupla `(nombre_nodo, [hijos])`
3. Las hojas son los tokens del lexer
4. Cuando hay `ε` (epsilon), devolvemos tupla con lista vacía

**Métodos principales:**
- `token_actual()`: devuelve el token actual sin consumirlo
- `comer(tipo_esperado)`: valida y consume un token del tipo esperado
- `programa()`: punto de entrada del parser
- `asignacion()`, `expresion()`, `termino()`, `factor()`: funciones recursivas para cada regla gramatical

**Ejemplo de ejecución:**
```
Entrada: x = 2 - 3
Tokens: [("id", "x"), ("=", "="), ("numero", "2"), ("-", "-"), ("numero", "3")]

1. programa()
   └─ asignacion()
      └─ comer("id") → ("id", "x") ✓
      └─ comer("=") → ("=", "=") ✓
      └─ expresion()
         └─ termino()
            └─ factor()
               └─ comer("numero") → ("numero", "2") ✓
            └─ termino_prim() → ("TerminoPrim", []) porque próximo es "-"
         └─ expresion_prim()
            ├─ comer("-") → ("-", "-") ✓
            ├─ termino()
            │  └─ factor()
            │     └─ comer("numero") → ("numero", "3") ✓
            │  └─ termino_prim() → ("TerminoPrim", [])
            └─ expresion_prim() → ("ExpresionPrim", []) porque no hay más tokens

Resultado AST:
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

**Manejo de errores:**
- Lanza `ParseError` si encuentra tokens inesperados
- Muestra el token problemático y su posición en la entrada
- Valida que se consuman todos los tokens al finalizar

---

## SEMÁNTICA *semantica.py*

Evalúa el árbol de análisis sintáctico (AST) generado por el parser y ejecuta las operaciones.

**Estructura:**
- Tabla de símbolos (`env`): diccionario que almacena las variables y sus valores
- Funciones soportadas: `{"abs": abs, "sin": math.sin, "cos": math.cos, "tan": math.tan}`

**Funciones principales:**
- `calcular(op, a, b)`: ejecuta operaciones aritméticas (`+`, `-`, `*`, `/`, `%`)
  - Detecta división por cero y lanza excepción
- `visitar(nodo, env)`: recorre el AST y despacha a la función visitadora correspondiente
- `v_Programa(h, env)`: procesa el nodo raíz
- `v_Asignacion(h, env)`: asigna un valor a una variable
- `v_Expresion(h, env)` y `v_Termino(h, env)`: evalúan expresiones combinando operandos y operadores
- `v_prim(nodo, acum, env)`: maneja recursivamente las operaciones acumuladas (para `+`, `-`, `*`, `/`, `%`)
- `v_Factor(h, env)`: evalúa factores (números, variables, funciones, expresiones entre paréntesis)

**Diccionario VISITORS:**
Mapea nombres de nodos a sus funciones visitadoras para un despacho dinámico.

**Validaciones:**
- Detecta variables no definidas
- Valida divisiones por cero
- Maneja desbordamientos en operaciones

---

## MAIN *main.py*

Orquesta el pipeline completo: lectura de archivo → lexer → parser → semántica.

**Flujo:**
1. Lee el archivo de entrada (pasado como argumento)
2. Ejecuta el lexer para obtener tokens
3. Ejecuta el parser para construir el AST
4. Ejecuta el análisis semántico para evaluar la expresión
5. Muestra tokens, AST, resultado final y variables definidas

**Manejo de errores:**
- `ParseError`: errores sintácticos del parser
- `ZeroDivisionError`: división por cero
- `NameError`: variable no definida
- `OverflowError`: desbordamiento en operaciones

---

## ARCHIVOS DE PRUEBA *gramatica/*

- **ll1_prueba_1.txt:** Prueba válida con función trigonométrica
  ```
  x = 2 + 3 * sin(45)
  ```

- **ll1_prueba_2.txt:** Prueba que genera error semántico (división por cero)
  ```
  x = 10 / sin(0)
  ```

- **ll1_prueba_3.txt:** Prueba que genera error sintáctico
  ```
  x = 2 + * sin(45)
  ```

---

## FLUJO COMPLETO DEL COMPILADOR

```
Código fuente
    ↓
[LEXER] → Tokens
    ↓
[PARSER] → AST (Árbol de Análisis Sintáctico)
    ↓
[SEMÁNTICA] → Resultado + Tabla de símbolos
```

Cada etapa valida su entrada y reporta errores específicos del tipo que procesa.

---

## INTEGRANTES
- David Avendaño
- Laura Niño
- Brayan Paredes
