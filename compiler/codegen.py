from llvmlite import ir 
from parser import *
def code_gen(raiz, tableofsymbols): 
        module = ir.Module('meu_modulo.bc') 
        t_int = ir.IntType(32) 
        t_func = ir.FunctionType(t_int, ()) 
        for symbol in tableofsymbols: 
                if(symbol['token'] == 'ID'): 
                        if(symbol['escopo'] == 'global' and symbol['tipo'] == 'inteiro'):  
                                symbol['code'] = ir.GlobalVariable(module, ir.IntType(32),symbol['nome']) 
                                symbol['code'].initializer = ir.Constant(ir.IntType(32), 0) 
                                symbol['code'].linkage = "common"
                                            # Define o alinhamento em 4
                                symbol['code'].align = 4 
                        if(symbol['escopo'] == 'global' and symbol['tipo'] == 'flutuante'):  
                                symbol['code'] = ir.GlobalVariable(module, ir.FloatType(),symbol['nome']) 
                                symbol['code'].initializer = ir.Constant(ir.FloatType(), 0) 
                                symbol['code'].linkage = "common"
                                            # Define o alinhamento em 4
                                symbol['code'].align = 4        
                                            #print(symbol['nome'])      
        '''                            
        ''' 
        for symb in tableofsymbols: 
                if(symb['token']== 'func'): 
                        nomefuncao = symb['nome']   
                        funcao = ir.Function(module, t_func, name=symb['nome']) 
                        bb = funcao.append_basic_block('entry') 
                        builder = ir.IRBuilder(bb) 
                        for s in tableofsymbols: 
                                if s['token'] == 'ID' and s['escopo'] == nomefuncao: 
                                        if(s['tipo'] == 'inteiro'): 
                                                s['code'] = builder.alloca(ir.IntType(32), name=s['nome'])
                                                s['code'].align = 4
                        for node in LevelOrderIter(raiz): 
                                if(get_name(node) == 'cabecalho'):  
                                        # se eu achar o nome da funcao que eu quero
                                        if(get_last_value_name(node.children[0]) == symb['nome']):
                                                for retorno in LevelOrderIter(node): 
                                                        if(get_name(retorno) == 'retorna'): 
                                                                retornofuncao = get_last_value_name(retorno.children[2].children[0]) 
                                                corpo = node.children[4] 
                                                for n in LevelOrderIter(corpo): 
                                                        if(get_name(n) == 'atribuicao'): 
                                                                nomevar = get_last_value_name(n.children[0].children[0]) 
                                                                for t in tableofsymbols: 
                                                                        if t['nome'] == nomevar: 
                                                                                codename = t['code'] 
                                                                builder.store(ir.Constant(ir.IntType(32), get_last_value_name(n.children[2].children[0])), codename)

                        #print(nomefuncao,retornofuncao)                
        arquivo = open('vars.ll', 'w')
        arquivo.write(str(module))
        arquivo.close()
        print(module)                                                          