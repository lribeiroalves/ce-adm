from machine import Pin
import dht as DHT
from time import sleep, sleep_ms, ticks_ms
from Clock import Clock
from CardSD import CardSD


class MyDht:
    """ Classe para implementação específica do uso do modulo dht
    para leituras de umidade e temperatura em períodos predefinidos"""
    
    def __init__(self, dht_pin: int = 33, time_ms: int = 1000, clock:Clock = None, sd:CardSD = None):
        self.__dht_object = DHT.DHT11(Pin(dht_pin))
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = [0, 0]
        self.__update_enable = True
        self.__clock = clock
        self.__sd = sd
        if self.__sd and self.__clock: # Create Data logger
            time = self.__clock.get_time()
            self.__log_path = f'/sd/data_logger/dht/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
            self.__sd.write_data(self.__log_path, 'temp,umid,year,month,day,hour,minute,second\n', 'w')
    
    
    @property
    def readings(self):
        for v in self.__readings:
            v = 0xfe if v == 0xff else v
        
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
            r = (self.__dht_object.temperature() * 5, self.__dht_object.humidity())
            if self.__clock and self.__sd:
                time = self.__clock.get_time()
                self.__sd.write_data(self.__log_path, f'{r[0]},{r[1]},{time["ano"] - 2000},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]}\n', 'a')
            return r
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
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            # Realiza a leitura a salva na lista de retorno, desabilita novas leituras
            r = self.read_dht()
            self.__readings = [r[0], r[1]]
            self.__update_enable = False


if __name__ == '__main__':
    # Exemplo de aplicação da classe MyDht
    from CardSD import CardSD
    from Clock import Clock
    
    sd = CardSD()
    clock = Clock()
    
    dht = MyDht(dht_pin=33, sd=sd, clock=clock)
    while True:
        dht.update()
        if not dht.update_enable:
            print(dht.readings[0]/5, dht.readings[1])
            dht.update_enable = True
        