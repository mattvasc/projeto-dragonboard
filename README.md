# Projeto Dragonboard
Projeto de contribuição para a disciplina IoT ofertada na **Universidade Federal de São Carlos**. 
O Projeto consiste em criar um servidor em python que monitore canais **MQTT** em adjunto aos sensores da placa **DB410C**.
## Sobre o server.py
Consiste em um servidor multithread onde cada thread terá a responsabilidade de cuidar de um sensor e escutar/publicar em um determinado tópico do protocolo MQTT.
## Sobre o arquivo config.json
Arquivo de configuração do servidor, onde a primeira linha é exclusivamente dedicada a configuração do broker mqtt e para as demais, cada linha equivale a uma entrada/saída do shield (Utilizado para desenvolvimento do projeto **LinkerSprite Starter Kit**).
É necessário fornecer objetos com os parâmetros necessários para o correto funcionamento.
### Configuração do Broker
É necessário na primeira linha do arquivo fornecer um objeto json com os seguintes atributos:
- server - String de onde se encontra o broker
- port - Número da porta onde o broker está rodando.
##### Exemplo de configuração de Broker:
{ "server" : "localhost"; "port" : 1883 }
### Configurar uma entrada/saída digital
Após a configuração do broker, segue os objetos referente aos sensores. Parâmetros necessários:
- port - Indica em qual porta do shield o sensor está conectado. Valores válidos: "d1", "d2", "d3" e "d4".
- mode - Indica se o sensor conectado é de entrada de saída. Valores válidos: "in" ou "out".
- topic - Indica em qual tópico o sensor irá escutar no caso de dispositivo de entrada, ou publicar em caso de dispositivo de entrada.
- onlyNewValues - Configuração exclusiva para dispositivos de entrada, se ativa, não publicará valores repetidos no tópico cuja o qual o sensor está configurado. Valores válidos: true/false.
##### Exemplo de uma entrada dígital:
{ "port" : "d1", "mode": "in", "topic":"apertou", "onlyNewValues" : false,  "interval" : 0.05 }

##### Exemplo de uma saída digital:
{ "port" : "d2", "mode": "out", "topic":"apertou"}



## Sobre o projeto
Atualmente, o projeto está sendo desenvolvido pelo grupo de estudantes:
- Mateus S. Vasconcelos
- Giovanna Blasco

E contou com a colaboração dos seguintes no ano de 2017:
- Gabriela Ramos
- Letícia Berto
- Mateus S. Vasconcelos
- Wesley Moura

Em adjunto com os professores:
- Fábio Verdi
- Yeda Venturi
