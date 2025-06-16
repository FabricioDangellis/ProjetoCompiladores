import ply.lex as lex

errors = []

reserved = {
    'some': 'SOME', 'only': 'ONLY', 'all': 'ALL', 'value': 'VALUE',
    'min': 'MIN', 'max': 'MAX', 'exactly': 'EXACTLY', 'that': 'THAT',
    'not': 'NOT', 'and': 'AND', 'or': 'OR',
    'Class:': 'CLASS', 'EquivalentTo:': 'EQUIVALENTTO', 'Individuals:': 'INDIVIDUALS',
    'SubClassOf:': 'SUBCLASSOF', 'DisjointClasses:': 'DISJOINTCLASSES'
}

VALID_TYPES = [
    "owl:rational", "owl:real", "rdf:langString", "rdf:PlainLiteral",
    "rdf:XMLLiteral", "rdfs:Literal", "xsd:anyURI", "xsd:base64Binary",
    "xsd:boolean", "xsd:byte", "xsd:dateTime", "xsd:dateTimeStamp",
    "xsd:decimal", "xsd:double", "xsd:float", "xsd:hexBinary", "xsd:int",
    "xsd:integer", "xsd:language", "xsd:long", "xsd:Name", "xsd:NCName",
    "xsd:negativeInteger", "xsd:NMTOKEN", "xsd:nonNegativeInteger",
    "xsd:nonPositiveInteger", "xsd:normalizedString", "xsd:positiveInteger",
    "xsd:short", "xsd:string", "xsd:token", "xsd:unsignedByte", "xsd:unsignedInt",
    "xsd:unsignedLong", "xsd:unsignedShort"
]

tokens = [
    'KEYWORD','INDIVIDUAL_NAME', 'CLASS_ID', 'PROPERTY_ID', 'CARDINALITY',
    'DATATYPE', 'OPEN_BRACKET', 'CLOSE_BRACKET', 'OPEN_CURLY', 'CLOSE_CURLY',
    'OPEN_PAREN', 'CLOSE_PAREN', 'LESS_THAN', 'GREATER_THAN', 'COMMA', 'EQUAL'
] + list(reserved.values())

t_OPEN_BRACKET   = r'\['
t_CLOSE_BRACKET  = r'\]'
t_OPEN_CURLY     = r'\{'
t_CLOSE_CURLY    = r'\}'
t_OPEN_PAREN     = r'\('
t_CLOSE_PAREN    = r'\)'
t_LESS_THAN      = r'<'
t_GREATER_THAN   = r'>'
t_EQUAL          = r'='
t_COMMA          = r','

def t_KEYWORD(t):
    r'(some|only|all|value|min|max|exactly|that|not|and|or|Class:|EquivalentTo:|Individuals:|SubClassOf:|DisjointClasses:)'
    t.type = reserved[t.value]
    return t

def t_DATATYPE(t):
    r'(xsd|owl|rdf|rdfs):[a-zA-Z]+(?:[a-zA-Z0-9]*)?'
    if t.value in VALID_TYPES:
        return t
    else:
        errors.append(f"Erro Léxico: Tipo inválido '{t.value}' na linha {t.lineno}.")
        t.lexer.skip(1)

def t_INDIVIDUAL_NAME(t):
    r'[A-Z][a-zA-Z]*[0-9]+'
    return t

def t_CLASS_ID(t):
    r'[A-Z][a-zA-Z]*(?:_[A-Z][a-zA-Z]*)*'
    return t

def t_PROPERTY_ID(t):
    r'(has[A-Z][a-zA-Z]*)|(is[A-Z][a-zA-Z]*Of)|([a-z][a-zA-Z]*)'
    return t

def t_CARDINALITY(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# Atualizar contagem de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t'

def t_error(t):
    errors.append(f"Erro Léxico: Caractere inválido '{t.value[0]}' na linha {t.lineno}.")
    t.lexer.skip(1)

def build_lexer():
    lexer = lex.lex()
    lexer.errors = errors
    return lexer
