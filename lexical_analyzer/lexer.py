# -*- coding: UTF-8 -*-
import ply.lex as lex
from ply.lex import TOKEN
import sys
import re
# Palavras Rservadas
reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'senão': 'SENAO',
    'fim': 'FIM',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA',
    'até': 'ATE',
    'flutuante': 'FLUTUANTE',
    'inteiro': 'INTEIRO',
    'repita': 'REPITA',
}
# Lista de nomes dos tokens
tokens = [
# Logicals
'E', 'OU', 'NAO', 
# Types
'NUMERO_PONTO_FLUTUANTE', 'NUMERO_INTEIRO',
# Arithmeticals
'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO',
# Relationals
'MENORIGUAL', 'MAIORIGUAL', 'IGUALDADE', 'DIFERENTE', 'MENOR', 'MAIOR',
# Simbolos
'VIRGULA', 'ATRIBUICAO', 'ABREPARENTESES', 'FECHAPARENTESES', 'ABRECOLCHETE', 'FECHACOLCHETE',
'ABRECHAVE', 'FECHACHAVE', 'DOISPONTOS',
# Outros
'ID', 'COMENTARIO']+list(reserved.values())

# NUMEROS
t_NUMERO_PONTO_FLUTUANTE = r'((\d+)(\.\d+)(e(\+|-)?(\d+))?|(\d+)e(\+|-)?(\d+))'
t_NUMERO_INTEIRO = r'\d+'
 
# LOGICOS 
t_E = r'&&'
t_OU = r'\|'
t_NAO = r'\!'
#OPERACOES
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
#SIMBOLOS
t_VIRGULA = r','
t_ATRIBUICAO = r':='
t_ABREPARENTESES = r'\('
t_FECHAPARENTESES = r'\)'
t_ABRECOLCHETE = r'\['
t_FECHACOLCHETE = r'\]'
t_ABRECHAVE = r'\{'
t_FECHACHAVE = r'\}'
t_DOISPONTOS = r':' 

#RELACIONAIS
def t_DIFERENTE(t):
    r'<>'
    return t

def t_IGUALDADE(t):
    r'='
    return t
def t_MAIORIGUAL(t):
    r'>='
    return t

def t_MAIOR(t):
    r'>'
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_MENOR(t):
    r'<'
    return t

def t_ID(t):
    r'[A-Za-zÁ-Ñá-ñ_][\w_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMENTARIO(t):
    r'{[^(})]*}'
    lineCount = re.findall('\n', t.value)
    t.lexer.lineno += len(lineCount)

# New lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# IGNORA ESPACO E TAB
t_ignore = ' \t'

# Erro
def t_error(t):
    raise Exception("Caracter ilegal '{}' (linha {})".format(t.value[0], t.lineno))

lexer = lex.lex(debug=False) 

if __name__ == '__main__':
    lista_tokens = []
    new_token = {}
    code = open(sys.argv[1])
    code_text = code.read()
    lex.input(code_text)
    while True:
        tok = lex.token()
        if not tok:
            break
        new_token['Tipo'] = tok.type
        new_token['Linha'] = tok.lineno
        new_token['Valor'] = tok.value
        lista_tokens.append(new_token)
        print(new_token)
    new_token = {}