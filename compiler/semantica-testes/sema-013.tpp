{Erro: Chamada para a função principal não permitida}
{Aviso: Coerção implícita do valor atribuído para 'a'}
{Aviso: Coerção implícita do valor retornado por 'func'}
{Erro: Função principal deveria retornar inteiro, mas retorna vazio}

flutuante: a
inteiro: b

inteiro func()
  a := 10
  retorna(1)
fim

inteiro principal()
	b := 18
	a := func() 
  retorna(0)
fim
