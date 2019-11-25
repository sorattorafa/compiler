from llvmlite import ir 
from parser import *
def code_gen(raiz, tableofsymbols):
        module = ir.Module('meu_modulo.bc') 
        for symbol in tableofsymbols: 
                if(symbol['token'] == 'ID'): 
                        if(symbol['escopo'] == 'global'): 
                                symbol['code'] = ir.GlobalVariable(module, ir.IntType(32),symbol['nome']) 
                                symbol['code'].initializer = ir.Constant(ir.IntType(32), 0) 
                                symbol['code'].linkage = "common"
                                            # Define o alinhamento em 4
                                symbol['code'].align = 4
                                            #print(symbol['nome']) 
        for symbol in tableofsymbols: 
                if(symbol['token'] == 'func' and symbol['nome'] == 'principal'): 
                        for node in LevelOrderIter(raiz): 
                                name = get_name(node) 
                                if(name == 'declaracao_funcao'): 
                                        if(get_last_value_name(node.children[1].children[0]) == 'principal'):
                                                for node2 in LevelOrderIter(node):                                                          
                                                        if(get_name(node2) == 'retorna'): 
                                                                            #print(get_last_value_name(node2.children[2].children[0])) 
                                                                retornoprincipal = get_last_value_name(node2.children[2].children[0]) 
                                                                            ## define o retorno da funcao main
                                                                Zero32 = ir.Constant(ir.IntType(32), retornoprincipal) 
                                                                            # Cria função main
                                                                t_func_main = ir.FunctionType(ir.IntType(32), ()) 
                                                                            # Declara função main
                                                                main = ir.Function(module, t_func_main, name='main') 
                                                                            # Declara o bloco de entrada
                                                                entryBlock = main.append_basic_block('entry')
                                                                endBasicBlock = main.append_basic_block('exit')

                                                                            # Adiciona o bloco de entrada
                                                                builder = ir.IRBuilder(entryBlock)

                                                                            # Cria o valor de retorno e inicializa com zero
                                                                returnVal = builder.alloca(ir.IntType(32), name='retorno')
                                                                builder.store(Zero32, returnVal) 
                                                                for s in tableofsymbols: 
                                                                        if(s['token'] == 'ID'): 
                                                                                s['code'] = builder.alloca(ir.IntType(32), name=s['nome'])
                                                                                            # Define o alinhamento
                                                                                s['code'].align = 4  
                                                                                            # gerar atribuicao 
                                                                                for no in LevelOrderIter(node): 
                                                                                        if(get_name(no) == 'atribuicao'):  
                                                                                                            #print('atribuicao', get_last_value_name(no.children[0].children[0]))
                                                                                                            # Cria uma constante pra armazenar o numero 1 
                                                                                                if(s['nome'] == get_last_value_name(no.children[0].children[0])): 
                                                                                                        print(s['nome'])
                                                                                                        num1 = ir.Constant(ir.IntType(32),get_last_value_name(no.children[2].children[0]))
                                                                                                                    # Armazena o 1 na variave 'a'
                                                                                                        builder.store(num1, s['code'])                                                          
                                                                            # Cria um salto para o bloco de saída
                                                                builder.branch(endBasicBlock)

                                                                            # Adiciona o bloco de saida
                                                                builder.position_at_end(endBasicBlock)

                                                                            # return 0
                                                                            # Cria o return
                                                                returnVal_temp = builder.load(returnVal, name='', align=4)
                                                                builder.ret(returnVal_temp)   

                                                        #if(get_name(node2) == 'SE'):                                         
        arquivo = open('vars.ll', 'w')
        arquivo.write(str(module))
        arquivo.close()
        print(module)                                                          