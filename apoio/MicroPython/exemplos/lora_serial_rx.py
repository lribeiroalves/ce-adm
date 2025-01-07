from machine import UART
from time import sleep, sleep_ms

lora = UART(2, baudrate=1200, tx=4, rx=2)

print('LORA RX')
sleep(3)

while True:
    if lora.any():
        sleep_ms(150)
        print([num for num in lora.read()])