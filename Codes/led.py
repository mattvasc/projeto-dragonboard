from libsoc_zero.GPIO import LED
from time import sleep

led = LED('GPIO-A')

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
