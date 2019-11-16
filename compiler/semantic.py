from anytree import Node, LevelOrderIter, PreOrderIter  
import re  
 
# se a variável for declarada o estado é inicializada 
# se ela é utilizada o estado é utilizada 
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
        if node_name == 'declaracao_variaveis' and  len(node.children[2].children[0].children) == 3: 
        #    print('oi') 
            no_atual = node.children[2].children[0]
            while len(no_atual.children) > 1: 
                nome = get_last_value_name(no_atual.children[2].children[0]) 
                tipo = get_name(node.children[0].children[0]) 
                token = get_name(node.children[2].children[2].children[0]) 
                linha = no_atual.children[2].children[0].line 
                estado = 'inicializada' 
                if(get_name(node.parent) == 'declaracao'): 
                    escopo1 = 'global' 
                else: 
                    escopo = node 
                    while(get_name(escopo) != 'cabecalho'): 
                        escopo = escopo.parent 
                    escopo = get_last_value_name(escopo.children[0])     
                    escopo1 = escopo 
                dimensao1 = 0 
                indicereal1 = 0       
                numero += 1   
                variavel = {} 
                variavel['nome'] = nome 
                variavel['tipo'] = tipo 
                variavel['token'] = token 
                variavel['linha'] = linha 
                variavel['numero'] = numero 
                variavel['escopo'] = escopo1 
                variavel['dimensao'] = dimensao1 
                variavel['indice'] = indicereal1 
                variavel['estado'] = estado 
                existe = 0     
                for v in variaveis: 
                    if(v['nome'] == variavel['nome']): 
                        existe = 1 
                if(existe == 0):          
                    variaveis.append(variavel)            
                no_atual = no_atual.children[0]  

            nomex = get_last_value_name(no_atual.children[0].children[0]) 
            tipox = get_name(node.children[0].children[0]) 
            tokenx = get_name(no_atual.children[0].children[0]) 
            linhax = no_atual.children[0].children[0].line 
            estadox = 'inicializada' 
            if(get_name(node.parent) == 'declaracao'): 
                escopox = 'global' 
            else: 
                escopo = node 
                while(get_name(escopo) != 'cabecalho'): 
                    escopo = escopo.parent 
                escopo = get_last_value_name(escopo.children[0])     
                escopox = escopo 
            dimensaox = 0 
            indicerealx = 0       
            numero += 1  
            variavel = {} 
            variavel['nome'] = nomex 
            variavel['tipo'] = tipox 
            variavel['token'] = tokenx 
            variavel['linha'] = linhax 
            variavel['numero'] = numero 
            variavel['escopo'] = escopox 
            variavel['dimensao'] = dimensaox 
            variavel['indice'] = indicerealx
            variavel['estado'] = estadox 
            existe = 0     
            for v in variaveis: 
                if(v['nome'] == nomex): 
                    existe = 1 
            if(existe == 0):          
                variaveis.append(variavel) 

            nome = get_last_value_name(node.children[2].children[2].children[0]) 
            tipo = get_name(node.children[0].children[0]) 
            token = get_name(node.children[2].children[2].children[0])  
            linha = node.children[2].children[2].children[0].line 
            estado = 'inicializada' 
            if(get_name(node.parent) == 'declaracao'): 
                escopo1 = 'global' 
            else: 
                escopo = node 
                while(get_name(escopo) != 'cabecalho'): 
                    escopo = escopo.parent 
                escopo = get_last_value_name(escopo.children[0])     
                escopo1 = escopo 
            dimensao1 = 0 
            indicereal1 = 0       
            numero += 1  
            variavel = {} 
            variavel['nome'] = nome 
            variavel['tipo'] = tipo 
            variavel['token'] = token 
            variavel['linha'] = linha 
            variavel['numero'] = numero 
            variavel['escopo'] = escopo1 
            variavel['dimensao'] = dimensao1 
            variavel['indice'] = indicereal1 
            variavel['estado'] = estado 
            existe = 0     
            for v in variaveis: 
                if(v['nome'] == variavel['nome']): 
                    existe = 1 
            if(existe == 0):          
                variaveis.append(variavel)  

        if node_name == 'declaracao_variaveis' and len(node.children[2].children) == 3: 
            if(get_name(node.children[2].children[0].children[0]) == 'var'): 
                nome1 = get_last_value_name(node.children[2].children[0].children[0].children[0])
                tipo1 =  get_name(node.children[0].children[0]) 
                token1 =  get_name(node.children[2].children[0].children[0].children[0]) 
                linha1 = node.children[2].children[0].children[0].children[0].line 
                estado = 'inicializada'  
                if(get_name(node.parent) == 'declaracao'): 
                    escopo1 = 'global' 
                else: 
                    escopo = node 
                    while(get_name(escopo) != 'cabecalho'): 
                        escopo = escopo.parent 
                    escopo = get_last_value_name(escopo.children[0])     
                    escopo1 = escopo 
                dimensao1 = 0 
                indicereal1 = 0       
                numero += 1  
                variavel = {} 
                variavel['nome'] = nome1 
                variavel['tipo'] = tipo1 
                variavel['token'] = token1 
                variavel['linha'] = linha1 
                variavel['numero'] = numero 
                variavel['escopo'] = escopo1 
                variavel['dimensao'] = dimensao1 
                variavel['indice'] = indicereal1 
                variavel['estado'] = estado 
                existe = 0     
                for v in variaveis: 
                    if(v['nome'] == nome1): 
                        existe = 1 
                if(existe == 0):          
                    variaveis.append(variavel)                 
            if(get_name(node.children[2].children[0].children[0]) == 'var'): 
                nome2 = get_last_value_name(node.children[2].children[2].children[0]) 
                tipo2 =  get_name(node.children[0].children[0]) 
                token2 =  get_name(node.children[2].children[2].children[0])
                linha2 = node.children[2].children[2].children[0].line 
                estado2 = 'inicializada' 
                if(get_name(node.parent) == 'declaracao'): 
                    escopo2 = 'global' 
                else: 
                    escopo = node 
                    while(get_name(escopo) != 'cabecalho'): 
                        escopo = escopo.parent 
                    escopo = get_last_value_name(escopo.children[0])     
                    escopo2 = escopo 
                dimensao2 = 0 
                indicereal2 = 0       
                numero += 1 
                variavel = {} 
                variavel['nome'] = nome2 
                variavel['tipo'] = tipo2 
                variavel['token'] = token2 
                variavel['linha'] = linha2 
                variavel['numero'] = numero 
                variavel['escopo'] = escopo2 
                variavel['dimensao'] = dimensao2 
                variavel['indice'] = indicereal2 
                variavel['estado'] = estado2 
                existe = 0     
                for v in variaveis: 
                    if(v['nome'] == nome2): 
                        existe = 1 
                if(existe == 0):          
                    variaveis.append(variavel)  

        if node_name == 'declaracao_variaveis' and len(node.children[2].children) == 1:
            if(len(node.children[2].children[0].children) == 2): 
                if(get_name(node.children[2].children[0].children[1]) == 'indice'): 
                    for n in PreOrderIter(node.children[2].children[0].children[1]): 
                        if(get_name(n) ==  'numero'): 
                            if(get_name(n.children[0]) == 'NUMERO_PONTO_FLUTUANTE'): 
                                raise Exception("Indice do vetor '{}' da linha '{}' não pode ser Flutuante".format(get_last_value_name(node.children[2].children[0].children[0]), node.children[2].children[0].children[0].line)) 
                            else: 
                                indicereal = get_last_value_name(n.children[0]) 
            else: 
                indicereal = 0                                 
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
            variavel['indice'] = indicereal
            variavel['estado'] = 'inicializada' 
            if(get_name(node.parent) == 'declaracao'): 
                variavel['escopo'] = 'global'
            else: 
                escopo = node 
                while(get_name(escopo) != 'cabecalho'): 
                    escopo = escopo.parent 
                escopo = get_last_value_name(escopo.children[0])     
                variavel['escopo'] = escopo 
            existe = 0     
            for v in variaveis: 
                if(v['nome'] == variavel['nome']): 
                    existe = 1 
            if(existe == 0):          
                variaveis.append(variavel) 
            else: 
                print("Variável {} ja definida anteriormente na linha {}".format(variavel['nome'], variavel['linha'])) 
        if (node_name == 'declaracao_funcao'): 
            funcao = {} 
            numero += 1 
            funcao['numero'] = numero   
            funcao['token'] = 'func'  
            if(len(node.children) == 2): 
                funcao['tipo'] = get_name(node.children[0].children[0])
                funcao['nome'] = get_last_value_name(node.children[1].children[0]) 
                funcao['linha'] = node.children[1].children[0].line 
                retornobool = 0  
                for node2 in PreOrderIter(node): 
                    if(get_name(node2) == 'retorna'):  
                        for node3 in PreOrderIter(node2): 
                            if(get_name(node3) == 'var'): 
                                nomex = get_last_value_name(node3.children[0]) 
                                funcao['retorno'] = nomex
                            elif(get_name(node3) == 'numero'): 
                                funcao['retorno'] = get_name(node3.children[0])

                if(get_name(node.children[1].children[4].children[0]) == 'acao'): 
                    if(get_name(node.children[1].children[4].children[0].children[0]) != 'retorna'): 
                        raise Exception("Função {} sem retorno".format(funcao['nome']))
                if(get_name(node.children[1].children[4].children[0]) == 'vazio'): 
                    funcao['retorno'] = 'vazio' 
                    raise Exception("Função {} sem retorno".format(funcao['nome'])) 
                if(get_name(node.children[1].children[4].children[0].children[0]) != 'retorna' and get_name(node.children[1].children[4].children[1].children[0]) != 'retorna' ): 
                    raise Exception("Função {} sem retorno".format(funcao['nome']))              
                funcao['estado'] = 'inicializada'         
                if(get_name(node.children[1].children[2].children[0]) == 'vazio'): 
                    funcao['parametros-formais'] = 0    
                elif(get_name(node.children[1].children[2].children[0]) == 'parametro'): 
                    funcao['lista-parametros'] =  get_last_value_name(node.children[1].children[2].children[0].children[2])
                    funcao['parametros-formais'] = 1 
                else: 
                    cont = 1 
                    aux = node.children[1].children[2] 
                    funcao['lista-parametros'] = [] 
                    funcao['lista-parametros'] += get_last_value_name(aux.children[0].children[0].children[2]) 
                    while(len(aux.children) != 1): 
                        aux = aux.children[2] 
                        if(len(aux.children) == 1): 
                            funcao['lista-parametros'] += get_last_value_name(aux.children[0].children[2]) 
                        else: 
                            funcao['lista-parametros'] += get_last_value_name(aux.children[0].children[0].children[2])
                        cont += 1 
                    funcao['parametros-formais'] = cont  
            else: 
                funcao['tipo'] = 'vazio' 
                funcao['nome'] = get_last_value_name(node.children[0].children[0]) 
                funcao['linha'] = node.children[0].children[0].line 
                if(get_name(node.children[0].children[2].children[0]) == 'vazio'): 
                    funcao['parametros-formais'] = 0  
                existeretorno = 0
                for node2 in PreOrderIter(node): 
                    if(get_name(node2) == 'retorna'):  
                        for node3 in PreOrderIter(node2): 
                            if(get_name(node3) == 'var'): 
                                nomex = get_last_value_name(node3.children[0]) 
                                funcao['retorno'] = nomex 
                                existeretorno = 1
                            elif(get_name(node3) == 'numero'): 
                                funcao['retorno'] = get_name(node3.children[0]) 
                                existeretorno = 1 
                if(existeretorno == 1): 
                    raise Exception("A função {} é do tipo void e possui um valor de retorno = {}".format(funcao['nome'], funcao['retorno']))                         
            funcaodeclarada = 0 
            for variavel in variaveis: 
                if(variavel['token'] == 'func' and variavel['nome'] == funcao['nome']): 
                    funcaodeclarada = 1  
            if(funcaodeclarada == 1): 
                raise Exception("Função '{}' já foi declarada anteriormente".format(funcao['nome'])) 
            else:  
                variaveis.append(funcao)  
    return variaveis        
 
'''
if not main : error 
if main return not int : error
''' 
def verify_main(tableofsymbols):  
    boole = 0 
    for symbol in tableofsymbols:  
        if(symbol['nome'] == 'principal'): 
            boole = 1 
    if(boole == 0): 
        raise Exception("Não existe uma função principal")                              
'''
verify return of all functions
'''  
def verify_functions(tableofsymbols,raiz):  
    for symbol in tableofsymbols:  
        if(symbol['token'] == 'func'):    
            for node in LevelOrderIter(raiz): 
                if(get_name(node) == 'declaracao_funcao'): 
                    if(len(node.children) == 2): 
                        if(get_last_value_name(node.children[1].children[0]) == symbol['nome']): 
                            for node2 in LevelOrderIter(node): 
                                if(get_name(node2) == 'parametro'): 
                                    if(get_last_value_name(node2.children[2]) == symbol['retorno']): 
                                        symbol['retorno'] = get_name(node2.children[0].children[0]) 
                    else: 
                        if(get_last_value_name(node.children[0].children[0]) == symbol['nome']): 
                            for node2 in LevelOrderIter(node): 
                                if(get_name(node2) == 'parametro'): 
                                    if(get_last_value_name(node2.children[2]) == symbol['retorno']): 
                                        symbol['retorno'] = get_name(node2.children[0].children[0])                     
    for symbol in tableofsymbols: 
        if(symbol['token'] == 'func' and symbol['tipo'] != 'vazio'): 
            if(symbol['parametros-formais'] != 0): 
                for l in symbol['lista-parametros']:  
                    for node in LevelOrderIter(raiz): 
                        if(get_name(node) == 'parametro'): 
                            if(get_last_value_name(node.children[2]) == l): 
                                if(symbol['tipo'] != get_name(node.children[0].children[0])):
                                    print("Aviso! Função {} do tipo {} recebe um {}".format(symbol['nome'], symbol['tipo'], get_name(node.children[0].children[0]) )) 
                     

    for symbol in tableofsymbols: 
        if(symbol['tipo'] == 'inteiro' and symbol['token'] == 'func'): 
            for s in tableofsymbols: 
                if(s['nome'] == symbol['retorno']): 
                    symbol['retorno'] = s['tipo'] 
        if(symbol['token'] == 'func' and symbol['tipo'] == 'inteiro'): 
            if(symbol['retorno'] != 'inteiro' and symbol['retorno'] != 'NUMERO_INTEIRO'): 
                raise Exception("Erro na função {} do tipo {} retorna um {}. Tipo incompatível!".format(symbol['nome'], symbol['tipo'], symbol['retorno'])) 
        if(symbol['token'] == 'func' and symbol['tipo'] == 'flutuante'):     
            if(symbol['retorno'] != 'flutuante' and symbol['retorno'] != 'NUMERO_PONTO_FLUTUANTE'): 
                raise Exception("Erro na função {} do tipo {} retorna um {}".format(symbol['nome'], symbol['tipo'], symbol['retorno']))              
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
            listaparametros = node.children[2]  
            nparams = 0 
            if get_name(node.children[2].children[0]) != 'vazio': 
                for nx in LevelOrderIter(listaparametros): 
                    if(get_name(nx) == 'chamada_funcao'): 
                        nparams = 0 
                    if(get_name(nx) == 'expressao'): 
                        nparams += 1       
            for symbol in tableofsymbols: 
                if(symbol['nome'] == get_last_value_name(node.children[0]) and symbol['token'] == 'func'): 
                    symbol['parametros-reais'] = nparams 
            for symbol in tableofsymbols: 
                print(symbol)  
                if(symbol['token'] == 'func' and symbol['parametros-formais'] != 0  and 'parametros-reais' in symbol and symbol['parametros-formais'] != symbol['parametros-reais']): 
                    raise Exception("Função {} é chamada com o número de parametros {} porém ela foi definida com {} parametros formais".format(symbol['nome'], symbol['parametros-reais'], symbol['parametros-formais']))        
            #parametrosreais  
    for symbol in tableofsymbols:  
        if(symbol['token'] == 'func' and symbol['nome'] != 'principal' and symbol['estado'] != 'utilizada'): 
            print("Aviso! Função {} na linha {} foi declarada e não utilizada".format(symbol['nome'], symbol['linha'])) 
def verify_variables(tableofsymbols,raiz): 
    parametros = [] 
    for n in LevelOrderIter(raiz): 
        if get_name(n) == 'parametro': 
            nome = get_last_value_name(n.children[2]) 
            parametros.append(nome) 
    # salvar uma lista de parametros para verificar sua inicializacao antes da atribuição   
    for symbol in tableofsymbols: 
        if(symbol['token'] == 'ID'): 
            for node in LevelOrderIter(raiz): 
                if(get_name(node) == 'cabecalho'): 
                    if(get_last_value_name(node.children[0]) == symbol['escopo'] or symbol['escopo'] == 'global'): 
                        if(get_name(node.children[4].children[0]) != 'acao'): 
                            aux = node.children[4].children[0] 
                            for node2 in LevelOrderIter(aux): 
                                if(get_name(node2) == 'atribuicao'): 
                                    if(get_last_value_name(node2.children[0].children[0]) == symbol['nome']): 
                                        symbol['estado'] = 'utilizada'  
                                    for node3 in LevelOrderIter(node2):       
                                        if(get_name(node3) == 'var'): 
                                            booleano = 0  
                                            for s in tableofsymbols: 
                                                if(s['nome'] == get_last_value_name(node3.children[0])): 
                                                    booleano = 1 
                                            if(booleano == 0): 
                                                raise Exception("A variavel {} foi utilizada porém não foi definida formalmente".format(get_last_value_name(node3.children[0])))            
    for symbol in tableofsymbols: 
        if(symbol['token'] == 'ID'): 
            for node in LevelOrderIter(raiz):  
                if(get_name(node) == 'atribuicao'): 
                    for node2 in LevelOrderIter(node): 
                        if(get_name(node2) == 'var'): 
                            if(symbol['nome'] == get_last_value_name(node2.children[0])): 
                                symbol['estado'] = 'utilizada' 

    for symbol in tableofsymbols: 
        if(symbol['token'] == 'ID' and symbol['estado'] == 'inicializada'): 
            print("Aviso! Variavel '{}' da linha {} foi declarada porém não utilizada".format(symbol['nome'], symbol['linha']))  
    for node in LevelOrderIter(raiz):  
        if(get_name(node) == 'atribuicao'): 
            declarada = 0   
            for symbol in tableofsymbols: 
                if(symbol['token'] == 'ID' and symbol['nome'] == get_last_value_name(node.children[0].children[0])): 
                    declarada = 1 
                if get_last_value_name(node.children[0].children[0]) in parametros: 
                    declarada = 1              
            if(declarada == 0): 
                raise Exception("A variavel '{}' foi utilizada na linha {} porém não foi definida formalmente.".format(get_last_value_name(node.children[0].children[0]), symbol['linha'])) 
def verify_index_var(tableofsymbols, raiz):  
    for no in LevelOrderIter(raiz): 
        if(get_name(no) == 'atribuicao'):  
            if(len(no.children[0].children) == 2): 
                nomei = get_last_value_name(no.children[0].children[0])  
                if(get_name(no.children[0].children[1]) == 'indice'): 
                    for no2 in LevelOrderIter(no.children[0].children[1]): 
                        if(get_name(no2) == 'numero'): 
                            if(get_name(no2.children[0]) == 'NUMERO_PONTO_FLUTUANTE'): 
                                raise Exception("A atribuição do um array '{}' na linha '{}' não pode ter indíce do tipo flutuante".format(nomei, no.children[0].children[0].line)) 
                            indexreal = get_last_value_name(no2.children[0])  
                for s in tableofsymbols: 
                    if(s['nome'] == nomei): 
                        if(s['indice'] < indexreal): 
                            raise Exception('Índice da variavel {} foi excedido na atribuição'.format(s['nome']))

def verify_assignments(tableofsymbols,raiz): 
    parametros = [] 
    for n in LevelOrderIter(raiz): 
        if get_name(n) == 'parametro': 
            nome = get_last_value_name(n.children[2]) 
            tipo = get_name(n.children[0].children[0]) 
            parametro = {} 
            parametro['nome'] = nome 
            parametro['tipo'] = tipo  
            parametros.append(parametro) 
    for node in LevelOrderIter(raiz): 
        if(get_name(node) == 'atribuicao'): 
            linha =  node.children[0].children[0].line
            var = get_last_value_name(node.children[0].children[0]) 
           # print(var)  
            b = 0
            for symbol in tableofsymbols: 
                if(symbol['nome'] == var and symbol['escopo']): 
                    tipoatribuicao = symbol['tipo'] 
                    nome = var 
                    b = 1 
            if(b == 0): 
                for p in parametros: 
                    if p['nome'] == var: 
                        tipoatribuicao = p['tipo']

            for node2 in LevelOrderIter(node.children[2]): 
                if(get_name(node2) == 'chamada_funcao'): 
                    nomefuncao = get_last_value_name(node2.children[0]) 
                    for s in tableofsymbols: 
                        if(s['nome'] == nomefuncao): 
                            tipoutilizado = s['tipo'] 
                            nome2 = nomefuncao 
                if(get_name(node2) == 'numero'): 
                    tipoutilizado = get_name(node2.children[0])              
                if(get_name(node2) == 'var'): 
                    nomevar = get_last_value_name(node2.children[0]) 
                    for s in tableofsymbols: 
                        if(s['token'] == 'ID' and s['nome'] == nomevar): 
                            tipoutilizado = s['tipo'] 
                            nome2 = nomevar  
            if(tipoutilizado == 'NUMERO_INTEIRO' or tipoutilizado == 'inteiro'): 
                if(tipoatribuicao == 'flutuante' or tipoatribuicao == 'NUMERO_PONTO_FLUTUANTE'): 
                   print(" Aviso! A Variável {} é '{}' e recebe {} na linha {}".format(var,tipoatribuicao, tipoutilizado, linha))  
            if(tipoutilizado == 'NUMERO_PONTO_FLUTUANTE' or tipoutilizado == 'flutuante'): 
                if(tipoatribuicao == 'inteiro' or tipoatribuicao == 'NUMERO_INTEIRO'): 
                   print("Aviso! A Variável {} é '{}' e recebe {} na linha {}".format(var,tipoatribuicao, tipoutilizado, linha))                         
    for symbol in tableofsymbols: 
        print(symbol['nome'], ':',symbol) 