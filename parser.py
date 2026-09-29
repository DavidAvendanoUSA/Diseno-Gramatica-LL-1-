from lexer import lexer
from parser import Parser, ParseError


def main():
    # Ejemplo simple
    codigo = "x = 2 + 3 * sin(45)"
    
    print(f"Código fuente: {codigo}\n")
    
    try:
        # Lexer
        tokens = lexer(codigo)
        print(f"Tokens: {tokens}\n")
        
        # Parser
        parser = Parser(tokens)
        ast = parser.parsear()
        
        print("AST (Árbol de Análisis Sintáctico):")
        print(ast)
        
    except ParseError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
