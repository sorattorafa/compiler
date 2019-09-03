{preenche o vetor} 
inteiro: vet[100];
preencheVetor(inteiro:n)
  inteiro: i
  inteiro: j
  i := 0
  j := n
  repita
    vet[i] = j
    i := i + 1
    j := j - 1
  até i < n
fim

{ função insertion sort }
insertion_sort(inteiro:n) 
 inteiro: i  
 inteiro: j  
 inteiro tmp  
 i := 1
 repita  
    j := i 
    repita  
        tmp = vet[j] 
        vet[j] = vet[j-1] 
        vet[j-1] = tmp 
        j := j - 1
    até (j > 0) && (vet[j-1] > vet[j])
    i := i +1  
 até i < n 
fim

{ main }
inteiro principal()
  preencheVetor(10)
  insertion_sort(10)
  retorna(0)
fim