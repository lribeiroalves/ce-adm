from machine import Pin, ADC
from time import ticks_ms

# NÚMERO DE LEITURAS QUE SERÃO FEITAS POR AMOSTRA
N_LEITURAS = 10

class CalcADC:
    """ Classe para implementação dos métodos de calculo e correção do ADC """
    def __init__(self, pin: int, time_ms: int = 100):
        self.__adc = ADC(Pin(pin))
        self.__adc.atten(ADC.ATTN_11DB)
        self.__adc.width(ADC.WIDTH_12BIT)
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__read = 0
        self.__readings = [0,0]
        self.__update_enable = True
        self.__count_readings = 0
        
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
            self.__readings = [0,0]
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')
    
    
    def __medir(self):
        """ Calcula a media de n medições do valor do ADC """
        valor_medido = 0
        medicoes = 100
        for c in range(0, medicoes):
            valor_medido += self.__adc.read()
        
        return valor_medido / medicoes
    
    
    def __corrige_erro(self, v: float):
        return 32.34 * (0.922 * (v * 3.6 / 4095) + 0.140) - 47.84
    
    
    def update(self):
        """ Realiza as medições corrige o erro n vezes """
        current_time = ticks_ms()
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            # realiza a leitura 10 vezes e calcula retorna a média
            if self.__count_readings < N_LEITURAS:
                r = self.__medir()
                r_corrigido = self.__corrige_erro(r)
                self.__read += r_corrigido
                self.__count_readings += 1
            else:
                self.__read = self.__read / N_LEITURAS
                r_inteiro = int(self.__read)
                r_decimal = self.__read - r_inteiro
                self.__readings[0] = r_inteiro
                self.__readings[1] = int(r_decimal * 100)
#                 self.__readings[0] = r_inteiro.to_bytes(1, 'little')
#                 self.__readings[1] = int(r_decimal * 100).to_bytes(1, 'little')
                self.__read = 0
                self.__count_readings = 0
                self.__update_enable = False


if __name__ == '__main__':
    adc = CalcADC(34)
    
    while True:
        adc.update()
        
        if not adc.update_enable:
            inteiro = adc.readings[0]
            decimal = adc.readings[1] / 100
#             inteiro = int.from_bytes(adc.readings[0], 'little')
#             decimal = int.from_bytes(adc.readings[1], 'little') / 100
            print(inteiro+decimal)
            
            adc.update_enable = True
            