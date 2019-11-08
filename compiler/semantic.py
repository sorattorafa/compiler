from anytree import Node, LevelOrderIter, PreOrderIter  
import re  


# mostra o valor da variavel  
def get_last_value_name(node_param):
    return re.search('-(.)*', node_param.name).group(0)[1:len(node_param.name) + 1] 
# mostra o tipo da variável
def get_name(node_param):
    node_param_name = re.search('=(.)*', node_param.name).group(0)
    node_param_name = node_param_name[1:len(node_param_name)]
    haves_id = re.search('(.)*-', node_param_name)
    if haves_id:
        node_param_name = haves_id.group(0)
        node_param_name = node_param_name[:len(node_param_name) - 1]
    return node_param_name  

def get_var(node_param):
    node_param_name = re.search('=ID-(.)*', node_param.name).group(0)
    node_param_name = node_param_name[1:len(node_param_name)]
    haves_id = re.search('(.)*-', node_param_name)
    if haves_id:
        node_param_name = haves_id.group(0)
        node_param_name = node_param_name[:len(node_param_name) - 1]
    return node_param_name     

def trim_tree(root_param):
    for node_iter in LevelOrderIter(root_param):
        if len(node_iter.children) == 1:
            if node_iter.children[0].children:
                nod_name = get_name(node_iter)
                if nod_name != 'programa':
                    children = node_iter.children
                    parent = node_iter.parent
                    node_iter.children[0].parent = node_iter.parent
                    parent.children = tuple(list(parent.children)[0:len(parent.children) - 1])
                    list_children = list(node_iter.parent.children)
                    for i in range(len(list_children)):
                        if list_children[i] == node_iter:
                            list_children[i] = children[0]
                    node_iter.parent.children = tuple(list_children)
                    trim_tree(root_param)
                    break   
'''
store vars
'''             
def tabela_variaveis(root_param): 
    numero = 0 
    variaveis = []
    for node in PreOrderIter(root_param):
        node_name = get_name(node) 
        if node_name == 'declaracao_variaveis': 
            if(len(node.children[2].children[0].children) == 2): 
                if(len(node.children[2].children[0].children[1].children) == 4): 
                    dimensao = 2  
                else: 
                    dimensao = 1 
            else: 
                dimensao = 0
            # inteiro ou flutuante
            tipo = get_name(node.children[0].children[0])               
            token =  get_name(node.children[2].children[0].children[0]) 
            nome =  get_last_value_name(node.children[2].children[0].children[0]) 
            linha = node.children[2].children[0].children[0].line     
            variavel = {}  
            numero += 1 
            variavel['numero'] = numero
            variavel['tipo'] = tipo 
            variavel['token'] = token  
            variavel['nome'] = nome
            variavel['linha'] = linha 
            variavel['dimensao'] = dimensao 
            variavel['estado'] = 'inicializada' 
            if(variavel['nome'] not in variaveis): 
                variaveis.append(variavel) 
            else: 
                print('Variável ja definida anteriormente') 
        if (node_name == 'declaracao_funcao'): 
            funcao = {} 
            numero += 1 
            funcao['numero'] = numero 
            funcao['tipo'] = get_name(node.children[0].children[0])  
            funcao['token'] = 'func' 
            funcao['nome'] = get_last_value_name(node.children[1].children[0]) 
            funcao['linha'] = node.children[1].children[0].line 
            if(get_name(node.children[1].children[4].children[0]) == 'vazio'): 
                funcao['retorno'] = 'vazio' 
            if(get_name(node.children[1].children[4].children[0]) == 'corpo'): 
                funcao['retorno'] = get_name(node.children[1].children[4].children[1].children[0].children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0]) 
            else:  
                funcao['retorno'] = get_name(node.children[1].children[4].children[0].children[0].children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0])            
            funcao['estado'] = 'inicializada'         
            if(get_name(node.children[1].children[2].children[0]) == 'vazio'): 
                funcao['parametros-formais'] = 0  
            elif(get_name(node.children[1].children[2].children[0]) == 'parametro'): 
                funcao['parametros-formais'] = 1 
            else: 
                cont = 1 
                aux = node.children[1].children[2] 
                while(len(aux.children) != 1): 
                    aux = aux.children[2] 
                    cont += 1 
                funcao['parametros-formais'] = cont               
            variaveis.append(funcao)  
    return variaveis        
 
'''
if not main : error 
if main return not int : error
''' 
def verifica_main(tableofsymbols): 
    boole = 0 
    for symbol in tableofsymbols:  
        if(symbol['nome'] == 'principal'): 
            boole = 1 
    if(boole == 0): 
        raise Exception("Não existe uma função principal")          
    for symbol in tableofsymbols: 
        #print('Symbol!',symbol) 
        if(symbol['nome'] == 'principal' and symbol['token'] == 'func' and symbol['retorno']!= 'NUMERO_INTEIRO'): 
            raise Exception("A função principal da linha'{}' deveria retornar um inteiro. ".format(symbol['linha']))    
    #for symbol in tableofsymbols: 
    #    if(symbol['token'] == 'func' and symbol[''])                           
'''
verify return of all functions
'''  
def verify_functions(tableofsymbols,raiz): 
    for symbol in tableofsymbols: 
        if(symbol['tipo'] == 'inteiro' and symbol['token'] == 'func' and symbol['retorno'] != 'NUMERO_INTEIRO'): 
            raise Exception("Erro semântico na linha {} na função '{}'. A função inteiro não retorna um valor inteiro.".format(symbol['linha'], symbol['nome']))
        if(symbol['tipo'] == 'flutuante' and symbol['token'] == 'func' and symbol['retorno'] != 'NUMERO_PONTO_FLUTUANTE'): 
            raise Exception("Erro semântico na linha {} na função '{}'. A função flutuante não retorna um valor flutuante. ".format(symbol['linha'], symbol['nome'])) 
    for node in LevelOrderIter(raiz):
        if(get_name(node) == 'chamada_funcao'): 
            nomefuncao = get_last_value_name(node.children[0]) 
            boli = 0 
            for symbol in tableofsymbols: 
                if(nomefuncao == 'principal'): 
                    raise Exception("Erro: Chamada para a função principal não permitida.")     
                if(symbol['nome'] == nomefuncao): 
                    symbol['estado'] = 'utilizada'  
                    boli = 1       
            if(boli == 0): 
                raise Exception("Erro semântico. A função '{}' foi chamada sem ser definida formalmente".format(nomefuncao))             
            if (get_name(node.children[2].children[0]) == 'vazio'): 
                parametrosreais = 0 
                for symbol in tableofsymbols: 
                    if(symbol['nome'] == nomefuncao): 
                        symbol['parametros-reais'] = parametrosreais 
            elif(get_name(node.children[2].children[0]) == 'expressao'): 
                parametrosreais = 1 
                for symbol in tableofsymbols: 
                    if(symbol['nome'] == nomefuncao): 
                        symbol['parametros-reais'] = parametrosreais      
            else: 
                aux2 = 1    
                aux = node.children[2]  
                while(get_name(aux.children[0]) != 'expressao'): 
                    aux = aux.children[0] 
                    aux2 += 1 
                for symbol in tableofsymbols: 
                    if(symbol['nome'] == nomefuncao): 
                        symbol['parametros-reais'] = aux2      
            #parametrosreais  
    for symbol in tableofsymbols: 
        if(symbol['token'] == 'func' and symbol['parametros-formais'] != 0): 
            if(symbol['parametros-formais'] != symbol['parametros-reais']): 
                raise Exception("A função'{}' na linha {} é definida com {} parametros formais e chamada com {} ".format(symbol['nome'],symbol['linha'],symbol['parametros-formais'],symbol['parametros-reais'])) 
        if(symbol['token'] == 'func' and symbol['nome'] != 'principal' and symbol['estado'] != 'utilizada'): 
            raise Exception("Função {} na linha {} foi declarada e não utilizada".format(symbol['nome'], symbol['linha']))        