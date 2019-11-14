{Aviso: Coerção implícita do valor atribuído para 'a', variável a flutuante recebendo um inteiro}
{Erro: Função 'func' do tipo inteiro retornando flutuante}
{Aviso: Função 'func' declarada, mas não utilizada}
{Aviso: Chamada recursiva para a função 'principal'}
{Erro: Função 'principal' deveria retornar inteiro, mas retorna vazio}

{flutuante: a}
inteiro: b

inteiro func()
  b := 10
  retorna(b)
fim

inteiro principal()
	b := 18 
  {a:= 1}  
  func()
  retorna(b)
fim
