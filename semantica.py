import math

FUNCIONES = {"abs": abs, "sin": math.sin, "cos": math.cos, "tan": math.tan, "arctan": math.atan}

def calcular(op, a, b):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op in ("/", "%"):
        if b == 0:
            raise ZeroDivisionError("División por cero")
        return a / b if op == "/" else a % b

def visitar(nodo, env):
    nombre, hijos = nodo
    return VISITORS[nombre](hijos, env)

def v_Programa(h, env):
    return visitar(h[0], env)

def v_Asignacion(h, env):
    valor = visitar(h[2], env)
    env[h[0][1]] = valor              # h[0] es el token ("id", "x")
    return valor

def v_Expresion(h, env):              # Termino ExpresionPrim
    return v_prim(h[1], visitar(h[0], env), env)

def v_Termino(h, env):                # Factor TerminoPrim
    return v_prim(h[1], visitar(h[0], env), env)

def v_prim(nodo, acum, env):          # sirve para ExpresionPrim y TerminoPrim
    _, h = nodo
    if not h:                         # ε: no hay más operaciones
        return acum
    op, operando, resto = h
    acum = calcular(op[0], acum, visitar(operando, env))
    return v_prim(resto, acum, env)

def v_Factor(h, env):
    tipo, valor = h[0]
    if tipo == "-":                       # - Factor (unario negativo)
        return -visitar(h[1], env)
    if len(h) == 4:                       # función: nombre ( Expresion )
        return FUNCIONES[valor](visitar(h[2], env))
    if tipo == "numero":
        return float(valor) if "." in valor else int(valor)
    if tipo == "id":
        if valor not in env:
            raise NameError(f"Variable no definida: {valor}")
        return env[valor]
    if tipo == "(":                       # ( Expresion )
        return visitar(h[1], env)

VISITORS = {
    "Programa": v_Programa,
    "Asignacion": v_Asignacion,
    "Expresion": v_Expresion,
    "Termino": v_Termino,
    "Factor": v_Factor,
}
