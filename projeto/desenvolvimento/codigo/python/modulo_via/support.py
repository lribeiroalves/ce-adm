from machine import Pin
import dht as DHT
from time import sleep, sleep_ms


class MyDht:
    """
    Classe para implementação específica do uso do modulo dht
    para leituras de umidade e temperatura em períodos predefinidos
    """
    def __init__(self, pin, time_ms=1000):
        self.__dht_pin = Pin(pin)
        self.__read_time = time_ms
        self.__dht = DHT.DHT11(self.__dht_pin)
        self.__read_values = []
        
    
    def read_dht(self) -> tuple[int, int]:
        """ Realiza apenas uma leitura e retorna uma tupla (temperatura * 5, umidade) """
        try:
            self.__dht.measure()
            return (self.__dht.temperature() * 5, self.__dht.humidity())
        except Exception as err:
            print(err)
            return (255, 255)
            


if __name__ == '__main__':
    my_dht = MyDht(pin=33)
    while True:
        print(my_dht.read_dht())
        sleep(1)
        