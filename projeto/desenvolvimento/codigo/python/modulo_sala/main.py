from machine import UART
from Oled import Oled
import time

oled = Oled()
lora = UART(1, baudrate=1200, tx=32, rx=33)

oled.limpar()
oled.escrever('LORA Initializing')
time.sleep(5)
oled.limpar()
oled.escrever('LORA Ready', 10, 0)
time.sleep(3)

while True:
    if lora.any():
        pacote = [byte for byte in lora.read()]
        msg = pacote[:-1]
        rssi = -(256 - pacote[-1])
        
        print(f'Message Received: {msg}')
        print(f'rssi: {rssi} dBm')
        
        oled.limpar()
        oled.escrever(f'Bytes In: {len(msg)}', 5, 0)
        oled.escrever(f'RSSI: {rssi}dBm', 20, 0)
