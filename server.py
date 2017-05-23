import json
import threading
import paho.mqtt.client as mqtt
from subprocess import call
from time import sleep

#Área de variaveis globais
global mqtt_config
#########

#criador de objetos que serao carregados nas threads
class Carregar(object):
	def __init__(self, linha):
		self.__dict__ = json.loads(linha)


#thread
class monitorDigitalSaida (threading.Thread):
	def __init__(self, objeto):
		threading.Thread.__init__(self)
		self.objeto = objeto
	def run(self):
		global mqtt_config
		print("Iniciando Monitor de Saída Digital para a porta: ", self.objeto.port + " no topico: " + self.objeto.topic)		
		client = mqtt.Client()
		#servidor seria interessante por no arquivo de configuracao tambem talvez
		client.connect(mqtt_config.server, mqtt_config.port)
		def on_message(mqttc, obj, msg):
			if(msg.payload.decode('UTF-8') == "1" or  msg.payload.decode('UTF-8').lower() == "true" or msg.payload.decode('UTF-8').lower() == "on"): 	#ligar porta
				call(["./digital", dicionario[self.objeto.port], "1"])
			elif(msg.payload.decode('UTF-8') == "0" or  msg.payload.decode('UTF-8').lower() == "false" or msg.payload.decode('UTF-8').lower() == "off"): #10ligar porta
				call(["./digital", dicionario[self.objeto.port], "0"])
		client.on_message = on_message
		client.subscribe(self.objeto.topic)
		client.loop_forever()



#thread:
class monitorDigitalEntrada (threading.Thread):
	def __init__(self, objeto):
		threading.Thread.__init__(self)
		self.objeto = objeto
	def run(self):
		print("Iniciando Monitor de Entrada Digital para a porta: ", self.objeto.port + " no topico: " + self.objeto.topic)	
		global dicionario
		global mqtt_config
		client = mqtt.Client()
		client.connect(mqtt_config.server, mqtt_port)
		client.publish(objeto.topic, "0")
		ultimo = 0
		while 1:
			valor = call(["./digital", dicionario[self.objeto.port], 'r' ])
			print("li: " + str(valor))
			if (valor and (not self.objeto.onlyNewValues or ultimo == 0)):
				client.publish(objeto.topic, "1")
				ultimo = 1
			elif(not self.objeto.onlyNewValues or ultimo == 1):
				client.publish(self.objeto.topic, "0")
				ultimo = 0
			sleep(self.objeto.interval)

#thread:    ~~ Em desenvolvimento !!!!!!!!!!
def monitorAnalogicoEntrada(objeto, nome):
	print("Iniciando Monitor de Entrada Analogica para a porta: ", self.objeto.port + " no topico: " + self.objeto.topic)	
	global travaAnalogica
	while True:
		travaAnalogica.acquire()
		# call(["analogic"])
		trava.release()
		sleep(self.objeto.interval)

# main:
if __name__=='__main__':
	global mqtt_config
	#converte porta para GPIO_ID
	dicionario = {'d1': '36', 'd2': "13", 'd3' : "115", "d4" : "24"}
	travaAnalogica = threading.Lock
	primeira_linha = True
	with open("config.json") as f:
		for linha in f:
			if(len(linha)>5):
				if primeira_linha :
					mqtt_config = Carregar(linha)
					primeira_linha = False
				else:
					objeto = Carregar(linha)
					if(objeto.port.lower() == "adc1" or objeto.port.lower() == "adc2"):
						if(objeto.mode.lower() == "in" or objeto.mode.lower() == "input"):
							thread = monitorAnalogicoEntrada(objeto)
							thread.start()
					elif(objeto.port.lower() == "d1" or objeto.port.lower() == "d2" or objeto.port.lower() == "d3" or objeto.port.lower() == "d4" or objeto.port.lower() == "d5"):
						if(objeto.mode.lower() == "in" or objeto.mode.lower() == "input"):
							thread = monitorDigitalEntrada(objeto)
							thread.start()
						elif(objeto.mode.lower() == "out" or objeto.mode.lower() == "output"):
							thread = monitorDigitalSaida(objeto)
							thread.start()

	#espera infinita pelas threads
	thread.join()
