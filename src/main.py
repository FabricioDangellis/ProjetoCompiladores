from lexical_analyzer import build_lexer, errors as lex_errors
from parser import build_parser, syntax_errors, classifications

if __name__ == '__main__':
    path = input("Digite o caminho do arquivo OWL: ")

    try:
        with open(path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Arquivo '{path}' não encontrado.")
        exit(1)

    lexer = build_lexer()
    lexer.input(code)

    print("\n====== TOKENS LÉXICOS ======")
    for token in iter(lexer.token, None):
        lineno = getattr(token, "lineno", "?")
        print(f"{token.type:<20} {token.value:<20} Linha: {lineno}")

    print("\n====== ERROS LÉXICOS ======")
    if lex_errors:
        for err in lex_errors:
            print(err)
    else:
        print("Nenhum erro léxico encontrado.")

    # Reinicializa o lexer para o parser
    lexer.input(code)

    parser = build_parser()
    parser.parse(code, lexer=lexer)

    print("\n====== ERROS SINTÁTICOS ======")
    if syntax_errors:
        for err in syntax_errors:
            print(err)
    else:
        print("Nenhum erro sintático encontrado.")

    print("\n====== CLASSIFICAÇÃO DAS CLASSES ======")
    for class_name, types in classifications:
        print(f"{class_name}: {' & '.join(types)}")
