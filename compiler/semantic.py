from anytree import Node, LevelOrderIter, PreOrderIter  
import re   

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

# guarda as variáveis                
def tabela_simbolos(root_param): 
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
            nome =  node.children[2].children[0].children[0].name 
            nome = nome[5:]
            linha = node.children[2].children[0].children[0].line     
            if (get_name(node.parent.parent.parent.parent) == 'programa' ): 
                escopo = 'global' 
            ## else verifica se está dentro de uma função     
            variavel = {}  
            numero += 1 
            variavel['numero'] = numero
            variavel['tipo'] = tipo 
            variavel['token'] = token  
            variavel['nome'] = nome
            variavel['linha'] = linha 
            variavel['escopo'] = escopo 
            variavel['dimensao'] = dimensao 
            variavel['estado'] = 'inicializada' 
            variaveis.append(variavel)       
    return variaveis        

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