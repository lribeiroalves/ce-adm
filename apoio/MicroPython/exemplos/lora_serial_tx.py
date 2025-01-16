from machine import UART
from time import sleep

lora = UART(1, baudrate=1200, tx=27, rx=26)

print('LORA TX')
sleep(3)

while True:
    send = lora.write(bytes([10,20,30]))
    print(send)
    sleep(1)