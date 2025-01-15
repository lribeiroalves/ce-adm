from machine import UART
from time import sleep, sleep_ms

# lora1 = UART(1, baudrate=1200, tx=4, rx=2)
lora2 = UART(2, baudrate=4800, tx=17, rx=16)

print('LORA RX')
sleep(3)

while True:
#     if lora1.any():
#         sleep_ms(1000)
#         print(f'Lora1: {[num for num in lora1.read()]}')
    
    if lora2.any():
        sleep_ms(500)
        msg = [num for num in lora2.read()]
        print(f'Lora2: {msg[:-1]}')
        print(f'Lora2 RSSI: {-(256 - msg[-1])} dBm')