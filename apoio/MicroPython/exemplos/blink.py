from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)
    print('led_on')
    time.sleep(0.5)
    led.value(0)
    print('led_off')
    time.sleep(0.5)