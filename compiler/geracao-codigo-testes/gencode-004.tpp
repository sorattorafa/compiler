inteiro: n
inteiro: soma

inteiro principal()
	n := 0
	soma := 0
	repita
		soma := soma + n
		n := n + 1
	até n <= 10
 
	escreva(soma)
	retorna(0)
fim
