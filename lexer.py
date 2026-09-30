def lexer(codigo):
    tokens = []
    i = 0
    n = len(codigo)

    while i < n:
        caracter = codigo[i]

        
        if caracter.isspace():
            i += 1

        
        elif caracter.isdigit() or (caracter == '.' and i + 1 < n and codigo[i + 1].isdigit()):
            numero = ""
            while i < n and codigo[i].isdigit():
                numero += codigo[i]
                i += 1
            if i < n and codigo[i] == '.':
                numero += '.'
                i += 1
                while i < n and codigo[i].isdigit():
                    numero += codigo[i]
                    i += 1
            tokens.append(("numero", numero))

        
        elif caracter.isalpha() or caracter == "_":
            identificador = ""
            while i < n and (codigo[i].isalnum() or codigo[i] == "_"):
                identificador += codigo[i]
                i += 1
            tokens.append(("id", identificador))

        
        elif caracter in "+-*/%=()":
            tokens.append((caracter, caracter))
            i += 1

        
        else:
            i += 1

    return tokens
