class ParseError(Exception):
    """Excepción para errores de parsing"""
    pass


class Parser:
    def __init__(self, tokens):
        """
        Inicializa el parser con una lista de tokens.
        
        Args:
            tokens: lista de tuplas (tipo, valor) del lexer
        """
        self.tokens = tokens
        self.pos = 0  # Posición actual en la lista de tokens
    
    def token_actual(self):
        """Retorna el token actual sin comerlo"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def comer(self, tipo_esperado):
        """
        come un token si coincide con el tipo esperado.
        
        Args:
            tipo_esperado: tipo de token que esperamos (ej: "+", "id", "numero")
        
        Returns:
            La tupla del token consumido
        
        Raises:
            ParseError: si el token no coincide
        """
        token = self.token_actual()
        
        if token is None:
            raise ParseError(
                f"Se esperaba '{tipo_esperado}' pero se encontró el fin del archivo :0"
            )
        
        tipo_actual, valor = token
        
        if tipo_actual != tipo_esperado:
            raise ParseError(
                f"Se esperaba '{tipo_esperado}' pero se encontró '{tipo_actual}' con valor '{valor}'"
            )
        
        self.pos += 1
        return token
    
    # ============== REGLAS DEL PARSER ==============
    # Cada función corresponde a un no terminal de la gramática
    
    def programa(self):
        """
        Programa → Asignacion
        
        Returns:
            ("Programa", [asignacion_node])
        """
        asignacion = self.asignacion()
        return ("Programa", [asignacion])
    
    def asignacion(self):
        """
        Asignacion → id = Expresion
        
        Returns:
            ("Asignacion", [id_token, =_token, expresion_node])
        """
        id_token = self.comer("id")
        igual_token = self.comer("=")
        expresion = self.expresion()
        
        return ("Asignacion", [id_token, igual_token, expresion])
    
    def expresion(self):
        """
        Expresion → Termino ExpresionPrim
        
        Esto evalúa sumas y restas (de menor precedencia).
        
        Returns:
            ("Expresion", [termino_node, expresion_prim_node])
        """
        termino = self.termino()
        expresion_prim = self.expresion_prim()
        
        return ("Expresion", [termino, expresion_prim])
    
    def expresion_prim(self):
        """
        ExpresionPrim → + Termino ExpresionPrim
                    | - Termino ExpresionPrim
                    | ε (epsilon - nada)
        
        Maneja las operaciones de suma y resta iterativas.
        
        Returns:
            ("ExpresionPrim", [...]) con operador, termino y siguiente prim
            O ("ExpresionPrim", []) si es epsilon
        """
        token = self.token_actual()
        
        # Si es + o -, se come y continua recursivamente
        if token and token[0] in ["+", "-"]:
            operador_token = self.comer(token[0])
            termino = self.termino()
            expresion_prim = self.expresion_prim()
            
            return ("ExpresionPrim", [operador_token, termino, expresion_prim])
        
        # Si no es + ni -, es epsilon (lista vacía)
        else:
            return ("ExpresionPrim", [])
    
    def termino(self):
        """
        Termino → Factor TerminoPrim
        
        Esto evalúa multiplicaciones y divisiones (mayor precedencia).
        
        Returns:
            ("Termino", [factor_node, termino_prim_node])
        """
        factor = self.factor()
        termino_prim = self.termino_prim()
        
        return ("Termino", [factor, termino_prim])
    
    def termino_prim(self):
        """
        TerminoPrim → * Factor TerminoPrim
                    | / Factor TerminoPrim
                    | % Factor TerminoPrim
                    | ε (epsilon - nada)
        
        Maneja las operaciones de multiplicación, división y módulo iterativas.
        
        Returns:
            ("TerminoPrim", [...]) con operador, factor y siguiente prim
            O ("TerminoPrim", []) si es epsilon
        """
        token = self.token_actual()
        
        if token and token[0] in ["*", "/", "%"]:
            operador_token = self.comer(token[0])
            factor = self.factor()
            termino_prim = self.termino_prim()
            
            return ("TerminoPrim", [operador_token, factor, termino_prim])
        
        else:
            return ("TerminoPrim", [])
    
    def factor(self):
        """
        Factor → numero
            | id
            | abs ( Expresion )
            | sin ( Expresion )
            | cos ( Expresion )
            | tan ( Expresion )
            | ( Expresion )
        
        Esto evalúa los elementos más básicos (números, variables, funciones).
        
        Returns:
            Tupla con la estructura según el tipo de factor
        """
        token = self.token_actual()
        
        if token is None:
            raise ParseError("Se esperaba Factor pero se encontró el fin del archivo")
        
        tipo, valor = token
        
        # Caso 1: Número literal
        if tipo == "numero":
            numero_token = self.comer("numero")
            return ("Factor", [numero_token])
        
        # Caso 2: Variable (id)
        elif tipo == "id":
            # Verificar si es una palabra clave (función trigonométrica)
            if valor in ["sin", "cos", "tan", "abs"]:
                # Es una función
                funcion_token = self.comer("id")
                paren_abierto = self.comer("(")
                expresion = self.expresion()
                paren_cerrado = self.comer(")")
                
                return ("Factor", [funcion_token, paren_abierto, expresion, paren_cerrado])
            else:
                # Es una variable normal
                id_token = self.comer("id")
                return ("Factor", [id_token])
        
        # Caso 3: Expresión entre paréntesis
        elif tipo == "(":
            paren_abierto = self.comer("(")
            expresion = self.expresion()
            paren_cerrado = self.comer(")")
            
            return ("Factor", [paren_abierto, expresion, paren_cerrado])
        
        # Caso 4: Menos unario (números o factores negativos)
        elif tipo == "-":
            menos_token = self.comer("-")
            factor_nodo = self.factor()
            return ("Factor", [menos_token, factor_nodo])
        
        else:
            raise ParseError(
                f"Se esperaba Factor (numero, id, signo '-' o paréntesis) pero se encontró '{tipo}' con valor '{valor}'"
            )
    
    def parsear(self):
        """
        Inicia el parsing del programa completo.
        
        Returns:
            El árbol de análisis sintáctico (AST)
        
        Raises:
            ParseError: si hay errores sintácticos
        """
        try:
            ast = self.programa()
            
            # Verificar que se consumieron todos los tokens
            if self.pos < len(self.tokens):
                raise ParseError(
                    f"Tokens extra inesperados :0  después de terminar el programa: {self.tokens[self.pos:]}"
                )
            
            return ast
        
        except ParseError as e:
            # Mostrar información del error
            token = self.token_actual()
            if token:
                print(f"Error en posición {self.pos}: {token}")
            print(f"Error: {e}")
            raise
