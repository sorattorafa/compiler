 # ------------------------------------------------------------
 # calclex.py
 #
 # tokenizer for a simple expression evaluator for
 # numbers and +,-,*,/
 # ------------------------------------------------------------
import ply.lex as lex 

# Declare reserved words
reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'fim': 'FIM',
    'senão': 'SENAO',
    'repita': 'REPITA',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA',
    'até': 'ATE',
    'inteiro': 'INTEIRO',
    'flutuante': 'FLUTUANTE',
}
 
 # List of token names.   This is always required
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',  
    'EQUALS', 
    'NAME', 
    'NUMBER_FLOAT', 
    'ID', 
    'NOT_EQUAL',
    'GREATER_THAN',
    'GREATER_EQUAL',
    'LESS_THAN',
    'LESS_EQUAL',
    'ASSIGNMENT',
    # Logical
    'AND',
    'OR',
    'NOT',
    #SYMBOLS 
    'COLON',
    'COMMA',
]+ list(reserved.values())
 
 # Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS = r'='
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
 
 # A regular expression rule with some action code 
def t_ID(t):
    r'''[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]
    [a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*''' 
    t.type = reserved.get(t.value,'ID') 
    return t
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t
  
def t_NUMBER_FLOAT(t):
    r'([+-]?([0-9]*[.])?[0-9]+)'
    t.value = float(t.value)
    return t

 # Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NOT_EQUAL(t):
    r'<>'
    return t

def t_GREATER_EQUAL(t):
    r'>='
    t.lexpos = find_column(t)
    return t

def t_GREATER_THAN(t):
    r'>'
    return t

def t_LESS_EQUAL(t):
    r'<='
    return t

def t_LESS_THAN(t):
    r'<'
    return t

def t_ASSIGNMENT(t):
    r':='
    return t

# LOGICAL
def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(t):
    r'\!'
    return t   

# Symbols
def t_COLON(t):
    r':'
    return t

def t_COMMA(t):
    r','
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
 # Build the lexer
lexer = lex.lex() 

 # Test it out
data = '''
3 + 4 * 10
  + -20 *2  
variável = 2.5
'''
 
 # Give the lexer some input
lexer.input(data)
 
 # Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok) 

for tok in lexer:
    print(tok) 
 # Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
