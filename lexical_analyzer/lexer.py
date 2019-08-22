# ------------------------------------------------------------
# LEXICAL ANALYZER USING PYTHON AND PLY PACKAGE
# ------------------------------------------------------------
import ply.lex as lex 
  
class MyLexer(object):
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
        'OPENFUNCT', 
        'CLOSEFUNCT', 
        'ENDLINE', 
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
        'COMMENT', 
        #commands 
        'FOR', 
        'PRINT',
    ]+ list(reserved.values())
     
     # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\(' 
    t_RPAREN  = r'\)' 
    t_OPENFUNCT  = r'\{' 
    t_CLOSEFUNCT  = r'\}' 
    t_ENDLINE  = r';'
    t_EQUALS = r'='
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_FOR   = r'fo  r'
    t_PRINT = r'print'   
    t_ignore  = ' \t'

    def t_COMMENT(self,t):
        r'\{[^\"]*\}'
        pass
       # No return value. Token discarded 

     # A regular expression rule with some action code 
    def t_ID(self,t):
        r'''[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]
        [a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*''' 
        t.type = self.reserved.get(t.value,'ID')  
        return t
    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t
      
    def t_NUMBER_FLOAT(self,t):
        r'([+-]?([0-9]*[.])?[0-9]+)'
        t.value = float(t.value)
        return t

     # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NOT_EQUAL(self,t):
        r'!='
        return t

    def t_GREATER_EQUAL(self,t):
        r'>='
        t.lexpos = find_column(self,t)
        return t

    def t_GREATER_THAN(self,t):
        r'>'
        return t

    def t_LESS_EQUAL(self,t):
        r'<='
        return t

    def t_LESS_THAN(self,t):
        r'<'
        return t

    def t_ASSIGNMENT(self,t):
        r':='
        return t

    # LOGICAL
    def t_AND(self,t):
        r'&&'
        return t

    def t_OR(self,t):
        r'\|\|'
        return t

    def t_NOT(self,t):
        r'\!'
        return t   

    # Symbols
    def t_COLON(self,t):
        r':'
        return t

    def t_COMMA(self,t):
        r','
        return t
    
    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
     # Build the lexer
    def build(self):
        self.lexer = lex.lex(debug=False, module=self, optimize=False) 
    def test(self,data):
         # Give the lexer some input 
        self.lexer.input(data)
         
         # Tokenize
        while True:
            tok = self.lexer.token()
            if not tok: 
                break      # No more input
            print(tok) 

        for tok in self.lexer:
            print(tok) 
         # Tokenize
        while True:
            tok = self.lexer.token()
            if not tok: 
                break      # No more input
            print(tok.type, tok.value, tok.lineno, tok.lexpos) 

 # Build the lexer and try it out
m = MyLexer()
m.build()           # Build the lexer  
# input data
data = '''
{ 3 + 4 * 10
   + -20 *2  
}
i = 0
repita:  
    i := i + 1 
    variável := i
até: i != 5
'''
m.test(data)     # Test it
