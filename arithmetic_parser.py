import logging

from arithmetic_expressions import *
from arithmetic_lexer import tokens
from ply import yacc

log = logging.getLogger()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),            # Unary minus operator
)

def p_statement_expression(p):
    '''
    statement : assignment 
                | expression
                | polynomial
                | evaluation
    '''
    p[0] = p[1]

def p_evaluation_expression(p):
    '''
    evaluation : EVAL LPAREN VARIABLE EQUAL expression COMMA expression RPAREN
    '''
    p[0] = Litteral(PolyExpr(var = p[3], expr = p[7]).eval(value = p[5]))

def p_polynomial_expression(p):
    '''
    polynomial : POLY LPAREN VARIABLE COMMA expression RPAREN
    '''
    p[0] = PolyExpr(var = p[3], expr = p[5])

def p_assignment_expression(p):
    '''
    assignment : VARIABLE EQUAL expression
    '''
    var = Variable(name = p[1], value = p[3])

def p_other_math_expr(p):
    '''
    expression : SIN LPAREN expression RPAREN
               | COS LPAREN expression RPAREN
               | LOG LPAREN expression RPAREN
               | EXP LPAREN expression RPAREN 
               | SQRT LPAREN expression RPAREN
    '''
    if p[1] == 'sin':
        p[0] = SinExpr(p[3])
    if p[1] == 'cos':
        p[0] = CosExpr(p[3])
    if p[1] == 'log':
        p[0] = LogExpr(p[3])
    if p[1] == 'exp':
        p[0] = ExpExpr(p[3])
    if p[1] == 'sqrt':
        p[0] = SqrtExpr(p[3])

def p_artith_expression(p):
    '''
    expression : expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression
           | expression POWER expression
           | LPAREN expression RPAREN
           | MINUS expression %prec UMINUS
    '''
    if len(p) == 4: # Binary Operation
        if p[1] == '(' and p[3] == ')':
            p[0] = p[2]
        if p[2] == '+':
            p[0] = AddExpr(p[1],p[3])
        if p[2] == '-':
            p[0] = SubExpr(p[1],p[3])
        if p[2] == '*':
            p[0] = MulExpr(p[1],p[3])
        if p[2] == '/':
            p[0] = DivExpr(p[1],p[3])
        if p[2] == '^':
            p[0] = PowExpr(p[1], p[3])
    
    if len(p) == 3: # Unary Operation
        p[0] = OppExpr(p[2])
            
def p_int_expression(p):
    'expression : INT'
    p[0] = Litteral(int(p[1]))

def p_float_expression(p):
    'expression : FLOAT'
    p[0] = Litteral(float(p[1]))

def p_constant_expression(p):
    'expression : PI'
    p[0] = Litteral(math.pi)
    
def p_variable_expression(p):
    '''
    expression : VARIABLE
    '''
    try:
        p[0] = Litteral(Variable.vars[p[1]].eval())
    except KeyError:
        p[0] = Variable(name = p[1])
    except AttributeError:
        p[0] = Variable(name = p[1])
    except Exception as e:
        raise e

def p_error(p):
    print(f"Syntax error in input: {p}")

parser = yacc.yacc(debug=True)

def assert_expr(expr: str, expected):
    parsed_expr = parser.parse(expr, debug=log)
    expr_value = parsed_expr.eval()
    assert expr_value == expected

if __name__ == "__main__":
    eval = parser.parse('eval(x = 1, 4 * x^2 + 5 * x + 2)')
    assert eval.eval() == 11
    
    poly = parser.parse('poly(x, x+2)')
    assert str(poly) == 'Poly(x, (x + 2))'

    assert_expr('sqrt(4)', 2)
    assert_expr('cos(pi/2)', math.cos(math.pi/2))
    assert_expr('sin(0)', 0)
    assert_expr('log(1)', 0)
    assert_expr('exp(0)', 1)
    assert_expr('2^(-(5 - 4))', 0.5)
    assert_expr('3.5*2 + 2.5/0.5', 12.0)

    parser.parse('this_is_a_variable123=(3+2)')
    assert Variable.vars['this_is_a_variable123'].eval() == (3+2)

    parser.parse('x=(3 * 4 - 2)')
    assert Variable.vars['x'].eval() == 10
    parser.parse('y=x-2')
    assert Variable.vars['y'].eval() == 8

    parser.parse('z + 3') # error: variable was not initialized before

    assert_expr('(((3*2) + (7/1)) - (4+8))', (((3*2) + (7/1)) - (4+8)))
    assert_expr('(2+(3*1))', (2+(3*1)))
    assert_expr('((2 + 7)*(4-2))', ((2 + 7)*(4-2)))
    assert_expr('2 + 5 - 1 * (6/2)', 2 + 5 - 1 * (6/2))
    assert_expr('4/2*3', 6)
    assert_expr('4-2-2', 4-2-2)
    assert_expr('4/(2*3)', 4/(2*3))
    assert_expr('(4/2)*3', (4/2)*3)
    assert_expr('3 + -(-(-4)*2)', 3 + -(-(-4)*2))
    assert_expr('(3 + (-((-(-4))*2)))', (3 + (-((-(-4))*2))))

    print("All assertions passed!")
    Variable.vars = dict() # reset vars
    
    print("Write your expressions:")
    while(True): # Calculator
        data = input()
        result = parser.parse(data)
        if result:
            print("=>", result.eval())

