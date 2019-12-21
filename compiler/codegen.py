from llvmlite import ir 
from main import *  
from llvmlite import binding as llvm 

def code_gen(raiz, tableofsymbols): 
        printaux = 0    
        printaux2 = 0  
        operacao = 0 
        lastaux = 0 
        subaux = 0
        ponteiroaux = None  
        nse = 0   
        llvm.initialize()
        llvm.initialize_all_targets()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter() 

        module = ir.Module('geracao-codigo-tpp.bc')  
        module.triple = llvm.get_default_triple()

        target = llvm.Target.from_triple(module.triple)
        target_machine = target.create_target_machine()  

        llvm.load_library_permanently('./io.so')
        module.data_layout = target_machine.target_data  
         
        leiaInteiro = ir.Function(module,ir.FunctionType(ir.IntType(32),[]),name="leiaInteiro")  
        leiaFlutuante = ir.Function(module,ir.FunctionType(ir.FloatType(),[]),name="leiaFlutuante") 
        escreva =  ir.FunctionType(ir.VoidType(), [ir.IntType(32)]) 
        escrevafloat =  ir.FunctionType(ir.VoidType(), [ir.FloatType()])
        plh_print = ir.Function(module, escreva, 'escrevaInteiro')    
        plh_print_float = ir.Function(module, escrevafloat, 'escrevaFlutuante')   


        t_int = ir.IntType(32) 
        t_func = ir.FunctionType(t_int, ()) 
        for symbol in tableofsymbols: 
                if(symbol['token'] == 'ID'): 
                        if(symbol['escopo'] == 'global' and symbol['tipo'] == 'inteiro'):  
                                symbol['code'] = ir.GlobalVariable(module, ir.IntType(32),symbol['nome']) 
                                symbol['code'].initializer = ir.Constant(ir.IntType(32), 0) 
                                symbol['code'].linkage = "common"
                                symbol['code'].align = 4 
                        if(symbol['escopo'] == 'global' and symbol['tipo'] == 'flutuante'):  
                                symbol['code'] = ir.GlobalVariable(module, ir.FloatType(),symbol['nome']) 
                                symbol['code'].initializer = ir.Constant(ir.FloatType(), 0.0) 
                                symbol['code'].linkage = "common"
                                symbol['code'].align = 4              
        for symb in tableofsymbols: 
                if(symb['token']== 'func'): 
                        if('lista-parametros' in symb): 
                                i = 0 
                                t_soma = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
                                funcao = ir.Function(module, t_soma, symb['nome']) 
                                nomefuncao = symb['nome'] 
                                symb['codigo'] = funcao   
                                for parametro in symb['lista-parametros']:
                                        funcao.args[i].name = parametro
                                        i += 1 
                                bb = funcao.append_basic_block('entry')  
                                builder = ir.IRBuilder(bb)        
                        else:
                                nomefuncao = symb['nome'] 
                                if symb['nome'] == 'principal': 
                                        funcao = ir.Function(module, t_func, name='main') 
                                else:                   
                                        funcao = ir.Function(module, t_func, name=symb['nome'])  
                                symb['codigo'] = funcao 
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
                                                        if(get_name(retorno) == 'retorna' and get_name(retorno.children[2]) == 'var'): 
                                                                if(get_name(retorno.children[2]) == 'var'): 
                                                                        for ks in tableofsymbols: 
                                                                                if ks['nome'] == get_last_value_name(retorno.children[2].children[0]): 
                                                                                        if 'code' in ks:
                                                                                                retornofuncao = ks['nome'] 
                                                                                        else:  
                                                                                                retornofuncao = 0          
                                                                if(get_name(retorno.children[2]) == 'numero'): 
                                                                        retornofuncao = get_last_value_name(retorno.children[2].children[0]) 
                                                                if(get_name(retorno.children[2]) == 'expressao_aditiva'):   
                                                                        for simbolo in tableofsymbols: 
                                                                                if simbolo['nome'] == get_last_value_name(retorno.children[2].children[0].children[0]): 
                                                                                        loadvar1 =  builder.alloca(ir.IntType(32), name=simbolo['nome'])  
                                                                                if simbolo['nome'] == get_last_value_name(retorno.children[2].children[2].children[0]): 
                                                                                        loadvar2 =  builder.alloca(ir.IntType(32), name=simbolo['nome']) 
                                                                                if get_last_value_name(retorno.children[2].children[2].children[0]) == 't': 
                                                                                        loadvar2 = builder.alloca(ir.IntType(32), name='t')         
                                                                        if(get_name(retorno.children[2].children[1].children[0]) == 'SOMA'): 
                                                                                retornofuncao = builder.add( loadvar1 , loadvar2 , name='retorno_soma_funcao', flags=()) 
                                                                        if(get_name(retorno.children[2].children[1].children[0]) == 'SUBTRACAO'):  
                                                                                subaux = 1
                                                                                retornofuncao = builder.sub( loadvar1 , loadvar2 , name='retorno_sUB_funcao', flags=())         
                                                        else: 
                                                                if get_name(retorno) == 'retorna' and get_name(retorno.children[2]) == 'expressao_aditiva':  
                                                                        if(get_name(retorno.children[2].children[1].children[0]) == 'SOMA'): 
                                                                        
                                                                                retornofuncao = 0  
                                                                                primeiravariavel = get_last_value_name(retorno.children[2].children[0].children[0]) 
                                                                                segundavariavel = get_last_value_name(retorno.children[2].children[2].children[0])
                                                                                                
                                                                                #load_a = builder.load(a) 
                                                                                z = builder.alloca(t_int, name=primeiravariavel) 
                                                                                x = builder.alloca(t_int, name=segundavariavel) 
                                                                                z = builder.load(z, "") 
                                                                                x = builder.load(x, "")
                                                                                retornofuncao = builder.add(z,x, name='add') 
                                                                        if(get_name(retorno.children[2].children[1].children[0]) == 'SUBTRACAO'): 
                                                                        
                                                                                retornofuncao = 0  
                                                                                primeiravariavel = get_last_value_name(retorno.children[2].children[0].children[0]) 
                                                                                segundavariavel = get_last_value_name(retorno.children[2].children[2].children[0])
                                                                                                
                                                                                #load_a = builder.load(a) 
                                                                                z = builder.alloca(t_int, name=primeiravariavel) 
                                                                                x = builder.alloca(t_int, name=segundavariavel) 
                                                                                z = builder.load(z, "") 
                                                                                x = builder.load(x, "")
                                                                                retornofuncao = builder.sub(z,x, name='add')        
                                                                        #builder.store(add, b) 
                                                                if get_name(retorno) == 'retorna' and get_name(retorno.children[2]) == 'numero':  
                                                                        retornofuncao = get_last_value_name(retorno.children[2].children[0])         
                                                corpo = node.children[4] 
                                                while len(corpo.children) != 0: 
                                                        corpo = corpo.children[0] 
                                                #print(get_name(corpo)) 
                                                while get_name(corpo.parent) != 'cabecalho': 
                                                        if get_name(corpo) == 'corpo': 
                                                                if get_name(corpo.children[1]) == 'leia':  
                                                                        if printaux == 0:
                                                                                voidptr_ty = ir.IntType(32).as_pointer()
                                                                                scanf_ty = ir.FunctionType(ir.IntType(32), [])     
                                                                                #leiaInteiro = ir.Function(module,ir.FunctionType(ir.IntType(32),[]),name="leiaInteiro")
                                                                                printaux = 1  
                                                                        if printaux == 1:  
                                                                                #caule = builder.call(ponteiroaux, [])  
                                                                                for s in tableofsymbols: 
                                                                                        if s['tipo'] == 'inteiro' and s['nome'] == get_last_value_name(corpo.children[1].children[2].children[0]):  
                                                                                                #print(s['tipo'])     
                                                                                                builder.store(builder.call(leiaInteiro, ()) , s['code'])  
                                                                                        if s['tipo'] == 'flutuante' and s['nome'] == get_last_value_name(corpo.children[1].children[2].children[0]):  
                                                                                                #print(s['tipo'])     
                                                                                                builder.store(builder.call(leiaFlutuante, ()) , s['code'])  
                                                                                                              
                                                                if get_name(corpo.children[1]) == 'escreva':  
                                                                        nome = get_last_value_name(corpo.children[1].children[2].children[0])
                                                                        for s in tableofsymbols: 
                                                                                if s['nome'] == nome and s['tipo'] == 'inteiro':  
                                                                                        codigov = s['code'] 
                                                                                        builder.call(plh_print,[builder.load(codigov)])  
                                                                                if s['nome'] == nome and s['tipo'] == 'flutuante':  
                                                                                        codigov = s['code'] 
                                                                                        builder.call(plh_print_float,[builder.load(codigov)])  
                                                
                                                                if(get_name(corpo.children[1]) == 'repita'):
                                                                        repita = funcao.append_basic_block('repita_inicio') 
                                                                        repitafim = funcao.append_basic_block('repita_fim')   

                                                                        builder.branch(repita)  
                                                                        builder.position_at_end(repita)  
                                                                        for mynode in LevelOrderIter(corpo.children[1]):  
                                                                                if get_name(mynode) == 'leia': 
                                                                                        for s in tableofsymbols: 
                                                                                                if s['nome'] == get_last_value_name(mynode.children[2].children[0]): 
                                                                                                        #codigov = s['code']   
                                                                                                        builder.store(builder.call(leiaInteiro,[]),s['code'])
                                                                                if get_name(mynode) == 'escreva':  
                                                                                        if printaux == 0:
                                                                                                for s in tableofsymbols: 
                                                                                                        if s['nome'] == get_last_value_name(mynode.children[2].children[0]): 
                                                                                                                codigov = s['code']
                                                                                                                #builder.call(plh_print,[builder.load(codigov)]) 

                                                                                if get_name(mynode) == 'atribuicao': 
                                                                                        if get_name(mynode.children[2]) == 'expressao_aditiva' and get_name(mynode.children[2].children[2]) == 'numero' and get_name(mynode.children[2].children[1].children[0]) == 'SOMA': 
                                                                                                #print('oi') 
                                                                                                if get_last_value_name(mynode.children[0].children[0]) == get_last_value_name(mynode.children[2].children[0].children[0]): 
                                                                                                        numerow = get_last_value_name(mynode.children[2].children[2].children[0]) 
                                                                                                        for symb2 in tableofsymbols: 
                                                                                                                if symb2['nome'] == get_last_value_name(mynode.children[0].children[0]): 
                                                                                                                        temp = builder.load(symb2['code'], "")
                                                                                                                        num = builder.alloca(ir.IntType(32), name=numerow)  
                                                                                                                        numreal = builder.load(num) 
                                                                                                                        temp = builder.add(temp, numreal, name='incremento', flags=())   
                                                                                                                        builder.call(plh_print,[builder.load(symb2['code'])])  
                                                                                        if get_name(mynode.children[2]) == 'expressao_aditiva' and get_name(mynode.children[2].children[2]) == 'numero' and get_name(mynode.children[2].children[1].children[0]) == 'SUBTRACAO': 
                                                                                                print('ola')
                                                                                                if get_last_value_name(mynode.children[0].children[0]) == get_last_value_name(mynode.children[2].children[0].children[0]): 
                                                                                                        numerow = get_last_value_name(mynode.children[2].children[2].children[0]) 
                                                                                                        for symb2 in tableofsymbols: 
                                                                                                                if symb2['nome'] == get_last_value_name(mynode.children[0].children[0]): 
                                                                                                                        temp = builder.load(symb2['code'], "")
                                                                                                                        num = builder.alloca(ir.IntType(32), name=numerow)  
                                                                                                                        numreal = builder.load(num) 
                                                                                                                        temp = builder.sub(temp, numreal, name='incremento', flags=())                                                                            
                                                                                        if get_name(mynode.children[2]) == 'chamada_funcao' and get_name(mynode.children[2].children[2].children[0]) == 'chamada_funcao':  
                                                                                                funcaochamada = get_last_value_name(mynode.children[2].children[0])  
                                                                                                funcao1 = get_last_value_name(mynode.children[2].children[2].children[0].children[0]) 
                                                                                                funcao2 = get_last_value_name(mynode.children[2].children[2].children[2].children[0])  
                                                                                                primeiravariavel = get_last_value_name(mynode.children[2].children[2].children[0].children[2].children[0].children[0])
                                                                                                segundavariavel = get_last_value_name(mynode.children[2].children[2].children[0].children[2].children[2].children[0]) 
                                                                                                terceiravariavel = get_last_value_name(mynode.children[2].children[2].children[2].children[2].children[0].children[0]) 
                                                                                                quartavariavel = get_last_value_name(mynode.children[2].children[2].children[2].children[2].children[2].children[0]) 
                                                                                                
                                                                                                variavelatribuicao = get_last_value_name(mynode.children[0].children[0]) 
                                                                                                for sss in tableofsymbols: 
                                                                                                        if sss['nome'] == variavelatribuicao: 
                                                                                                                res = sss['code'] 
                                                                                                for sss in tableofsymbols: 
                                                                                                        if sss['token'] == 'ID': 
                                                                                                                if sss['nome'] == primeiravariavel: 
                                                                                                                        primeirocodigo = sss['code'] 
                                                                                                                if sss['nome'] == segundavariavel: 
                                                                                                                        segundocodigo = sss['code'] 
                                                                                                                if sss['nome'] == terceiravariavel: 
                                                                                                                        terceirocodigo = sss['code'] 
                                                                                                                if sss['nome'] == quartavariavel: 
                                                                                                                        quartocodigo = sss['code']                 
                                                                                                for sss in tableofsymbols: 
                                                                                                        if sss['token'] == 'func' and sss['nome'] == funcao1: 
                                                                                                                codigofuncao1 = sss['codigo'] 
                                                                                                        if sss['token'] == 'func' and sss['nome'] == funcao2: 
                                                                                                                codigofuncao2 = sss['codigo'] 
                                                                                                                
                                                                                                for sss in tableofsymbols:         
                                                                                                        if sss['token'] == 'func' and sss['nome'] == funcaochamada: 
                                                                                                                #print('código', sss['codigo'])  
                                                                                                                call = builder.call(sss['codigo'], [builder.call(codigofuncao1, [builder.load(primeirocodigo) , builder.load(segundocodigo)]) ,  builder.call(codigofuncao2, [builder.load(terceirocodigo) , builder.load(quartocodigo)])])
                                                                                                                builder.store(call,res) 
                                                                                                                #builder.call(plh_print,[builder.load(res)]) 
                                                                                                                # call = builder.call(sss['codigo], [builder.call(codigofuncao1, [builder.load(a), builder.load(b)]) , builder.call(soma, [builder.load(a), builder.load(b)])])                 
                                                                                        if get_name(mynode.children[2]) == 'chamada_funcao' and get_name(mynode.children[2].children[2].children[0]) != 'chamada_funcao':  
                                                                                                operacao = 1 
                                                                                                funcaochamada = get_last_value_name(mynode.children[2].children[0]) 
                                                                                                variavelatribuicao = get_last_value_name(mynode.children[0].children[0])
                                                                                                #res = builder.alloca(ir.IntType(32), name=variavelatribuicao)  
                                                                                                if(get_name(mynode.children[2].children[2]) == 'lista_argumentos'):
                                                                                                        var1 = get_last_value_name(mynode.children[2].children[2].children[0].children[0]) 
                                                                                                        var2 = get_last_value_name(mynode.children[2].children[2].children[2].children[0])  
                                                                                                        #print(var1, var2)  
                                                                                                        for sss in tableofsymbols:  
                                                                                                                if sss['token'] == 'ID' and sss['nome'] == var1: 
                                                                                                                        var11 = sss['code']  
                                                                                                                if sss['token'] == 'ID' and sss['nome'] == var2: 
                                                                                                                        var22 = sss['code']     
                                                                                                        for sss in tableofsymbols:         
                                                                                                                if sss['token'] == 'func' and sss['nome'] == funcaochamada: 
                                                                                                                        call = builder.call(sss['codigo'], [builder.load(var11), builder.load(var22)]) 
                                                                                                                        for s in tableofsymbols: 
                                                                                                                                if s['nome'] == variavelatribuicao: 
                                                                                                                                        #res = s['code'] 
                                                                                                                                        builder.store(call, s['code']) 
                                                                                                                                        builder.call(plh_print,[builder.load(codigov)])                          
                                                                                        nome_var = get_last_value_name(mynode.children[0].children[0])  
                                                                                        for symbn in tableofsymbols: 
                                                                                                if symbn['nome'] == nome_var: 
                                                                                                        store = symbn['code'] 
                                                                                        if(get_name(mynode.children[2]) == 'chamada_funcao' and get_name(mynode.children[2].children[0]) == 'var'):  
                                                                                                 
                                                                                                variavelatribuicao = get_last_value_name(mynode.children[0].children[0])  
                                                                                                funcaochamada = get_last_value_name(mynode.children[2].children[0]) 
                                                                                                res = builder.alloca(ir.IntType(32), name=variavelatribuicao)  
                                                                                                if(get_name(mynode.children[2].children[2]) == 'lista_argumentos'):
                                                                                                        var1 = get_last_value_name(mynode.children[2].children[2].children[0].children[0]) 
                                                                                                        var2 = get_last_value_name(mynode.children[2].children[2].children[2].children[0]) 
                                                                                                for sss in tableofsymbols:  
                                                                                                        if sss['token'] == 'ID' and sss['nome'] == var1: 
                                                                                                                var11 = sss['code']  
                                                                                                        if sss['token'] == 'ID' and sss['nome'] == var2: 
                                                                                                                var22 = sss['code']     
                                                                                                for sss in tableofsymbols:         
                                                                                                        if sss['token'] == 'func' and sss['nome'] == funcaochamada: 
                                                                                                                call = builder.call(sss['codigo'], [builder.load(var11), builder.load(var22)])
                                                                                                                builder.store(call, res)
                                                                                                #print(variavelatribuicao,funcaochamada)
                                                                                        if get_name(mynode.children[2]) == 'expressao_aditiva':  
                                                                                                if(get_name(mynode.children[2].children[0]) == 'var'): 
                                                                                                        for s1 in tableofsymbols: 
                                                                                                                if s1['nome'] == get_last_value_name(mynode.children[2].children[0].children[0]): 
                                                                                                                     temp1 = builder.load(s1['code'], "") 
                                                                                                elif(get_name(mynode.children[2].children[0]) == 'numero'): 
                                                                                                        temp1 = ir.Constant(ir.IntType(32), get_last_value_name((mynode.children[2].children[0].children[0]))) 
                                                                                                if(get_name(mynode.children[2].children[2]) == 'var'): 
                                                                                                        for s1 in tableofsymbols: 
                                                                                                                if s1['nome'] == get_last_value_name(mynode.children[2].children[2].children[0]): 
                                                                                                                    temp2 = builder.load(s1['code'], "") 
                                                                                                elif get_name(mynode.children[2].children[2]) == 'numero':  
                                                                                                        temp2 = ir.Constant(ir.IntType(32), get_last_value_name((mynode.children[2].children[2].children[0])))                                                                                                                                                   
                                                                                                storetemp = builder.add( temp1 , temp2 , name='result', flags=()) 
                                                                                                builder.store(storetemp, store)                                                         

                                                                        if(get_name(corpo.children[1].children[3]) == 'expressao_simples'): 
                                                                                for symbx in tableofsymbols: 
                                                                                        if symbx['nome'] == get_last_value_name(corpo.children[1].children[3].children[0].children[0]): 
                                                                                                codx = symbx['code']  
                                                                                                cod1 = builder.load(codx, 'b_cmp', align=4) 
                                                                                if(get_name(corpo.children[1].children[3].children[2]) == 'numero'): 
                                                                                        cod2 = ir.Constant(ir.IntType(32), get_last_value_name(corpo.children[1].children[3].children[2].children[0]))                
                                                                                if(get_name(corpo.children[1].children[3].children[1].children[0]) == 'MAIOR'): 
                                                                                        relacional = '>' 
                                                                                elif(get_name(corpo.children[1].children[3].children[1].children[0]) == 'MENOR'): 
                                                                                        relacional = '<'                 
                                                                                elif(get_name(corpo.children[1].children[3].children[1].children[0]) == 'IGUALDADE'): 
                                                                                        relacional = '==' 
                                                                                elif(get_name(corpo.children[1].children[3].children[1].children[0]) == 'MENORIGUAL'): 
                                                                                        relacional = '<=' 
                                                                                elif(get_name(corpo.children[1].children[3].children[1].children[0]) == 'MAIOR_GUAL'): 
                                                                                        relacional = '>='     
                                                                                elif(get_name(corpo.children[1].children[3].children[1].children[0]) == 'DIFERENTE'): 
                                                                                        relacional = '!='                                                                                     
                                                                                # if nequal if do até vai pro fim, if equal vai pra repita novamente 
                                                                                If_while = builder.icmp_signed(relacional, cod1, cod2, name='if_test_while')
                                                                                builder.cbranch(If_while,repita, repitafim) 
                                                                                builder.position_at_end(repitafim)   
                                                                                
                                                                if(get_name(corpo.children[1]) == 'atribuicao' and get_name(corpo.children[1].children[2]) != 'chamada_funcao'): 
                                                                        #if(get_name(corpo.children[1].children[2]) != 'var'): 
                                                                        #        p#rint('oi')
                                                                        nomevar = get_last_value_name(corpo.children[1].children[0].children[0]) 
                                                                        for t in tableofsymbols: 
                                                                                if t['nome'] == nomevar and t['token'] == 'ID': 
                                                                                        codename = t['code']  
                                                                                        tipo = t['tipo']  
                                                                        if(get_name(corpo.children[1].children[2]) != 'var'):  
                                                                                if(tipo == 'inteiro'):                 
                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(corpo.children[1].children[2].children[0]) ), codename)         
                                                                                if(tipo == 'flutuante' and get_name(corpo.children[1].children[2]) == 'numero'): 
                                                                                        number = get_last_value_name(corpo.children[1].children[2].children[0])                                         
                                                                                        builder.store( ir.Constant(ir.FloatType(), float(number)) , codename) 
                                                                        if(get_name(corpo.children[1].children[2]) == 'var'):  
                                                                                print('oi')
                                                                                nomevariavel = get_last_value_name(corpo.children[1].children[2].children[0]) 
                                                                                for x in tableofsymbols: 
                                                                                        if x['nome'] == nomevariavel: 
                                                                                                builder.store(builder.load(x['code'],""), codename)          
                                                                if(get_name(corpo.children[1]) == 'atribuicao' and get_name(corpo.children[1].children[2]) == 'chamada_funcao'):  
                                                                        print('oi')
                                                                        funcaochamada = get_last_value_name(corpo.children[1].children[2].children[0]) 
                                                                        variavelatribuicao = get_last_value_name(corpo.children[1].children[0].children[0])
                                                                        #res = builder.alloca(ir.IntType(32), name=variavelatribuicao) 
                                                                        for s in tableofsymbols: 
                                                                                if s['nome'] == variavelatribuicao: 
                                                                                        codd = s['code']
                                                                        if(get_name(corpo.children[1].children[2].children[2]) == 'lista_argumentos'):
                                                                                var1 = get_last_value_name(corpo.children[1].children[2].children[2].children[0].children[0]) 
                                                                                var2 = get_last_value_name(corpo.children[1].children[2].children[2].children[2].children[0])  
                                                                                #print(var1, var2)  
                                                                                for sss in tableofsymbols:  
                                                                                        if sss['token'] == 'ID' and sss['nome'] == var1: 
                                                                                                var11 = sss['code']  
                                                                                        if sss['token'] == 'ID' and sss['nome'] == var2: 
                                                                                                var22 = sss['code']     
                                                                                for sss in tableofsymbols:         
                                                                                        if sss['token'] == 'func' and sss['nome'] == funcaochamada: 
                                                                                                call = builder.call(sss['codigo'], [builder.load(var11), builder.load(var22)])
                                                                                                builder.store(call, codd)
                                                                if get_name(corpo.children[1]) == 'se': 
                                                                        nse += 1  
                                                                        iftrue = funcao.append_basic_block('iftrue_{}'.format(nse))
                                                                        iffalse = funcao.append_basic_block('iffalse_{}'.format(nse))
                                                                        ifend = funcao.append_basic_block('ifend_{}'.format(nse)) 
                                                                        
                                                                        if get_name(corpo.children[1].children[1].children[1]) == 'operador_relacional': 
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
                                                                                if(get_name(corpo.children[1].children[1].children[1].children[0]) == 'MAIOR'): 
                                                                                        relacional = '>' 
                                                                                elif(get_name(corpo.children[1].children[1].children[1].children[0]) == 'MENOR'): 
                                                                                        relacional = '<'                 
                                                                                elif(get_name(corpo.children[1].children[1].children[1].children[0]) == 'IGUALDADE'): 
                                                                                        relacional = '==' 
                                                                                elif(get_name(corpo.children[1].children[1].children[1].children[0]) == 'MENORIGUAL'): 
                                                                                        relacional = '<=' 
                                                                                elif(get_name(corpo.children[1].children[1].children[1].children[0]) == 'MAIOR_GUAL'): 
                                                                                        relacional = '>='     
                                                                                elif(get_name(corpo.children[1].children[1].children[1].children[0]) == 'DIFERENTE'): 
                                                                                        relacional = '!='                                                          
                                                                                        
                                                                                If_1 = builder.icmp_signed(relacional, a_cmp, b_cmp, name='if_test_{}'.format(nse))
                                                                                builder.cbranch(If_1, iftrue, iffalse) 
                                                                                builder.position_at_end(iftrue) 
                                                                                for ny in LevelOrderIter(corpo.children[1].children[3]): 
                                                                                        if(get_name(ny) == 'atribuicao'): 
                                                                                               # print(get_name(ny)) 
                                                                                                for sy in tableofsymbols: 
                                                                                                        if sy['nome'] == get_last_value_name(ny.children[0].children[0]) and sy['token'] == 'ID': 
                                                                                                                if get_name(ny.children[2]) == 'numero':                        
                                                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(ny.children[2].children[0])), sy['code'])
                                                                                        
                                                                                        # if dentro do if  
                                                                                        if(get_name(ny) == 'se'):
                                                                                                iftrue2 = funcao.append_basic_block('iftrue_2')
                                                                                                iffalse2 = funcao.append_basic_block('iffalse_2')
                                                                                                ifend2 = funcao.append_basic_block('ifend_2')   
                                                                                                if(get_name(ny.children[1].children[1]) == 'operador_relacional'):
                                                                                                        var3 = get_last_value_name(ny.children[1].children[0].children[0]) 
                                                                                                        var4 = get_last_value_name(ny.children[1].children[2].children[0])   
                                                                                                        aux3 = 0 
                                                                                                        aux4 = 0 
                                                                                                        for k in tableofsymbols: 
                                                                                                                if k['nome'] == var3: 
                                                                                                                        c_cmp = builder.load(k['code'], k['nome']+'_cmp', align=4) 
                                                                                                                        aux3 = 1 
                                                                                                                if k['nome'] == var4:  
                                                                                                                        d_cmp = builder.load(k['code'], k['nome']+'_cmp', align=4) 
                                                                                                                        aux4 = 1
                                                                                                        if(aux3 == 0): 
                                                                                                                c_cmp = ir.Constant(ir.IntType(32), var3) 
                                                                                                        if(aux4 == 0):  
                                                                                                                d_cmp = ir.Constant(ir.IntType(32), var4)  
                                                                                                        if(get_name(ny.children[1].children[1].children[0]) == 'MAIOR'): 
                                                                                                                relacional = '>' 
                                                                                                        elif(get_name(ny.children[1].children[1].children[0]) == 'MENOR'): 
                                                                                                                relacional = '<'                 
                                                                                                        elif(get_name(ny.children[1].children[1].children[0]) == 'IGUALDADE'): 
                                                                                                                relacional = '==' 
                                                                                                        elif(get_name(ny.children[1].children[1].children[0]) == 'MENORIGUAL'): 
                                                                                                                relacional = '<=' 
                                                                                                        elif(get_name(ny.children[1].children[1].children[0]) == 'MAIOR_GUAL'): 
                                                                                                                relacional = '>='     
                                                                                                        elif(get_name(ny.children[1].children[1].children[0]) == 'DIFERENTE'): 
                                                                                                                relacional = '!='        
                                                                                                        If_2 = builder.icmp_signed(relacional, c_cmp, d_cmp, name='if_test_2')
                                                                                                        builder.cbranch(If_2, iftrue2, iffalse2) 
                                                                                                        builder.position_at_end(iftrue2)  
                                                                                                        if get_name(ny.children[3]) == 'atribuicao': 
                                                                                                                v1 = ny.children[3].children[0].children[0]
                                                                                                                r1 = ny.children[3].children[2].children[0] 
                                                                                                                for sf in tableofsymbols: 
                                                                                                                        if sf['nome'] == get_last_value_name(v1) and sf['token'] == 'ID': 
                                                                                                                                if(get_name(ny.children[3].children[2]) == 'numero'):
                                                                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(r1)), sf['code'])  
                                                                                                        builder.branch(ifend2)                                 
                                                                                                        builder.position_at_end(iffalse2)  
                                                                                                        if get_name(ny.children[5]) == 'atribuicao': 
                                                                                                                v1 = ny.children[5].children[0].children[0]
                                                                                                                r1 = ny.children[5].children[2].children[0] 
                                                                                                                for sf in tableofsymbols: 
                                                                                                                        if sf['nome'] == get_last_value_name(v1) and sf['token'] == 'ID': 
                                                                                                                                if(get_name(ny.children[5].children[2]) == 'numero'):
                                                                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(r1)), sf['code']) 
                                                                                                        builder.branch(ifend2)  
                                                                                                        builder.position_at_end(ifend2)  
                                                                                                        
                                                                                                          
                                                                                                        builder.branch(ifend)  
                                                                                                        builder.position_at_end(iffalse) 
                                                                                                        lastaux = 1 
                                                                                if lastaux == 0:                          
                                                                                        builder.branch(ifend)  
                                                                                        builder.position_at_end(iffalse)            
                                                                                if(get_name(corpo.children[1].children[4]) == 'SENAO'):  
                                                                                        if get_name(corpo.children[1].children[5]) == 'atribuicao': 
                                                                                                for sy in tableofsymbols: 
                                                                                                        if sy['nome'] == get_last_value_name(corpo.children[1].children[5].children[0].children[0]) and sy['token'] == 'ID':  
                                                                                                                if get_name(corpo.children[1].children[5].children[2]) == 'numero': 
                                                                                                                        builder.store(ir.Constant(ir.IntType(32), get_last_value_name(corpo.children[1].children[5].children[2].children[0])), sy['code'])                                                                                                                                                        
                                                                                builder.branch(ifend)   
                                                                                builder.position_at_end(ifend)
                                                                        
                                                        corpo = corpo.parent 
                        exitBasicBlock = funcao.append_basic_block('exit') 
                        builder.branch(exitBasicBlock) 
                        builder = ir.IRBuilder(exitBasicBlock) 
                        booleano = 0                                         
                        for z in tableofsymbols: 
                                if z['nome'] == retornofuncao and z['token'] == 'ID' and z['tipo'] == 'inteiro':            
                                        returnVal_temp = builder.load(z['code'], name='ret_temp', align=4)   
                                        builder.ret(returnVal_temp) 
                                        booleano = 1 
                        if(booleano == 0):    
                                if len(funcao.args) != 0: 
                                        if subaux == 1: 
                                                res = builder.sub(funcao.args[0], funcao.args[1])        
                                        else: 
                                                res = builder.add(funcao.args[0], funcao.args[1])
                                        builder.ret(res)    
                                else: 
                                        builder.ret(ir.Constant(ir.IntType(32), retornofuncao))                      
        arquivo = open('root.ll', 'w')
        arquivo.write(str(module))
        arquivo.close()
        print(module)    