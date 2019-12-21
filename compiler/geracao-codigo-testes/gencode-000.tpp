inteiro: n
inteiro: soma

inteiro principal()
	soma := 0 
	leia(n)
	repita
		soma := soma + n
		n := n - 1 
	até n = 0
 
	escreva(soma)
	retorna(0)
fim
