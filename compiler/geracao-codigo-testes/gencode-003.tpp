{Condicional}
inteiro: a

inteiro principal()
	inteiro: ret
	leia(a)   
	se a > 5 então
		se a < 20 então
			ret := 1
		senão
			ret := 2
		fim
	senão
		ret := 0
  fim 
  escreva(ret)

  retorna(0)
fim
