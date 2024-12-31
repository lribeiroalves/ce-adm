from machine import UART, Pin
import os
from time import sleep, sleep_ms


uart_2 = UART(1, baudrate=9600, tx=27, rx=26)
uart_1 = UART(2, baudrate=9600, tx=17, rx=16)

c = 0

while True:
    if uart_2.any():
        sleep_ms(10)
        print([num for num in uart_2.read()])
        c = 0
    
    sleep_ms(5)
    
    if c >= 0:
        c += 1
    
    if c >= 500:
        uart_1.write(bytes([12, 15, 255, 20, 100]))
        c = -1
    






# apenas para curiosidade (como retirar informações do hardware da ESP32)
# id_name = os.uname()
# print(id_name)