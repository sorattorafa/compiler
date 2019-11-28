from llvmlite import ir 
from parser import *
def code_gen(raiz, tableofsymbols):   
        nse = 0  
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
                                symbol['code'].initializer = ir.Constant(ir.FloatType(), 0.0) 
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
                                        if(s['tipo'] == 'flutuante'): 
                                                s['code'] = builder.alloca(ir.FloatType(), name=s['nome'])
                                                s['code'].align = 4        
                        for node in LevelOrderIter(raiz): 
                                if(get_name(node) == 'cabecalho'): 
                                        # se eu achar o nome da funcao que eu quero
                                        if(get_last_value_name(node.children[0]) == symb['nome']): 
                                                for retorno in LevelOrderIter(node): 
                                                        if(get_name(retorno) == 'retorna'): 
                                                                retornofuncao = get_last_value_name(retorno.children[2].children[0]) 
                                                corpo = node.children[4] 
                                                while len(corpo.children) != 0: 
                                                        corpo = corpo.children[0] 
                                                #print(get_name(corpo)) 
                                                while get_name(corpo.parent) != 'cabecalho': 
                                                        if get_name(corpo) == 'corpo': 
                                                                if(get_name(corpo.children[1]) == 'atribuicao'): 
                                                                        nomevar = get_last_value_name(corpo.children[1].children[0].children[0]) 
                                                                        for t in tableofsymbols: 
                                                                                if t['nome'] == nomevar and t['token'] == 'ID': 
                                                                                        codename = t['code']  
                                                                                        tipo = t['tipo'] 
                                                                        if(tipo == 'inteiro'):                 
                                                                                builder.store(ir.Constant(ir.IntType(32), get_last_value_name(corpo.children[1].children[2].children[0]) ), codename)         
                                                                        if(tipo == 'flutuante' and get_name(corpo.children[1].children[2]) == 'numero'): 
                                                                                #print(codename)  
                                                                                number = get_last_value_name(corpo.children[1].children[2].children[0])                                         
                                                                                builder.store( ir.Constant(ir.FloatType(), float(number)) , codename) 
                                                                        if(get_name(corpo.children[1].children[2]) == 'var'): 
                                                                                nomevariavel = get_last_value_name(corpo.children[1].children[2].children[0]) 
                                                                                for x in tableofsymbols: 
                                                                                        if x['nome'] == nomevariavel: 
                                                                                                builder.store(builder.load(x['code'],""), codename)          
                                                                if get_name(corpo.children[1]) == 'se': 
                                                                        nse += 1  
                                                                        iftrue = funcao.append_basic_block('iftrue_{}'.format(nse))
                                                                        iffalse = funcao.append_basic_block('iffalse_{}'.format(nse))
                                                                        ifend = funcao.append_basic_block('ifend_{}'.format(nse)) 
                                                                        
                                                                        if get_name(corpo.children[1].children[1].children[1].children[0]) == 'MAIOR': 
                                                                                var1 = get_last_value_name(corpo.children[1].children[1].children[0].children[0]) 
                                                                                var2 = get_last_value_name(corpo.children[1].children[1].children[2].children[0]) 
                                                                                aux1 = 0 
                                                                                aux2 = 0 
                                                                                for k in tableofsymbols: 
                                                                                        if k['nome'] == var1: 
                                                                                                a_cmp = builder.load(k['code'], 'a_cmp', align=4) 
                                                                                                aux1 = 1 
                                                                                        if k['nome'] == var2:  
                                                                                                b_cmp = builder.load(k['code'], 'b_cmp', align=4) 
                                                                                                aux2 = 1
                                                                                if(aux1 == 0): 
                                                                                        a_cmp = ir.Constant(ir.IntType(32), var1) 
                                                                                if(aux2 == 0):  
                                                                                        b_cmp = ir.Constant(ir.IntType(32), var2) 
                                                                                If_1 = builder.icmp_signed('>', a_cmp, b_cmp, name='if_test_1')
                                                                                builder.cbranch(If_1, iftrue, iffalse) 
                                                                                builder.position_at_end(iftrue) 
                                                                                for ny in LevelOrderIter(corpo.children[1].children[3]): 
                                                                                        if(get_name(ny) == 'atribuicao'): 
                                                                                                print(get_name(ny)) 
                                                                                                for sy in tableofsymbols: 
                                                                                                        if sy['nome'] == get_last_value_name(ny.children[0].children[0]) and sy['token'] == 'ID': 
                                                                                                                if get_name(ny.children[2]) == 'numero':                        
                                                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(ny.children[2].children[0])), sy['code'])
                                                                                builder.branch(ifend) 
                                                                                ## make the same way to else                                                  
                                                                        #print(get_name(corpo.children[1]))  
                                                                        

                                                        corpo = corpo.parent 
                        exitBasicBlock = funcao.append_basic_block('exit') 
                        #builder.branch(exitBasicBlock) 
                        builder = ir.IRBuilder(exitBasicBlock) 
                        booleano = 0                                         
                        for z in tableofsymbols: 
                                if z['nome'] == retornofuncao and z['token'] == 'ID' and z['tipo'] == 'inteiro':            
                                        returnVal_temp = builder.load(z['code'], name='ret_temp', align=4)   
                                        builder.ret(returnVal_temp) 
                                        booleano = 1 
                        if(booleano == 0):   
                                builder.ret(ir.Constant(ir.IntType(32), retornofuncao))

                        #  fazer o retorno da funcao               
        arquivo = open('root.ll', 'w')
        arquivo.write(str(module))
        arquivo.close()
        print(module)                                                          