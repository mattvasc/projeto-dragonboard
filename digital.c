#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <gpio.h>
#include <libsoc_gpio.h>
/*

Esse programa teve com intuito apenas descobrir qual pino da placa está
associado a qual porta do shield da Mezzanine.

Resultados obtidos:
Pino 23 -> ID 36  -> porta D1
Pino 25 -> ID 13  -> porta D2
Pino 27 -> ID 115 -> porta D3
Pino 29 -> ID 24  -> porta D4

Para compilacao: gcc acender_pino.c -o acender_pino -lsoc -l96BoardsGPIO

Pré requisito para compilação: biblioteca lsoc instalada corretamente e biblioteca 96BoardsGPIO também presente.

Para observar o resultado: plugue o módulo de led na respectiva porta e digite o respectivo pino!
*/
int main(int argc, char* argv[])
{
		if(argc<3){
			printf("Wrong usage of digital! Use: digital [PIN_ID] [BINARY VALUE or 'r']\n");
			return -1;
		}
		char pino = (char) atoi(argv[1]);
		char valor = ( argv[2][0] == '0' || argv[2][0] =='1') ? (char) atoi(argv[2]) : 3 ;
		if( (pino != 36 && pino != 13 && pino != 115 && pino != 24) || ( argv[2][0] != '0' && argv[2][0] !='1' && argv[2][0] !='r' && argv[2][0] != 'R') ){
			printf("Wrong usage of digital! Use: digital [PIN_ID] [BINARY VALUE or 'r']\n");
			return -1;
		}

		gpio *gpio_entrada;
		


		// Abrindo pino
		if(valor==1 || !valor){
			if(gpio_open(pino, "out")){
			    printf("Erro ao abrir o pino %d para saida!\n", pino);
			    return -1;
			}
		} else{ 
				gpio_entrada =  libsoc_gpio_request((pino),LS_SHARED);
				libsoc_gpio_set_direction(gpio_entrada,INPUT);
		    if(!gpio_entrada){
    	    printf("Erro ao abrir a porta para entrada!\n");
  		    return -1;
    		}
		}

		//Escrevendo no Pinoas
		if(valor==1 || !valor)
		{
			usleep(100);
  	  if (digitalWrite(pino, valor )){
        printf("Erro ao subir o estado logico do pino %d!\n", pino);
        return -1;    
    	}
			return 0;
		}
		else{ // Lendo o pino
			valor = libsoc_gpio_get_level(gpio_entrada);
			libsoc_gpio_free(gpio_entrada);
			return valor;
		}
   	return 2;
}

