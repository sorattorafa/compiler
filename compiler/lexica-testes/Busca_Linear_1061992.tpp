inteiro: A[20]
inteiro busca(inteiro: n)
	inteiro: ret
	inteiro: i
	ret := 0
	i := 0
	repita 
		se A[i] = n
			ret := 1
		i := i + 1
	até i = 20
	retorna(ret)
fim

inteiro principal()
	inteiro: i
	i := 0
	repita 
		A[i] := i
		i := i + 1
	até i = 20
	leia(n)
	escreva(busca(n))
	retorna(0)
fim