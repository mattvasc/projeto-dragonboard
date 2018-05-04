/* 

Compilar com a flag -lsoc
Informar apenas o numero da porta Digital de acordo com o Shield 
(de D1 a D4)

*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "libsoc_gpio.h"
#include "libsoc_debug.h"

int get_id (int porta);		// retorna o gpio_id de acordo com a porta 

int main ()
{

  int entrada, timer;
  gpio *gpio_entrada;
  gpio *gpio_saida;
  printf ("Digite em qual porta se localiza o botao de entrada: ");
  scanf ("%d%*c", &entrada);
  while (entrada < 0 || entrada > 4)
    {
      printf ("Favor digitar uma porta valida !\n");
      printf ("Digite em qual porta se localiza o botao de entrada: ");
      scanf ("%d%*c", &entrada);
    }
  
  gpio_entrada = libsoc_gpio_request (get_id (entrada), LS_SHARED);
  
  if (!gpio_entrada)
    {
      printf ("Erro ao abrir a porta D %d para entrada !\n", entrada);
      return 0;
    }
  
  libsoc_gpio_set_direction (gpio_entrada, INPUT);
  
  if (libsoc_gpio_get_direction (gpio_entrada) != INPUT)
    {
      printf ("Erro ao definir direcao das portas !\n");
      return 0;
    }
    
  timer = 0;
  printf ("Iniciando teste ...\n");
  while (timer < 9999)
    {
      if (libsoc_gpio_get_level (gpio_entrada) == HIGH)
	      printf("Botao foi pressionado!\n");
      else if (libsoc_gpio_get_level (gpio_entrada) == LOW)
	      printf("Esperando por uma acao\n");
      else{
	      printf ("Erro ao ler o botao de entrada !\n");
        break;
      }
      usleep (1000);
      timer++;
    }
  libsoc_gpio_set_level (gpio_saida, LOW);
  libsoc_gpio_free (gpio_entrada);
  libsoc_gpio_free (gpio_saida);
  printf ("teste finalizado !\n");
  return 0;
}

int get_id (int porta)
{
  switch (porta)
    {
    case 1:
      return 36;
    case 2:
      return 13;
    case 3:
      return 115;
    case 4:
      return 24;
    default:
      return 0;
    }
  return 0;
}
