import ply.yacc as yacc
from lexical_analyzer import tokens

#syntax_errors, onde armazenamos erros sintáticos com suas mensagens
#classifications, que guarda a classificação de cada classe encontrada no código

syntax_errors = []
classifications = []

#registrar quais características uma classe tem
flags = {
    'defined': False, 
    'closure': False,
    'enumerated': False,
    'nested': False,
    'covered': False
}

current_class = None

def mark_flag(name):
    if name in flags:
        flags[name] = True

def reset_flags():
    for key in flags:
        flags[key] = False

def get_classification():
    types = []
    if flags['defined']:
        types.append('Definida')
    else:
        types.append('Primitiva')
    if flags['closure']:
        types.append('Fechada')
    if flags['enumerated']:
        types.append('Enumerada')
    if flags['nested']:
        types.append('Aninhada')
    if flags['covered']:
        types.append('Coberta')
    return types

# ---------------------- GRAMÁTICA ------------------------

#define o ponto de entrada do código
def p_program(p):
    'program : classes'
    pass

#aceita uma única classe ou várias declarações de classe
def p_classes(p):
    '''classes : class_decl
               | class_decl classes'''
    pass

def p_class_primitive(p):
    'class_decl : CLASS CLASS_ID subclass_section disjoint_section individuals_section'
    global current_class
    current_class = p[2]
    flags['defined'] = False
    classifications.append((current_class, get_classification()))
    reset_flags()

def p_class_defined(p):
    'class_decl : CLASS CLASS_ID equivalentto_section disjoint_section individuals_section'
    global current_class
    current_class = p[2]
    flags['defined'] = True
    classifications.append((current_class, get_classification()))
    reset_flags()

def p_subclass_section(p):
    'subclass_section : SUBCLASSOF expression_list'
    pass

def p_expression_list(p):
    '''expression_list : expression
                       | expression COMMA expression_list'''
    pass

#Ela cobre todos os tipos de expressões possíveis, como expressões 
# simples, expressões com cardinalidade, expressões com fechamento, 
# e também expressões compostas com AND, OR, ou parênteses.
def p_expression(p):
    '''expression : simple_expression
                  | cardinality_expression
                  | comparison_expression
                  | closure_expression
                  | nested_expression
                  | OPEN_PAREN expression_list CLOSE_PAREN
                  | CLASS_ID
                  | CLASS_ID AND expression
                  | CLASS_ID AND expression_list
                  | expression AND expression'''
    pass

#trata expressões simples com some
def p_simple_expression(p):
    '''simple_expression : PROPERTY_ID SOME CLASS_ID
                         | PROPERTY_ID SOME DATATYPE'''
    mark_flag('nested')

#reconhece min, max, exactly com datatypes ou classes
def p_cardinality_expression(p):
    '''cardinality_expression : PROPERTY_ID MIN CARDINALITY CLASS_ID
                              | PROPERTY_ID MIN CARDINALITY DATATYPE
                              | PROPERTY_ID MAX CARDINALITY CLASS_ID
                              | PROPERTY_ID MAX CARDINALITY DATATYPE
                              | PROPERTY_ID EXACTLY CARDINALITY CLASS_ID
                              | PROPERTY_ID EXACTLY CARDINALITY DATATYPE'''
    mark_flag('nested')

#entende comparações como [< 400]
def p_comparison_expression(p):
    '''comparison_expression : PROPERTY_ID SOME DATATYPE OPEN_BRACKET GREATER_THAN EQUAL CARDINALITY CLOSE_BRACKET
                             | PROPERTY_ID SOME DATATYPE OPEN_BRACKET LESS_THAN CARDINALITY CLOSE_BRACKET
                             | PROPERTY_ID SOME DATATYPE OPEN_BRACKET LESS_THAN EQUAL CARDINALITY CLOSE_BRACKET'''
    mark_flag('nested')

#trata axiomas de fechamento com only
def p_closure_expression(p):
    'closure_expression : PROPERTY_ID ONLY OPEN_PAREN covered_expr CLOSE_PAREN'
    mark_flag('closure')
    mark_flag('covered')

#dentifica expressões aninhadas, como (hasSpiciness value Hot1)
def p_nested_expression(p):
    '''nested_expression : OPEN_PAREN PROPERTY_ID SOME CLASS_ID CLOSE_PAREN
                         | OPEN_PAREN PROPERTY_ID SOME DATATYPE CLOSE_PAREN
                         | OPEN_PAREN PROPERTY_ID SOME DATATYPE OPEN_BRACKET GREATER_THAN EQUAL CARDINALITY CLOSE_BRACKET CLOSE_PAREN
                         | OPEN_PAREN PROPERTY_ID SOME OPEN_PAREN PROPERTY_ID VALUE individual CLOSE_PAREN CLOSE_PAREN'''
    mark_flag('nested')

# qualquer indivíduo pertencente à classe mãe precisa também estar dentro de alguma classe filha
def p_covered_expr(p):
    '''covered_expr : CLASS_ID
                    | CLASS_ID OR CLASS_ID
                    | CLASS_ID OR CLASS_ID OR CLASS_ID
                    | CLASS_ID OR CLASS_ID OR CLASS_ID OR CLASS_ID'''
    mark_flag('covered')

#tratam os indivíduos, incluindo nomes de instâncias e listas de nomes, 
# além das seções DisjointClasses e Individuals.
def p_individual(p):
    '''individual : CLASS_ID
                  | INDIVIDUAL_NAME'''
    pass

#enumeração
def p_equivalentto_enum(p):
    'equivalentto_section : EQUIVALENTTO OPEN_CURLY INDIVIDUAL_NAME COMMA INDIVIDUAL_NAME COMMA INDIVIDUAL_NAME CLOSE_CURLY'
    mark_flag('enumerated')

def p_equivalentto_defined(p):
    'equivalentto_section : EQUIVALENTTO expression_list'
    mark_flag('defined')

def p_equivalentto_covered(p):
    'equivalentto_section : EQUIVALENTTO CLASS_ID OR CLASS_ID OR CLASS_ID'
    mark_flag('covered')
    mark_flag('defined')

def p_disjoint_section(p):
    '''disjoint_section : DISJOINTCLASSES disjoint_list
                        | empty'''

def p_disjoint_list(p):
    '''disjoint_list : CLASS_ID
                     | CLASS_ID COMMA disjoint_list'''
    pass

def p_individuals_section(p):
    '''individuals_section : INDIVIDUALS individual_list
                           | empty'''

def p_individual_list(p):
    '''individual_list : INDIVIDUAL_NAME
                       | INDIVIDUAL_NAME COMMA individual_list'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        syntax_errors.append(f"Erro Sintático na linha {p.lineno}: token inesperado '{p.value}'. Dica: verifique se a estrutura da classe está correta.")
    else:
        syntax_errors.append("Erro Sintático: fim inesperado do arquivo. Dica: verifique se todas as classes estão completas.")

def build_parser():
    return yacc.yacc()
