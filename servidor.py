import json
import _thread
import spidev
import paho.mqtt.client as mqtt
from libsoc_zero.GPIO import LED
from libsoc_zero.GPIO import Button
from libsoc import gpio
from time import sleep

client = mqtt.Client()
#servidor seria interessante por no arquivo de configuracao tambem talvez
client.connect("127.0.0.1", 1883)

dicionario = {'d1': 'GPIO-A', 'd2': "GPIO-C"}

class Carregar(object):
	def __init__(self, j):
		self.__dict__ = json.loads(j)

#thread:
def monitorDigitalSaida(objeto, nome):
	global dicionario
	saida = LED(dicionario[porta.port])
	print("Escutando o Topico " + objeto.topic)
	def on_message(mqttc, obj, msg):
		if(msg.payload.decode('UTF-8') == "1" or  msg.payload.decode('UTF-8').lower() == "true" or msg.payload.decode('UTF-8').lower() == "on"):
			#ligar porta
			saida.on()
		elif(msg.payload.decode('UTF-8') == "0" or  msg.payload.decode('UTF-8').lower() == "false" or msg.payload.decode('UTF-8').lower() == "off"):
			#10ligar porta
			saida.off()

	client.on_message = on_message
	client.subscribe(objeto.topic)
	client.loop_forever()

#thread:
def monitorDigitalEntrada(objeto, nome):
	global dicionario
	entrada = Button(dicionario[porta.port])
	while 1:
		if entrada.is_pressed():
			client.publish(objeto.topic, "1")
		else:
			client.publish(objeto.topic, "0")
			
		sleep(objeto.interval)

#thread:
def monitorAnalogicoEntrada(objeto, nome):
	spi = spidev.SpiDev()
	spi.open(0,0)
	spi.max_speed_hz= 10000
	spi.mode = 0b00
	spi.bits_per_word = 8
	channel_select =[0x01, 0x80, 0x00] if(objeto.port.lower()=="adc1") else [0x01, 0xA0, 0x00] 
	
	#confirmar se precisa liberar o pino a cada iteração
	while True:
		gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
		with gpio.request_gpios([gpio_cs]):
		gpio_cs.set_high()
    sleep(0.00001)
    gpio_cs.set_low()
    rx = spi.xfer(channel_select)
    gpio_cs.set_high()
    adc_value = (rx[1] << 8) & 0b1100000000
		adc_value = adc_value | (rx[2] & 0xff)
		client.publish(objeto.topico, adc_value * objeto.constant + objeto.offset );
		#free gpio_cs
		sleep(objeto.interval)
	
# main:	
if __name__=='__main__':	
	with open("portas.json") as f:
		for linha in f:
			objeto = Carregar(linha)
			if(objeto.port=="adc1".lower() or objeto.port.lower() == "adc2"):
				if(objeto.mode.lower() == "in" or objeto.mode.lower() == "input"):
					_thread.start_new_thread( monitorAnalogicoEntrada, (objeto, "") )
			elif(objeto.port.lower() == "d1" or objeto.port.lower() == "d2"):
				if(objeto.mode.lower() == "in" or objeto.mode.lower() == "input"):
					_thread.start_new_thread( monitorDigitalSaida, (objeto, "") )
				elif(objeto.mode.lower() == "out" or objeto.mode.lower() == "output")
					_thread.start_new_thread( monitorDigitalEntrada, (objeto, "") )
				
	#espera rustica pelas threads			
	while 1:
		sleep(1)

