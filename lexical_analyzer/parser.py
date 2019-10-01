# coding=utf-8 
from ast import AST
from ply import yacc
from lexer import tokens
from anytree import Node
import sys 
from anytree.exporter import DotExporter 
contador = 0  # utilizado para indicar o número do nó criado
parent = ''  # auxiliares para árvore
raiz = None # raiz
funcoes_id = []
  
 
# declaracao de variaveis 
def criar_variavel(pai,line2,t):
    global contador  
    var = Node(str(contador) + '#' + 'ID-' + t[1], parent=pai, line=line2)
    return var       

# arvore sintática é implementada com nós 
# um nó tem as seguintes informacoes: 
# (número # nome_da_regra) 
def criar_no(name, parent=None, line=None):
    global contador
    contador += 1 
    # estrutura para mostrar o número e o tipo do nó
    if parent and line:
        return Node( str(contador) + '#' + name, parent=parent, line=line)
    if parent:
        return Node(str(contador) + '#' + name, parent=parent)
    else:
        return Node(str(contador) + '#' + name) 
 
# primeiro nó raiz  
def p_programa(t):
    """ programa : lista_declaracoes """
    global raiz 
    raiz = criar_no('programa-raiz')  # cria um nó raiz
    t[0] = raiz # atribui ele pra raiz t[0]
    # atribui a lista de declarações como filho do programa
    t[1].parent = raiz  
    
# erro ao criar o primeiro no    
def p_programa_erro(t):
    """ programa : error"""
    print ("Erro na regra programa")  

# segundo nó (programa->lista de declaracoes)    
def p_lista_operacoes(t):
    ''' lista_declaracoes : lista_declaracoes declaracao
    | declaracao
    '''
    pai = criar_no('lista_declaracoes') 
    # programa->lista_declaracoes
    t[0] = pai 
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai 
def p_lista_operacoes_erro(t):
    """ lista_declaracoes : error declaracao"""
    print ("Erro na regra lista_declaracoes") 

def p_lista_operacoes_erro_2(t):
    ''' lista_declaracoes : lista_declaracoes error
    '''
    print ("Erro na regra lista_declaracoes")

def p_lista_operacoes_erro_3(t):
    ''' lista_declaracoes : error
    '''
    print ("Erro na regra lista_declaracoes")    

def p_declaracao(t):
    ''' declaracao : declaracao_variaveis
    | inicializacao_variaveis
    | declaracao_funcao
    ''' 
    pai = criar_no('declaracao') 
    # lista de declaracoes -> declaracao
    t[0] = pai 
    # declaracao -> ...
    t[1].parent = pai
def p_declaracao_erro(t):
    ''' declaracao : error '''
    print ("Erro na regra de declaração")

def p_declaracao_de_variavel(t):
    ''' declaracao_variaveis : tipo DOISPONTOS lista_variaveis''' 
    # cria no de declaracao de variaveis
    pai = criar_no('declaracao_variaveis') 
    t[0] = pai 
    t[1].parent = pai #tipo
    t[2] = criar_no('DOISPONTOS', pai) # :
    t[3].parent = pai # lista
def p_declaracao_de_variavel_erro(t):
    ''' declaracao_variaveis : error DOISPONTOS lista_variaveis'''
    print ("Erro na regra de declaracao_variaveis")

def p_variaveis_inicializacao(t):
    ''' inicializacao_variaveis : atribuicao'''
    pai = criar_no('inicializacao_variaveis') 
    t[0] = pai # inicicializacao
    t[1].parent = pai # atribuicao
def p_variaveis_inicializacao_erro(t):
    ''' inicializacao_variaveis : error'''
    print ("Erro na regra de inicializacao_variaveis")

def p_lista_variaveis_inicializacao(t):
    ''' lista_variaveis : lista_variaveis VIRGULA var
    | var
    '''
    pai = criar_no('lista_variaveis')
    t[0] = pai #lista variaveis
    t[1].parent = pai # = lista variaveis
    if (len(t) > 2):
        t[2] = criar_no('VIRGULA', pai) # ,
        t[3].parent = pai # var
def p_lista_variaveis_inicializacao_erro(t):
    ''' lista_variaveis : error VIRGULA var'''
    print ("Erro na regra de lista_variaveis")

def p_variavel(t):
    ''' var : ID
    | ID indice
    '''
    pai = criar_no('var')
    t[0] = pai
    global contador
    contador+=1 
    # t[1] = Node(str(contador) + '#' + 'ID-' + t[1], parent=pai, line=t.lineno(1))
    t[1] = criar_variavel(pai,t.lineno(1),t) 
    if len(t) > 2:
        t[2].parent = pai
def p_variavel_erro(t):
    ''' var : ID error '''
    print ("Erro na regra de var")

def p_indice(t):
    ''' indice : indice ABRECOLCHETE expressao FECHACOLCHETE
    | ABRECOLCHETE expressao FECHACOLCHETE
    '''
    pai = criar_no('indice')
    t[0] = pai
    if len(t) == 4:
        t[1] = criar_no('ABRECOLCHETE', pai)
        t[2].parent = pai
        t[3] = criar_no('FECHACOLCHETE', pai)
    else:
        t[1].parent = pai
        t[2] = criar_no('ABRECOLCHETE', pai)
        t[3].parent = pai
        t[4] = criar_no('FECHACOLCHETE', pai)
def p_indice_erro(t):
    ''' indice : indice ABRECOLCHETE error FECHACOLCHETE
    | ABRECOLCHETE error FECHACOLCHETE
    | error ABRECOLCHETE expressao FECHACOLCHETE
    '''
    print ("Erro na geração da regra indice")

def p_tipo_variavel(t):
    ''' tipo : INTEIRO
    | FLUTUANTE
    '''
    pai = criar_no('tipo')
    t[0] = pai
    t[1] = criar_no(t[1].upper(), pai)

def p_func_declaracao(t):
    ''' declaracao_funcao : tipo cabecalho
    | cabecalho
    '''
    pai = criar_no('declaracao_funcao')
    t[0] = pai
    t[1].parent = pai
    if len(t) == 3:
        t[2].parent = pai
def p_func_declaracao_erro(t):
    ''' declaracao_funcao : error cabecalho
    | tipo error
    | error
    '''
    print ("Erro na geração da regra declaracao_funcao")

def p_cabecalho_func(t):
    ''' cabecalho : ID ABREPARENTESES lista_parametros FECHAPARENTESES corpo FIM'''
    global funcoes_id
    funcoes_id.append(t[1])
    pai = criar_no('cabecalho')
    t[0] = pai
    t[1] = criar_no('ID-' + t[1], pai, t.lineno(1))
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai
    t[4] = criar_no('FECHAPARENTESES', pai)
    t[5].parent = pai
    t[6] = criar_no('FIM', pai)
def p_cabecalho_func_erro(t):
    ''' cabecalho : ID ABREPARENTESES error FECHAPARENTESES corpo FIM
    | ID ABREPARENTESES lista_parametros FECHAPARENTESES error FIM
    '''
    print ("Erro na geração da regra declaracao_funcao")

def p_lista_parametros(t):
    ''' lista_parametros : lista_parametros VIRGULA lista_parametros
    | parametro
    | vazio
    '''
    pai = criar_no('lista_parametros')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2] = criar_no('VIRUGLA', pai)
        t[3].parent = pai
def p_lista_parametros_erro(t):
    ''' lista_parametros : error VIRGULA lista_parametros
    | lista_parametros VIRGULA error
    | error
    '''
    print ("Erro na geração da regra lista_parametros")

def p_parametro(t):
    ''' parametro : tipo DOISPONTOS ID
    | parametro ABRECOLCHETE FECHACOLCHETE
    '''
    pai = criar_no('parametro')
    t[0] = pai
    t[1].parent = pai
    if t[2] == ':':
        t[2] = criar_no('DOISPONTOS', pai)
        t[3] = criar_no('ID-' + t[3], pai, line=t.lineno(3))
    else:
        t[2] = criar_no('ABRECOLCHETE', pai)
        t[3] = criar_no('FECHACOLCHETE', pai, line=t.lineno(3))
def p_parametro_erro(t):
    ''' parametro : error DOISPONTOS ID
    | error ABRECOLCHETE FECHACOLCHETE
    '''
    print ("Erro na geração da regra parametro")

def p_corpo(t):
    ''' corpo : corpo acao
    | vazio
    | acao
    '''
    pai = criar_no('corpo')
    t[0] = pai
    t[1].parent = pai
    if len(t) == 3:
        t[2].parent = pai
def p_corpo_erro(t):
    ''' corpo : error acao
    | corpo error
    | error
    '''
    print ("Erro na geração da regra corpo")

def p_acao(t):
    ''' acao : expressao
    | declaracao_variaveis
    | se
    | repita
    | leia
    | escreva
    | retorna
    '''
    pai = criar_no('acao')
    t[0] = pai
    t[1].parent = pai
def p_acao_erro(t):
    ''' acao : error'''
    print ("Erro na geração da regra acao")

def p_se(t):
    ''' se : SE expressao ENTAO corpo FIM
    | SE expressao ENTAO corpo SENAO corpo FIM
    '''
    pai = criar_no('se')
    t[0] = pai
    t[1] = criar_no('SE', pai, t.lineno(1))
    t[2].parent = pai
    t[3] = criar_no('ENTAO', pai)
    t[4].parent = pai
    if len(t) == 8:
        t[5] = criar_no('SENAO', pai)
        t[6].parent = pai
        t[7] = criar_no('FIM', pai)
    else:
        t[5] = criar_no('FIM', pai)
def p_se_erro(t):
    ''' se : SE error ENTAO corpo FIM
    | SE expressao ENTAO error FIM
    | SE error ENTAO corpo SENAO corpo FIM
    | SE expressao ENTAO error SENAO corpo FIM
    | SE expressao ENTAO corpo SENAO error FIM
    '''
    print ("Erro na geração da regra se")

def p_repita(t):
    ''' repita : REPITA corpo ATE expressao'''
    pai = criar_no('repita')
    t[0] = pai
    t[1] = criar_no('REPITA', pai)
    t[2].parent = pai
    t[3] = criar_no('ATE', pai, t.lineno(3))
    t[4].parent = pai
def p_repita_erro(t):
    ''' repita : REPITA corpo ATE error
    | REPITA error ATE expressao
    '''
    print ("Erro na geração da regra repita")

def p_atribuicao(t):
    ''' atribuicao : var ATRIBUICAO expressao'''
    pai = criar_no('atribuicao')
    t[0] = pai
    t[1].parent = pai
    t[2] = criar_no('ATRIBUICAO', pai)
    t[3].parent = pai 
def p_atribuicao_erro(t):
    ''' atribuicao : var ATRIBUICAO error
    | error ATRIBUICAO expressao
    '''
    print('Erro na geração da regra de atribuicao')

def p_leia(t):
    ''' leia : LEIA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('leia')
    t[0] = pai
    t[1] = criar_no('LEIA', pai)
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_leia_erro(t):
    ''' leia : LEIA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")

def p_escreva(t):
    ''' escreva : ESCREVA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('escreva')
    t[0] = pai
    t[1] = criar_no('ESCREVA', pai)
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_escreva_erro(t):
    ''' escreva : ESCREVA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")

def p_retorna(t):
    ''' retorna : RETORNA ABREPARENTESES expressao FECHAPARENTESES '''
    pai = criar_no('retorna')
    t[0] = pai
    t[1] = criar_no('RETORNA', pai, t.lineno(1))
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_retorna_erro(t):
    ''' retorna : RETORNA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra retorna")

def p_expressao(t):
    ''' expressao : expressao_logica
    | atribuicao
    '''
    pai = criar_no('expressao')
    t[0] = pai
    t[1].parent = pai
def p_expressao_erro(t):
    ''' expressao : error'''
    print ("Erro na geração da regra expressao")

def p_expressao_logica(t):
    ''' expressao_logica : expressao_simples
    | expressao_logica operador_logico expressao_simples
    '''
    pai = criar_no('expressao_logica')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai
        t[3].parent = pai
def p_expressao_logica_erro(t):
    ''' expressao_logica : error operador_logico expressao_simples
    | expressao_logica error expressao_simples
    | expressao_logica operador_logico error
    | error
    '''
    print ("Erro na geração da regra expressao_logica")

def p_expressao_simples(t):
    ''' expressao_simples : expressao_aditiva
    | expressao_logica operador_relacional expressao_simples
    '''
    pai = criar_no('expressao_simples')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai
        t[3].parent = pai
def p_expressao_simples_erro(t):
    ''' expressao_simples : error
    | error operador_relacional expressao_simples
    | expressao_logica error expressao_simples
    | expressao_logica operador_relacional error
    '''
    print ("Erro na geração da regra expressao_simples")

def p_expressao_aditiva(t):
    ''' expressao_aditiva : expressao_multiplicativa
    | expressao_aditiva operador_soma expressao_multiplicativa
    '''
    pai = criar_no('expressao_aditiva')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai
        t[3].parent = pai
def p_expressao_aditiva_erro(t):
    ''' expressao_aditiva : error
    | error operador_soma expressao_multiplicativa
    | expressao_aditiva error expressao_multiplicativa
    | expressao_aditiva operador_soma error
    '''
    print ("Erro na geração da regra expressao_aditiva")

def p_expressao_multiplicativa(t):
    ''' expressao_multiplicativa : expressao_unaria
    | expressao_multiplicativa operador_multiplicacao expressao_unaria
    ''' 
    pai = criar_no('expressao_multiplicativa')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai
        t[3].parent = pai 
        
def p_expressao_multiplicativa_erro(t):
    ''' expressao_multiplicativa : error
    | error operador_multiplicacao expressao_unaria
    | expressao_multiplicativa error expressao_unaria
    | expressao_multiplicativa operador_multiplicacao error
    '''
    print ("Erro na geração da regra expressao_multiplicativa")

def p_expressao_unaria(t):
    ''' expressao_unaria : fator
    | operador_soma fator
    | NAO fator
    '''
    pai = criar_no('expressao_unaria')
    t[0] = pai
    if t[1] == '!':
        t[1] = criar_no('NAO', pai)
    else:
        t[1].parent = pai

    if len(t) > 2:
        t[2].parent = pai
def p_expressao_unaria_erro(t):
    ''' expressao_unaria : error
    | error fator
    | operador_soma error
    | NAO error
    '''
    print ("Erro na geração da regra expressao_aditiva")

def p_operador_multiplicacao_divisao(t):
    ''' operador_multiplicacao : MULTIPLICACAO
    | DIVISAO
    '''
    pai = criar_no('operador_multiplicacao')
    t[0] = pai
    if t[1] == '*':
        t[1] = criar_no('MULTIPLICACAO', pai)
    else:
        t[1] = criar_no('DIVISAO', pai)

def p_fator(t):
    ''' fator : ABREPARENTESES expressao FECHAPARENTESES
    | var
    | chamada_funcao
    | numero
    '''
    pai = criar_no('fator')
    t[0] = pai
    if len(t) > 2:
        t[1] = criar_no('ABREPARENTESES', pai)
        t[2].parent = pai
        t[3] = criar_no('FECHAPARENTESES', pai)
    else:
        t[1].parent = pai

def p_fator_erro(t):
    ''' fator : ABREPARENTESES error FECHAPARENTESES
    | error
    '''
    print("Erro na geração da regra fator")

def p_numero(t):
    ''' numero : NUMERO_INTEIRO
    | NUMERO_PONTO_FLUTUANTE
    '''
    pai = criar_no('numero')
    t[0] = pai
    if t[1].find('.') == -1:
        t[1] = criar_no('NUMERO_INTEIRO-' + t[1], pai)
    else:
        t[1] = criar_no('NUMERO_PONTO_FLUTUANTE-' + t[1], pai)

def p_chamada_funcao(t):
    ''' chamada_funcao : ID ABREPARENTESES lista_argumentos FECHAPARENTESES
    '''
    pai = criar_no('chamada_funcao')
    t[0] = pai
    t[1] = criar_no('ID-' + t[1], pai, line=t.lineno(1))
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai
    t[4] = criar_no('FECHAPARENTESES', pai)


def p_chamada_funcao_erro(t):
    ''' chamada_funcao : ID ABREPARENTESES error FECHAPARENTESES'''
    print("Erro na geração da regra fator")

def p_lista_argumentos(t):
    ''' lista_argumentos : lista_argumentos VIRGULA expressao
    | expressao
    | vazio
    '''
    pai = criar_no('lista_argumentos')
    t[0] = pai
    t[1].parent = pai
    if len(t) > 2:
        t[2] = criar_no('VIRGULA', pai)
        t[3].parent = pai

def p_lista_argumentos_erro(t):
    ''' lista_argumentos : error VIRGULA expressao
    | lista_argumentos VIRGULA error
    | error
    '''
    print("Erro na geração da regra fator") 

def p_operador_relacional(t):
    ''' operador_relacional : MENOR
    | MAIOR
    | IGUALDADE
    | DIFERENTE
    | MENORIGUAL
    | MAIORIGUAL
    '''
    pai = criar_no('operador_relacional')
    t[0] = pai
    if t[1] == '<':
        t[1] = criar_no('MENOR', pai)
    elif t[1] == '>':
        t[1] = criar_no('MAIOR', pai)
    elif t[1] == '=':
        t[1] = criar_no('IGUALDADE', pai)
    elif t[1] == '<>':
        t[1] = criar_no('DIFERENTE', pai)
    elif t[1] == '>=':
        t[1] = criar_no('MAIOR_GUAL', pai)
    else:
        t[1] = criar_no('MENORIGUAL', pai)
# operador aritmetico
def p_operador_aritmetico(t):
    ''' operador_soma : SOMA
    | SUBTRACAO
    '''
    pai = criar_no('operador_aritmetico')
    t[0] = pai # raiz = op aritmetico
    # se a segunda palavra é +
    if t[1] == '+': 
        t[1] = criar_no('SOMA', pai) # op aritmetico => soma
    else:
        t[1] = criar_no('SUBTRACAO', pai) # op aritmetico => subtracao
 
# define operadores logicos e/ou 
def p_operadores_logico(t):
    ''' operador_logico : E
    | OU
    '''
    pai = criar_no('operador_logico')
    t[0] = pai # op log 
    # se a segunda palavra for e
    if t[1] == '&&': 
        # op logico -> e    
        t[1] = criar_no('E', pai)
    else: 
        # op logico -> ou    
        t[1] = criar_no('OU', pai)
 
# negacao 
def p_operador_not(t):
    ''' operador_negacao : NAO'''
    pai = criar_no('operador_negacao')
    t[0] = pai # operador negacao
    t[1] = criar_no('NAO', pai) # op -> nao
 
# somente t[0] como pai
def p_vazio(t):
    ' vazio : '
    pai = criar_no('vazio') 
    t[0] = pai # vazio

def p_erro(t): 
    # se for error de sintaxe    
    if t: 
        # mostra uma exeção indicando a linha e o token         
        raise Exception("Erro de sintaxe na linha {} no token '{}'".format(t.lineno, t.value))
    else: 
        # reinicia o parser    
        parser.restart() 
        # gera uma  execao de erro
        raise Exception("Erro")
  
# ativa o parser  
parser = yacc.yacc() 
#recebe o arquivo com códgio tpp
code = open(sys.argv[1]) 
# le arquivo
code_text = code.read() 
# realiza a analise sintatica do código
try:
    parser.parse(code_text)
except Exception as e:
    raise e 
# se não houver uma raíz possui erro
if not raiz:
    raise Exception('Nao foi possivel gerar a árvore') 
# se houver uma raiz então pode-se mostrar a ávore sintática dessa raiz  
DotExporter(raiz).to_picture("arvore-sintatica.png")