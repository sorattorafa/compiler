#include <stdio.h>

void escrevaInteiro(int ni) {
  printf("%d\n", ni);
}

void escrevaFlutuante(float nf) {
  printf("%f\n", nf);
}

int leiaInteiro() { 
  printf("Digite um número inteiro\n");
  int num;
  scanf("%d", &num);
  return num;
}

float leiaFlutuante() { 

  printf("Digite um número flutuante \n");
  float num;
  scanf("%f", &num);
  return num;
}