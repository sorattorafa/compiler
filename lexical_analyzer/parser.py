# coding=utf-8  
# dependencias utilizadas no python3
#from ast import AST
from ply import yacc
from lexer import tokens
from anytree import Node 
import sys 
from anytree.exporter import DotExporter   

# variáveis auxiliares para criação da árvore
contador = 0  # utilizado para indicar o número do nó criado
raiz = None # raiz
funcoes_id = [] 

# p.lineno(num). Return the line number for symbol num
# p.lexpos(num). Return the lexing position for symbol num 
 
# declaracao de variaveis 
def criar_variavel(pai,line2,t): 
    # get contador atual    
    global contador   
    # var : contador - ID -  nome da variável
    var = Node(str(contador) + '#' + 'ID-' + t[1], parent=pai, line=line2) 
    # retorna var
    return var        

# arvore sintática é implementada com nós 
# um nó tem as seguintes informacoes: 
# (número # nome_da_regra) 
def criar_no(name, parent=None, line=None):
    global contador
    contador += 1 
    # estrutura para mostrar o número e o tipo do nó
    if parent and line:
        return Node( str(contador) + '#' + name, parent=parent, line=line) # ID
    elif parent:
        return Node(str(contador) + '#' + name, parent=parent)
    else:
        return Node(str(contador) + '#' + name) 
 
# primeiro nó raiz  
def p_programa(p):
    """ programa : lista_declaracoes """
    global raiz 
    raiz = criar_no('programa-raiz')  # cria um nó raiz
    p[0] = raiz # atribui ele pra raiz t[0]
    # atribui a lista de declarações como filho do programa
    p[1].parent = raiz  
    
# erro ao criar o primeiro no    
def p_programa_erro(t):
    """ programa : error"""
    print ("Erro na regra programa")  

# segundo nó (programa->lista de declaracoes)    
def p_lista_declaracoes(t):
    ''' lista_declaracoes : lista_declaracoes declaracao
    | declaracao
    '''
    pai = criar_no('lista_declaracoes') 
    # programa->lista_declaracoes
    t[0] = pai 
    t[1].parent = pai
    if len(t) > 2:
        t[2].parent = pai 
def p_lista_declaracoes_erro(t):
    """ lista_declaracoes : error declaracao"""
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
    # se tiver indice
    if len(t) > 2:
        t[2].parent = pai
def p_variavel_erro(t):
    ''' var : ID error '''
    print ("Erro na regra de var")

def p_indice(t):
    ''' indice : indice ABRECOLCHETE expressao FECHACOLCHETE
    | ABRECOLCHETE expressao FECHACOLCHETE
    ''' 
    # utilizado em vetores e matrizes para saber o indice
    pai = criar_no('indice')
    t[0] = pai 
    #vetores
    if len(t) == 4:
        t[1] = criar_no('ABRECOLCHETE', pai)
        t[2].parent = pai
        t[3] = criar_no('FECHACOLCHETE', pai) 
    # matrizes    
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
    pai = criar_no('tipo') # tipo
    t[0] = pai
    t[1] = criar_no(t[1].upper(), pai) # tipo -> inteiro ou flutuante

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
    t[0] = pai # acao
    t[1].parent = pai # acao -> expressao
def p_acao_erro(t):
    ''' acao : error'''
    print ("Erro na geração da regra acao")


def p_repita(t):
    ''' repita : REPITA corpo ATE expressao'''
    pai = criar_no('repita')
    t[0] = pai # repita
    t[1] = criar_no('REPITA', pai) # repita -> REPITA
    t[2].parent = pai # corpo
    t[3] = criar_no('ATE', pai, t.lineno(3))
    t[4].parent = pai # expressao
def p_repita_erro(t):
    ''' repita : REPITA corpo ATE error
    | REPITA error ATE expressao
    '''
    print ("Erro na geração da regra repita")

def p_atribuicao(t):
    ''' atribuicao : var ATRIBUICAO expressao'''
    pai = criar_no('atribuicao')
    t[0] = pai # atribuição 
    t[1].parent = pai # atribuicao -> var
    t[2] = criar_no('ATRIBUICAO', pai)
    t[3].parent = pai # expressao
def p_atribuicao_erro(t):
    ''' atribuicao : var ATRIBUICAO error
    | error ATRIBUICAO expressao
    '''
    print('Erro na geração da regra de atribuicao')

def p_leia(t):
    ''' leia : LEIA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('leia')
    t[0] = pai # leia
    t[1] = criar_no('LEIA', pai)
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai # expressao
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_leia_erro(t):
    ''' leia : LEIA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")

def p_escreva(t):
    ''' escreva : ESCREVA ABREPARENTESES expressao FECHAPARENTESES'''
    pai = criar_no('escreva')
    t[0] = pai # escreva
    t[1] = criar_no('ESCREVA', pai)
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai # expressao
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_escreva_erro(t):
    ''' escreva : ESCREVA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra leia")
 
def p_se(t):
    ''' se : SE expressao ENTAO corpo FIM
    | SE expressao ENTAO corpo SENAO corpo FIM
    '''
    pai = criar_no('se')
    t[0] = pai # se
    t[1] = criar_no('SE', pai, t.lineno(1)) # se -> SE
    t[2].parent = pai # se -> SE expressao
    t[3] = criar_no('ENTAO', pai) # se-> SE Expressao Então
    t[4].parent = pai # corpo
    # se tiver um senão
    if len(t) == 8:
        t[5] = criar_no('SENAO', pai)
        t[6].parent = pai # corpo
        t[7] = criar_no('FIM', pai) 
    # fim sem o senão
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
    
def p_retorna(t):
    ''' retorna : RETORNA ABREPARENTESES expressao FECHAPARENTESES '''
    pai = criar_no('retorna')
    t[0] = pai # retorna
    t[1] = criar_no('RETORNA', pai, t.lineno(1))
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai # expressao
    t[4] = criar_no('FECHAPARENTESES', pai)
def p_retorna_erro(t):
    ''' retorna : RETORNA ABREPARENTESES error FECHAPARENTESES'''
    print ("Erro na geração da regra retorna")

def p_expressao(t):
    ''' expressao : expressao_logica
    | atribuicao
    '''
    pai = criar_no('expressao')
    t[0] = pai # expressao
    t[1].parent = pai # expressao -> expressao_logica
def p_expressao_erro(t):
    ''' expressao : error'''
    print ("Erro na geração da regra expressao")

def p_expressao_logica(t):
    ''' expressao_logica : expressao_simples
    | expressao_logica operador_logico expressao_simples
    '''
    pai = criar_no('expressao_logica')
    t[0] = pai
    t[1].parent = pai # expressao_logica -> expressao_simples 
    # operador logico
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
    t[0] = pai # expressao_simples
    t[1].parent = pai # expressao_aditiva 
    # operador relacional
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
    t[0] = pai # expressao aditiva
    t[1].parent = pai # expressao multiplicativa 
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
    t[0] = pai  # expressao multiplicativa
    t[1].parent = pai # expressao unaria 
    # expressao multiplicativa
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
    t[0] = pai # expressao unaria 
    # se for a negacao
    if t[1] == '!':
        t[1] = criar_no('NAO', pai) 
    # senao     
    else:
        t[1].parent = pai # fator 
    # operador soma    
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
    t[0] = pai # operador 
    # se for multiplicacao
    if t[1] == '*':
        t[1] = criar_no('MULTIPLICACAO', pai) 
    # se for divisao    
    else:
        t[1] = criar_no('DIVISAO', pai)

def p_fator(t):
    ''' fator : ABREPARENTESES expressao FECHAPARENTESES
    | var
    | chamada_funcao
    | numero
    '''
    pai = criar_no('fator')
    t[0] = pai # fator
    if len(t) > 2:
        t[1] = criar_no('ABREPARENTESES', pai)
        t[2].parent = pai # expressao
        t[3] = criar_no('FECHAPARENTESES', pai)
    else:
        t[1].parent = pai # chamada de funcao ou var ou numero

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
    t[0] = pai # NUMERO 
    # se não tiver a parte decimal então é inteiro
    if t[1].find('.') == -1:
        t[1] = criar_no('NUMERO_INTEIRO-' + t[1], pai)
    else: 
    # se tiver decimais é flutuante        
        t[1] = criar_no('NUMERO_PONTO_FLUTUANTE-' + t[1], pai)

def p_chamada_funcao(t):
    ''' chamada_funcao : ID ABREPARENTESES lista_argumentos FECHAPARENTESES
    '''
    pai = criar_no('chamada_funcao')
    t[0] = pai # chamada de funcao
    t[1] = criar_no('ID-' + t[1], pai, line=t.lineno(1)) # ID
    t[2] = criar_no('ABREPARENTESES', pai)
    t[3].parent = pai # lsta de argumentos
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
   
# relacao entre numeros   
def p_operador_relacional(t):
    ''' operador_relacional : MENOR
    | MAIOR
    | IGUALDADE
    | DIFERENTE
    | MENORIGUAL
    | MAIORIGUAL
    '''
    pai = criar_no('operador_relacional')
    t[0] = pai # t[0] -> op relacional
    if t[1] == '<':
        t[1] = criar_no('MENOR', pai) # op relacional -> menor
    elif t[1] == '<>':
        t[1] = criar_no('DIFERENTE', pai) # op relacional -> diferente
    elif t[1] == '>=':
        t[1] = criar_no('MAIOR_GUAL', pai) # op relacional -> maior igual 
    elif t[1] == '>':
        t[1] = criar_no('MAIOR', pai) # op relacional -> maior
    elif t[1] == '=':
        t[1] = criar_no('IGUALDADE', pai) # op relacional -> igual    
    else:
        t[1] = criar_no('MENORIGUAL', pai) # # op relacional -> menor igual
# operador aritmetico
def p_operador_soma(t):
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
 
def p_vazio(t):
    ' vazio : '
    pai = criar_no('vazio') 
    t[0] = pai # vazio  
    pass     

# funcao de erro
def p_erro(t): 
    # se for error de sintaxe    
    if t: 
        # mostra uma exeção indicando a linha e o token     
        # # print("Erro sintático na linha %d - Posição %d: '%s'" % (p.lineno, p.lexpos, p.value))     
        raise Exception("Erro sintático na linha {} no token '{}'".format(t.lineno, t.value))
    else: 
        # reinicia o parser    
        parser.restart()  
        print("Erro sintático nas definições!")
        exit(1)
        # gera uma  execao de erro
        raise Exception("Erro") 

def p_func_declaracao(t):
    ''' declaracao_funcao : tipo cabecalho
    | cabecalho
    '''
    pai = criar_no('declaracao_funcao')
    t[0] = pai # declaracao de funcao
    t[1].parent = pai # tipo
    if len(t) == 3:
        t[2].parent = pai # cabecalho
def p_func_declaracao_erro(t):
    ''' declaracao_funcao : error cabecalho
    | tipo error
    | error
    '''
    print ("Erro na geração da regra declaracao_funcao")

def p_cabecalho_func(t):
    ''' cabecalho : ID ABREPARENTESES lista_parametros FECHAPARENTESES corpo FIM'''
    global funcoes_id
    funcoes_id.append(t[1]) # armeza o id da funcao 
    pai = criar_no('cabecalho')
    t[0] = pai # cabecalho
    t[1] = criar_no('ID-' + t[1], pai, t.lineno(1)) # id
    t[2] = criar_no('ABREPARENTESES', pai) # (
    t[3].parent = pai # lista de parametros
    t[4] = criar_no('FECHAPARENTESES', pai) # )
    t[5].parent = pai # corpo
    t[6] = criar_no('FIM', pai) #fim

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
    t[0] = pai # lista de parametros
    t[1].parent = pai 
    if len(t) > 2:
        t[2] = criar_no('VIRUGLA', pai)
        t[3].parent = pai # lista de parametros
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
    t[0] = pai # parametro
    t[1].parent = pai # : parametro
    if t[2] == ':':
        t[2] = criar_no('DOISPONTOS', pai) # 1 opc
        t[3] = criar_no('ID-' + t[3], pai, line=t.lineno(3))
    else:
        t[2] = criar_no('ABRECOLCHETE', pai) # 2 opc
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
    t[0] = pai # corpo
    t[1].parent = pai # corpo : corpo
    if len(t) == 3:
        t[2].parent = pai # acao
def p_corpo_erro(t):
    ''' corpo : error acao
    | corpo error
    | error
    '''
    print ("Erro na geração da regra corpo")

if __name__ == '__main__': 
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
                DotExporter(raiz).to_picture("arvore-sintatica.png") 
        else:
                raise Exception('Houve erro ao tentar gerar a árvore')