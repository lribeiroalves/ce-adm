from machine import Pin
import dht as DHT
from time import sleep, sleep_ms, ticks_ms


class MyDht:
    """
    Classe para implementação específica do uso do modulo dht
    para leituras de umidade e temperatura em períodos predefinidos
    """
    def __init__(self, pin, time_ms=1000):
        self.__dht_pin = Pin(pin)
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__dht = DHT.DHT11(self.__dht_pin)
        self.__read_values = [0, 0]
        self.__read_enable = True
        
    
    def read_dht(self) -> tuple[int, int]:
        """ Realiza apenas uma leitura e retorna uma tupla (temperatura * 5, umidade) """
        try:
            self.__dht.measure()
            return (self.__dht.temperature() * 5, self.__dht.humidity())
        except Exception as err:
            print(err)
            return (255, 255)
    
    
    def update(self):
        current_time = ticks_ms()
        
        if current_time <= self.__previous_time + self.__read_time and self.read_enable == True:
            r = read_dht()
            self.__read_values = [r[0], r[1]]
            self.__read_enable = False


if __name__ == '__main__':
    my_dht = MyDht(pin=33)
    while True:
        my_dht.update()
        if not my_dht.__read_enable:
            print(my_dht.__read_values)
        else:
            print(my_dht.__read_enable)
        