from machine import Pin
import dht as DHT
from time import sleep, sleep_ms, ticks_ms


class MyDht:
    """ Classe para implementação específica do uso do modulo dht
    para leituras de umidade e temperatura em períodos predefinidos"""
    
    def __init__(self, dht_pin: int = 33, time_ms: int = 1000):
        self.__dht_object = DHT.DHT11(Pin(dht_pin))
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = [0, 0]
        self.__update_enable = True
    
    
    @property
    def readings(self):
        return self.__readings
    
    
    @property
    def update_enable(self):
        return self.__update_enable
    
    
    @update_enable.setter
    def update_enable(self, flag: bool):
        if flag == True:
            self.__update_enable = True
            self.__readings = [0, 0]
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')
    
    
    def read_dht(self) -> tuple[int, int]:
        """ Realiza uma leitura do sensor e retorna uma tupla (temperatura * 5, umidade),
            em caso de erro, repete recursivamente até que consiga o valor """
        try:
            self.__dht_object.measure()
            return (self.__dht_object.temperature() * 5, self.__dht_object.humidity())
        except OSError:
            sleep_ms(10)
            return self.read_dht()
        except Exception as err:
            print(err)
            return (255, 255)
    
    
    def update(self):
        """ Solicita ao sensor os valores repetidamente após o período predeterminado
            e atualiza a lista de retorno """
        current_time = ticks_ms()
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable == True:
            self.__previous_time = current_time
            # Realiza a leitura a salva na lista de retorno, desabilita novas leituras
            r = self.read_dht()
            self.__readings = [r[0], r[1]]
            self.__update_enable = False


if __name__ == '__main__':
    # Exemplo de aplicação da classe MyDht
    dht = MyDht(dht_pin=33)
    while True:
        dht.update()
        if not dht.update_enable:
            print(dht.readings)
            dht.update_enable = True
        