import sys
from lexer import lexer
from parser import Parser, ParseError
from semantica import visitar


def main():
    # Leer el archivo .txt pasado como segundo parámetro (sys.argv[1])
    if len(sys.argv) > 1:
        ruta_archivo = sys.argv[1]
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    else:
        print("Error: ruta inválida")
        return

    env = {}   # tabla de símbolos: guarda las variables

    print(f"Código fuente: {codigo}\n")

    try:
        tokens = lexer(codigo)
        print(f"Tokens: {tokens}\n")

        ast = Parser(tokens).parsear()
        print("AST (Árbol de Análisis Sintáctico):")
        print(ast)

        resultado = visitar(ast, env)
        print(f"\nResultado: {resultado}")
        print(f"Variables: {env}")

    except ParseError as e:
        print(f"Error de sintaxis: {e}")
    except (ZeroDivisionError, NameError, OverflowError) as e:
        print(f"Error semántico: {e}")


if __name__ == "__main__":
    main()
