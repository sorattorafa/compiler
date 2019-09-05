# ------------------------------------------------------------
# LEXICAL ANALYZER
# ------------------------------------------------------------
import ply.lex as lex 
from sys import argv 
  
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
        'NUMERO_INTEIRO', 
        'NUMERO_NOTACAO_CIENTIFICA',
        'SOMA',
        'SUBTRACAO',
        'MULTIPLICACAO',
        'DIVISAO',
        'ABREPARENTESES',
        'FECHAPARENTESES',  
        'IGUALDADE', 
        'NAME', 
        'NUMERO_FLUTUANTE', 
        'ID', 
        'DIFERENTE',
        'MAIOR',
        'MAIORIGUAL',
        'MENOR',
        'MENORIGUAL',
        'ATRIBUICAO',
        # Logical
        'E',
        'OU',
        'NEGACAO',
        #SYMBOLS 
        'DOISPONTOS',
        'VIRGULA', 
        'COMENTARIO', 
        'ABRECOLCHETES', 
        'FECHACOLCHETES'
    ]+ list(reserved.values())
     
     # Regular expression rules for simple tokens
    t_SOMA    = r'\+'
    t_SUBTRACAO   = r'-'
    t_MULTIPLICACAO   = r'\*'
    t_DIVISAO  = r'/'
    t_ABREPARENTESES  = r'\(' 
    t_FECHAPARENTESES  = r'\)' 
    t_ABRECOLCHETES  = r'\[' 
    t_FECHACOLCHETES  = r'\]' 
    t_IGUALDADE = r'='
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_ignore  = ' \t\n'
    t_NUMERO_FLUTUANTE = r'[-|\+]?[\d+]+\.[\d+]*'
    t_NUMERO_INTEIRO = r'[-|\+]?\d+'    
    t_NUMERO_NOTACAO_CIENTIFICA =  r'((\+|-)?[\d+]+\.?[\d+]*)E(\+|-)?[\d+]+'

    def t_COMENTARIO(self,t):
        r'\{((.|\n)*?)\}'
        pass
       # No return value. Token discarded 

     # A regular expression rule with some action code 
    def t_ID(self,t):
        r'''[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]
        [a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*''' 
        t.type = self.reserved.get(t.value,'ID')  
        return t  

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value) 

    def t_DIFERENTE(self,t):
        r'<>'
        return t

    def t_MAIORIGUAL(self,t):
        r'>='
        return t

    def t_MAIOR(self,t):
        r'>'
        return t

    def t_MENORIGUAL(self,t):
        r'<='
        return t

    def t_MENOR(self,t):
        r'<'
        return t

    def t_ATRIBUICAO(self,t):
        r':='
        return t

    # LOGICAL
    def t_E(self,t):
        r'&&'
        return t

    def t_OU(self,t):
        r'\|\|'
        return t

    def t_NEGACAO(self,t):
        r'\!'
        return t   

    # Symbols
    def t_DOISPONTOS(self,t):
        r':'
        return t

    def t_VIRGULA(self,t):
        r','
        return t
    
    # Error (no token)
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
            if (len(argv) == 2):
                print(tok.value) 
            if (len(argv) == 3):
                print(tok.type, "=>",tok.value)     
        for tok in self.lexer:
            print(tok)        