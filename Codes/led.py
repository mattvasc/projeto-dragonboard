from libsoc_zero.GPIO import LED
from time import sleep

# led conectado na porta D1
led = LED('GPIO-A')

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
