from lexical_analyzer import build_lexer, errors as lex_errors
from parser import build_parser, syntax_errors, classifications
from semantic_analyzer import SemanticAnalyzer

def run_lexical_analysis(code):
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

def run_syntactic_analysis(code):
    lexer = build_lexer()
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

def run_semantic_analysis(code):
    semantic = SemanticAnalyzer(code)
    classified_props, semantic_errors = semantic.analyze()

    print("\n==== CLASSIFICAÇÃO DAS PROPRIEDADES ====")
    if classified_props:
        for item in classified_props:
            print(item)
    else:
        print("Nenhuma propriedade classificada.")

    print("\n======= ERROS SEMÂNTICOS ========")
    if semantic_errors:
        for err in semantic_errors:
            print(err)
    else:
        print("Nenhum erro semântico encontrado.")


def show_menu(code):
    while True:
        print("\n======= MENU DE ANÁLISE =======")
        print("1 - Análise Léxica")
        print("2 - Análise Sintática")
        print("3 - Análise Semântica")
        print("4 - Sair")
        option = input("Escolha uma opção: ").strip()

        if option == '1':
            run_lexical_analysis(code)
        elif option == '2':
            run_syntactic_analysis(code)
        elif option == '3':
            run_semantic_analysis(code)
        elif option == '4':
            print("Encerrando o analisador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    path = input("Digite o caminho do arquivo OWL: ")

    try:
        with open(path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Arquivo '{path}' não encontrado.")
        exit(1)

    show_menu(code)
