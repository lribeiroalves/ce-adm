from machine import Pin
import dht as DHT
import time

dht = DHT.DHT11(Pin(33))

while True:
    try:
        dht.measure()
        print(f'Temperatura: {int(dht.temperature() * 5)}ºC - Umidade: {dht.humidity()}%')        
    except:
        print('Não foi possível realizar a leitura')
        
    time.sleep(1)