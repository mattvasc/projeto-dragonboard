#!/usr/bin/python3
import spidev
from libsoc import gpio
from time import sleep
 
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=10000
spi.mode = 0b00
spi.bits_per_word = 8

#Usando a porta ADC1
channel_select=[0x01, 0x80, 0x00]

#Para usar a porta ADC2 use o seguinte vetor de configuração
#channel_select=[0x01, 0xA0, 0x00]
 
if __name__=='__main__':
    gpio_cs = gpio.GPIO(18, gpio.DIRECTION_OUTPUT)
    with gpio.request_gpios([gpio_cs]):
        while True:
            gpio_cs.set_high()
            sleep(0.00001)
            gpio_cs.set_low()
            rx = spi.xfer(channel_select)
            gpio_cs.set_high()
            
            adc_value = (rx[1] << 8) & 0b1100000000
            adc_value = adc_value | (rx[2] & 0xff)
 
            print("adc_value: %d" % adc_value)
            sleep(1)

