# coding=utf-8  
# dependencias utilizadas no python3
from ply import yacc
from lexer import tokens
from anytree import Node, LevelOrderIter, PreOrderIter
import sys 
from anytree.exporter import DotExporter     
#import re   
from semantic import * 

# variáveis auxiliares para criação da árvore
raiz = None # raiz 
# lista dos id's de funcoes
lista_funcoes_id = [] 
contador = 0
# p.lineno(num). Return the line number for symbol num
# p.lexpos(num). Return the lexing position for symbol num 
 
# declaracao de variaveis 
def criar_variavel(pai,line2,p): 
    # var : contador - ID -  nome da variável
    var = Node('ID-' + p[1], parent=pai, line=line2) 
    # retorna var
    return var        

# arvore sintática é implementada com nós 
# um nó tem as seguintes informacoes:  
# (nome, pai, numero)
def criar_no(name, parent=None, line=None):  
    global contador 
    contador += 1    
    if parent and line:
        return Node(str(contador) + '=' + name, parent=parent, line=line)
    if parent:
        return Node(str(contador) + '=' + name, parent=parent)
    else:
        return Node(str(contador) + '=' + name)
 
# primeiro nó raiz  
def p_programa(p):
    """ programa : lista_declaracoes  
    """
    global raiz 
    raiz = criar_no('programa-raiz')  # cria um nó raiz
    p[0] = raiz # atribui ele pra raiz t[0]
    # atribui a lista de declarações como filho do programa
    p[1].parent = raiz  
    
# erro ao criar o primeiro no    
def p_programa_erro(p):
    """ programa : error"""
    print ("Erro na regra programa")  

# segundo nó (programa->lista de declaracoes)    
def p_lista_declaracoes(p):
    ''' lista_declaracoes : lista_declaracoes declaracao
    | declaracao
    '''
    pai = criar_no('lista_declaracoes') 
    # programa->lista_declaracoes
    p[0] = pai 
    p[1].parent = pai
    if len(p) == 3:
        p[2].parent = pai 
def p_lista_declaracoes_erro(p):
    """ lista_declaracoes : error declaracao"""
    print ("Erro na regra lista_declaracoes") 

def p_declaracao(p):
    ''' declaracao : declaracao_variaveis
    | inicializacao_variaveis
    | declaracao_funcao
    ''' 
    pai = criar_no('declaracao') 
    # lista de declaracoes -> declaracao
    p[0] = pai 
    # declaracao -> ...
    p[1].parent = pai
def p_declaracao_erro(p):
    ''' declaracao : error '''
    print ("Erro na regra de declaração")

def p_declaracao_de_variavel(p):
    ''' declaracao_variaveis : tipo DOISPONTOS lista_variaveis''' 
    # cria no de declaracao de variaveis
    pai = criar_no('declaracao_variaveis') 
    p[0] = pai 
    p[1].parent = pai #tipo
    p[2] = criar_no('DOISPONTOS', pai) # :
    p[3].parent = pai # lista
def p_declaracao_de_variavel_erro(p):
    ''' declaracao_variaveis : error DOISPONTOS lista_variaveis'''
    print ("Erro na regra de declaracao_variaveis")

def p_variaveis_inicializacao(p):
    ''' inicializacao_variaveis : atribuicao'''
    pai = criar_no('inicializacao_variaveis') 
    p[0] = pai # inicicializacao
    p[1].parent = pai # atribuicao
def p_variaveis_inicializacao_erro(p):
    ''' inicializacao_variaveis : error'''
    print ("Erro na regra de inicializacao_variaveis")

def p_lista_variaveis_inicializacao(p):
    ''' lista_variaveis : lista_variaveis VIRGULA var
    | var
    '''
    pai = criar_no('lista_variaveis')
    p[0] = pai #lista variaveis
    p[1].parent = pai # = lista variaveis
    if (len(p) > 2):
        p[2] = criar_no('VIRGULA', pai) # ,
        p[3].parent = pai # var
def p_lista_variaveis_inicializacao_erro(t):
    ''' lista_variaveis : error VIRGULA var'''
    print ("Erro na regra de lista_variaveis")

def p_variavel(p):
    ''' var : ID
    | ID indice
    ''' 
    global contador
    pai = criar_no('var')
    p[0] = pai 
    p[1] = Node(str(contador) + '=' + 'ID-' + p[1], parent=pai, line=p.lineno(1))
    # se tiver indice
    if len(p) > 2:
        p[2].parent = pai
def p_variavel_erro(p):
    ''' var : ID error '''
    print ("Erro na regra de var")

def p_indice(p):
    ''' indice : indice ABRECOLCHETE expressao FECHACOLCHETE
    | ABRECOLCHETE expressao FECHACOLCHETE
    ''' 
    # utilizado em vetores e matrizes para saber o indice
    pai = criar_no('indice')
    p[0] = pai 
    #vetores
    if len(p) == 4:
        p[1] = criar_no('ABRECOLCHETE', pai)
        p[2].parent = pai
        p[3] = criar_no('FECHACOLCHETE', pai) 
    # matrizes    
    else:
        p[1].parent = pai
        p[2] = criar_no('ABRECOLCHETE', pai)
        p[3].parent = pai
        p[4] = criar_no('FECHACOLCHETE', pai) 
        
def p_indice_erro(p):
    ''' indice : indice ABRECOLCHETE error FECHACOLCHETE
    | ABRECOLCHETE error FECHACOLCHETE
    | error ABRECOLCHETE expressao FECHACOLCHETE
    '''
    print ("Erro na geração da regra indice")

def p_tipo_variavel(p):
    ''' tipo : INTEIRO
    | FLUTUANTE
    '''
    pai = criar_no('tipo') # tipo
    p[0] = pai
    p[1] = criar_no(p[1], pai) # tipo -> inteiro ou flutuante

def p_acao(p):
    ''' acao : expressao
    | declaracao_variaveis
    | se
    | repita
    | leia
    | escreva
    | retorna
    '''
    pai = criar_no('acao')
    p[0] = pai # acao
    p[1].parent = pai # acao -> expressao
def p_acao_erro(p):
    ''' acao : error'''
    print ("Erro na geração da regra acao")


def p_repita(p):
    ''' repita : REPITA corpo ATE expressao'''
    pai = criar_no('repita')
    p[0] = pai # repita
    p[1] = criar_no('REPITA', pai) # repita -> REPITA
    p[2].parent = pai # corpo
    p[3] = criar_no('ATE', pai, p.lineno(3))
    p[4].parent = pai # expressao
def p_repita_erro(p):
    ''' repita : REPITA corpo ATE error
    | REPITA error ATE expressao
    '''
    print ("Erro na geração da regra repita")

def p_atribuicao(p):
    ''' atribuicao : var ATRIBUICAO expressao'''
    pai = criar_no('atribuicao')
    p[0] = pai # atribuição 
    p[1].parent = pai # atribuicao -> var
    p[2] = criar_no('ATRIBUICAO', pai)
    p[3].parent = pai # expressao
def p_atribuicao_erro(p):
    ''' atribuicao : var ATRIBUICAO error
    | error ATRIBUICAO expressao
    '''
    print('Erro na geração da regra de atribuicao')

def p_leia(p):
    ''' leia : LEIA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('leia')
    p[0] = pai # leia
    p[1] = criar_no('LEIA', pai)
    p[2] = criar_no('ABREPARENTESES', pai)
    p[3].parent = pai # expressao
    p[4] = criar_no('FECHAPARENTESES', pai)
def p_leia_erro(p):
    ''' leia : LEIA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")

def p_escreva(p):
    ''' escreva : ESCREVA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('escreva')
    p[0] = pai # escreva
    p[1] = criar_no('ESCREVA', pai)
    p[2] = criar_no('ABREPARENTESES', pai)
    p[3].parent = pai # expressao
    p[4] = criar_no('FECHAPARENTESES', pai)
def p_escreva_erro(p):
    ''' escreva : ESCREVA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")
 
def p_se(p):
    ''' se : SE expressao ENTAO corpo FIM
    | SE expressao ENTAO corpo SENAO corpo FIM
    '''
    pai = criar_no('se')
    p[0] = pai # se
    p[1] = criar_no('SE', pai, p.lineno(1)) # se -> SE
    p[2].parent = pai # se -> SE expressao
    p[3] = criar_no('ENTAO', pai) # se-> SE Expressao Então
    p[4].parent = pai # corpo
    # se tiver um senão
    if len(p) == 8:
        p[5] = criar_no('SENAO', pai)
        p[6].parent = pai 
        p[7] = criar_no('FIM', pai) 
    else:
        p[5] = criar_no('FIM', pai)
def p_se_erro(p):
    ''' se : SE error ENTAO corpo FIM
    | SE expressao ENTAO error FIM
    | SE error ENTAO corpo SENAO corpo FIM
    | SE expressao ENTAO error SENAO corpo FIM
    | SE expressao ENTAO corpo SENAO error FIM
    '''
    print ("Erro na geração da regra se") 
    
def p_retorna(p):
    ''' retorna : RETORNA ABREPARENTESES expressao FECHAPARENTESES '''
    pai = criar_no('retorna')
    p[0] = pai # retorna
    p[1] = criar_no('RETORNA', pai, p.lineno(1))
    p[2] = criar_no('ABREPARENTESES', pai)
    p[3].parent = pai # expressao
    p[4] = criar_no('FECHAPARENTESES', pai)
def p_retorna_erro(p):
    ''' retorna : RETORNA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra retorna")

def p_expressao(p):
    ''' expressao : expressao_logica
    | atribuicao
    '''
    pai = criar_no('expressao')
    p[0] = pai # expressao
    p[1].parent = pai # expressao -> expressao_logica
def p_expressao_erro(p):
    ''' expressao : error'''
    print ("Erro na geração da regra expressao")

def p_expressao_logica(p):
    ''' expressao_logica : expressao_simples
    | expressao_logica operador_logico expressao_simples
    '''
    pai = criar_no('expressao_logica')
    p[0] = pai
    p[1].parent = pai # expressao_logica -> expressao_simples 
    # operador logico
    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai
def p_expressao_logica_erro(p):
    ''' expressao_logica : error operador_logico expressao_simples
    | expressao_logica error expressao_simples
    | expressao_logica operador_logico error
    | error
    '''
    print ("Erro na geração da regra expressao_logica")

def p_expressao_simples(p):
    ''' expressao_simples : expressao_aditiva
    | expressao_logica operador_relacional expressao_simples
    '''
    pai = criar_no('expressao_simples')
    p[0] = pai # expressao_simples
    p[1].parent = pai # expressao_aditiva 
    # operador relacional
    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai
def p_expressao_simples_erro(p):
    ''' expressao_simples : error
    | error operador_relacional expressao_simples
    | expressao_logica error expressao_simples
    | expressao_logica operador_relacional error
    '''
    print ("Erro na geração da regra expressao_simples")

def p_expressao_aditiva(p):
    ''' expressao_aditiva : expressao_multiplicativa
    | expressao_aditiva operador_soma expressao_multiplicativa
    '''
    pai = criar_no('expressao_aditiva')
    p[0] = pai # expressao aditiva
    p[1].parent = pai # expressao multiplicativa 
    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai
def p_expressao_aditiva_erro(p):
    ''' expressao_aditiva : error
    | error operador_soma expressao_multiplicativa
    | expressao_aditiva error expressao_multiplicativa
    | expressao_aditiva operador_soma error
    '''
    print ("Erro na geração da regra expressao_aditiva")

def p_expressao_multiplicativa(p):
    ''' expressao_multiplicativa : expressao_unaria
    | expressao_multiplicativa operador_multiplicacao expressao_unaria
    ''' 
    pai = criar_no('expressao_multiplicativa')
    p[0] = pai  # expressao multiplicativa
    p[1].parent = pai # expressao unaria 
    # expressao multiplicativa
    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai 
        
def p_expressao_multiplicativa_erro(p):
    ''' expressao_multiplicativa : error
    | error operador_multiplicacao expressao_unaria
    | expressao_multiplicativa error expressao_unaria
    | expressao_multiplicativa operador_multiplicacao error
    '''
    print ("Erro na geração da regra expressao_multiplicativa")

def p_expressao_unaria(p):
    ''' expressao_unaria : fator
    | operador_soma fator
    | NAO fator
    '''
    pai = criar_no('expressao_unaria')
    p[0] = pai # expressao unaria 
    # se for a negacao
    if p[1] == '!':
        p[1] = criar_no('NAO', pai) 
    # senao     
    else:
        p[1].parent = pai # fator 
    # operador soma    
    if len(p) > 2:
        p[2].parent = pai
def p_expressao_unaria_erro(p):
    ''' expressao_unaria : error
    | error fator
    | operador_soma error
    | NAO error
    '''
    print ("Erro na geração da regra expressao_aditiva")

def p_operador_multiplicacao_divisao(p):
    ''' operador_multiplicacao : MULTIPLICACAO
    | DIVISAO
    '''
    pai = criar_no('operador_multiplicacao')
    p[0] = pai # operador 
    # se for multiplicacao
    if p[1] == '*':
        p[1] = criar_no('MULTIPLICACAO', pai) 
    # se for divisao    
    else:
        p[1] = criar_no('DIVISAO', pai)

def p_fator(p):
    ''' fator : ABREPARENTESES expressao FECHAPARENTESES
    | var
    | chamada_funcao
    | numero
    '''
    pai = criar_no('fator')
    p[0] = pai # fator
    if len(p) > 2:
        p[1] = criar_no('ABREPARENTESES', pai)
        p[2].parent = pai # expressao
        p[3] = criar_no('FECHAPARENTESES', pai)
    else:
        p[1].parent = pai # chamada de funcao ou var ou numero

def p_fator_erro(p):
    ''' fator : ABREPARENTESES error FECHAPARENTESES
    | error
    '''
    print("Erro na geração da regra fator")

def p_numero(p):
    ''' numero : NUMERO_INTEIRO
    | NUMERO_PONTO_FLUTUANTE
    '''
    pai = criar_no('numero')
    p[0] = pai # NUMERO 
    # se não tiver a parte decimal então é inteiro
    if p[1].find('.') == -1: 
        p[1] = criar_no('NUMERO_INTEIRO-' + p[1], pai) 
    else:  
        p[1] = criar_no('NUMERO_PONTO_FLUTUANTE-' + p[1], pai)         
    # se tiver decimais é flutuante        
def p_chamada_funcao(p):
    ''' chamada_funcao : ID ABREPARENTESES lista_argumentos FECHAPARENTESES
    '''
    pai = criar_no('chamada_funcao')
    p[0] = pai # chamada de funcao
    p[1] = criar_no('ID-' + p[1], pai, line=p.lineno(1)) # ID
    p[2] = criar_no('ABREPARENTESES', pai)
    p[3].parent = pai # lsta de argumentos
    p[4] = criar_no('FECHAPARENTESES', pai)


def p_chamada_funcao_erro(t):
    ''' chamada_funcao : ID ABREPARENTESES error FECHAPARENTESES 
    '''
    print("Erro na geração da regra fator")
 
 
def p_lista_argumentos(p):
    ''' lista_argumentos : lista_argumentos VIRGULA expressao
    | expressao
    | vazio
    '''
    pai = criar_no('lista_argumentos')
    p[0] = pai
    p[1].parent = pai
    if len(p) > 2:
        p[2] = criar_no('VIRGULA', pai)
        p[3].parent = pai

def p_lista_argumentos_erro(p):
    ''' lista_argumentos : error VIRGULA expressao
    | lista_argumentos VIRGULA error
    | error
    '''
    print("Erro na geração da regra fator") 
   
# relacao entre numeros   
def p_operador_relacional(p):
    ''' operador_relacional : MENOR
    | MAIOR
    | IGUALDADE
    | DIFERENTE
    | MENORIGUAL
    | MAIORIGUAL
    '''
    pai = criar_no('operador_relacional')
    p[0] = pai # t[0] -> op relacional
    if p[1] == '<':
        p[1] = criar_no('MENOR', pai) # op relacional -> menor
    elif p[1] == '<>':
        p[1] = criar_no('DIFERENTE', pai) # op relacional -> diferente
    elif p[1] == '>=':
        p[1] = criar_no('MAIOR_GUAL', pai) # op relacional -> maior igual 
    elif p[1] == '>':
        p[1] = criar_no('MAIOR', pai) # op relacional -> maior
    elif p[1] == '=':
        p[1] = criar_no('IGUALDADE', pai) # op relacional -> igual    
    else:
        p[1] = criar_no('MENORIGUAL', pai) # # op relacional -> menor igual
# operador aritmetico
def p_operador_soma(p):
    ''' operador_soma : SOMA
    | SUBTRACAO
    '''
    pai = criar_no('operador_aritmetico')
    p[0] = pai # raiz = op aritmetico
    # se a segunda palavra é +
    if p[1] == '+': 
        p[1] = criar_no('SOMA', pai) # op aritmetico => soma
    else:
        p[1] = criar_no('SUBTRACAO', pai) # op aritmetico => subtracao
 
# define operadores logicos e/ou 
def p_operadores_logico(p):
    ''' operador_logico : E
    | OU
    '''
    pai = criar_no('operador_logico')
    p[0] = pai # op log 
    # se a segunda palavra for e
    if p[1] == '&&': 
        # op logico -> e    
        p[1] = criar_no('E', pai)
    else: 
        # op logico -> ou    
        p[1] = criar_no('OU', pai)
 
# negacao 
def p_operador_not(p):
    ''' operador_negacao : NAO'''
    pai = criar_no('operador_negacao')
    p[0] = pai # operador negacao
    p[1] = criar_no('NAO', pai) # op -> nao
 
def p_vazio(p):
    ' vazio : '
    pai = criar_no('vazio') 
    p[0] = pai # vazio  
    pass     

def p_func_declaracao(p):
    ''' declaracao_funcao : tipo cabecalho
    | cabecalho
    '''
    pai = criar_no('declaracao_funcao')
    p[0] = pai # declaracao de funcao
    p[1].parent = pai # tipo
    if len(p) == 3:
        p[2].parent = pai # cabecalho
def p_func_declaracao_erro(p):
    ''' declaracao_funcao : error cabecalho
    | tipo error
    | error
    '''
    print ("Erro na geração da regra declaracao_funcao")

def p_cabecalho_func(p):
    ''' cabecalho : ID ABREPARENTESES lista_parametros FECHAPARENTESES corpo FIM'''
    global lista_funcoes_id
    lista_funcoes_id.append(p[1]) # armeza o id da funcao 
    pai = criar_no('cabecalho')
    p[0] = pai # cabecalho
    p[1] = criar_no('ID-' + p[1], pai, p.lineno(1)) # id
    p[2] = criar_no('ABREPARENTESES', pai) # (
    p[3].parent = pai # lista de parametros
    p[4] = criar_no('FECHAPARENTESES', pai) # )
    p[5].parent = pai # corpo
    p[6] = criar_no('FIM', pai) #fim

def p_cabecalho_func_erro(p):
    ''' cabecalho : ID ABREPARENTESES error FECHAPARENTESES corpo FIM
    | ID ABREPARENTESES lista_parametros FECHAPARENTESES error FIM
    '''
    print ("Erro na geração da regra declaracao_funcao")

def p_lista_parametros(p):
    ''' lista_parametros : lista_parametros VIRGULA lista_parametros
    | parametro
    | vazio
    '''
    pai = criar_no('lista_parametros')
    p[0] = pai # lista de parametros
    p[1].parent = pai 
    if len(p) > 2:
        p[2] = criar_no('VIRUGLA', pai)
        p[3].parent = pai # lista de parametros
def p_lista_parametros_erro(p):
    ''' lista_parametros : error VIRGULA lista_parametros
    | lista_parametros VIRGULA error
    | error
    '''
    print ("Erro na geração da regra lista_parametros")

def p_parametro(p):
    ''' parametro : tipo DOISPONTOS ID
    | parametro ABRECOLCHETE FECHACOLCHETE
    '''
    pai = criar_no('parametro')
    p[0] = pai # parametro
    p[1].parent = pai # : parametro
    if p[2] == ':':
        p[2] = criar_no('DOISPONTOS', pai) # 1 opc
        p[3] = criar_no('ID-' + p[3], pai, line=p.lineno(3))
    else:
        p[2] = criar_no('ABRECOLCHETE', pai) # 2 opc
        p[3] = criar_no('FECHACOLCHETE', pai, line=p.lineno(3))
def p_parametro_erro(p):
    ''' parametro : error DOISPONTOS ID
    | error ABRECOLCHETE FECHACOLCHETE
    '''
    print ("Erro na geração da regra parametro")

def p_corpo(p):
    ''' corpo : corpo acao
    | vazio
    | acao
    '''
    pai = criar_no('corpo')
    p[0] = pai # corpo
    p[1].parent = pai # corpo : corpo
    if len(p) == 3:
        p[2].parent = pai # acao
def p_corpo_erro(p):
    ''' corpo : error acao
    | corpo error
    | error
    '''
    print ("Erro na geração da regra corpo")

# funcao de erro
def p_erro(p): 
    # se for error de sintaxe    
    if p: 
        # mostra uma exeção indicando a linha e o token     
        # # print("Erro sintático na linha %d - Posição %d: '%s'" % (p.lineno, p.lexpos, p.value))     
        raise Exception("Erro sintático na linha {} no token '{}'".format(p.lineno, p.value))
    else: 
        # reinicia o parser    
        parser.restart()  
        print("Erro sintático nas definições!")
        exit(1)
        # gera uma  execao de erro
        raise Exception("Erro")  
 
def gera_raiz(): 
                # main 
        #  
        # ativa o parser  
        parser = yacc.yacc(debug=True, tabmodule='fooparsetab') 
        #recebe o arquivo com códgio tpp
        code = open(sys.argv[1]) 
        # le arquivo
        code_text = code.read() 
        # realiza a analise sintatica do código
        try:
                result = parser.parse(code_text, debug=False)  
                print('A raíz do programa: ',result) 
        except Exception as e:
                raise e 
        code.close()
        # se houver uma raiz então pode-se mostrar a ávore sintática dessa raiz 
        # se não houver uma raíz possui erro de construção sintática  
        if (raiz):   
                print("Gerando imagem da árvore...") 
                DotExporter(raiz).to_picture("arvore-sintatica1.png") 
                variaveis = tabela_simbolos(raiz)  
                print(variaveis)
                #trim_tree(raiz) 
                #DotExporter(raiz).to_picture('arvore_cortada.png')
                # semantica       
        else:
                raise Exception('Houve erro ao tentar gerar a árvore')
if __name__ == '__main__': 
        gera_raiz()