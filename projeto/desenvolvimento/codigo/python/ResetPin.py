from machine import Pin
from time import sleep_ms, ticks_ms
from Clock import Clock
from CardSD import CardSD

# NÚMERO DE LEITURAS QUE SERÃO FEITAS POR AMOSTRA
N_LEITURAS = 10

class ResetPin:
    """ Classe que implementa a leitura automática de um pino ligado ao sinal de Reset dos SDDs """

    def __init__(self, pin:int, time_ms:int = 100, sd:CardSD = None, clock:Clock = None):
        self.__pin = Pin(pin)
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = 0
        self.__update_enable = True
        self.__count_readings = 0
        self.__clock = clock
        self.__sd = sd
        if self.__sd and self.__clock: # Create Data logger
            time = self.__clock.get_time()
            self.__log_path = f'/sd/data_logger/reset/pin_{pin}/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
            self.__sd.write_data(self.__log_path, 'pin_state,year,month,day,hour,minute,second,mili_second\n', 'w')
        

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
            self.__readings = 0
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')


    def __read(self):
        """ Fazer a leitura do pino """
        pin_state = self.__pin.value()

        if self.__clock and self.__sd:
            time = self.__clock.get_time()
            self.__sd.write_data(self.__log_path, f'{pin_state},{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n', 'a')
        
        self.__readings = pin_state if not self.__readings else 1


    def update(self):
        """ Controle  fluxo de leituras e retornos """
        current_time = ticks_ms()

        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            if self.__count_readings < N_LEITURAS:
                self.__read()
                self.__count_readings += 1
            else:
                self.__count_readings = 0
                self.__update_enable = False



if __name__ == '__main__':
    pin = ResetPin(33)
    
    while True:
        pin.update()
        
        if not pin.update_enable:
            print('OK')
            pin.update_enable = True