from ply import lex

tokens = (
    'COMMA',
    'INT',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'LPAREN',
    'RPAREN',
    'UMINUS',  # unary minus
    'COS',
    'SIN',
    'LOG',
    'EXP',
    'SQRT',
    'PI',
    'EQUAL',
    'VARIABLE',
    'POLY',
    'EVAL',  
    )

t_COMMA = r','
t_INT = r'(0|[1-9][0-9]*)'
t_FLOAT = r'(0|[1-9][0-9]*)\.[0-9]+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VARIABLE = r'[a-z][\w]*'
t_EQUAL = r'='
t_ignore = ' '

def t_SIN(t):
    r'sin'
    return t

def t_COS(t):
    r'cos'
    return t

def t_LOG(t):
    r'log'
    return t

def t_EXP(t):
    r'exp'
    return t

def t_SQRT(t):
    r'sqrt'
    return t

def t_PI(t):
    r'pi'
    return t

def t_POLY(t):
    r'poly'
    return t

def t_EVAL(t):
    r'eval'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__" :
    # data = "150 - (10 / (3 * (3 + 2))) - 034 + 100001 + 4 + 0"
    data = 'eval(x = 1, 4 * x^2 + 5 * x + 2)'
    lexer.input(data)
    for tok in lexer :
        print(tok)