from machine import Pin, SoftI2C
from time import sleep, sleep_ms, ticks_ms

MPU = 0x68
PWR_MNGM = 0x6B
GYRO_ADDR = 0x43

class Gyroscope:
    """ Classe que implementa as funções de leitura do giroscopio
        do sensor MPU 5060 em tempos predefinidos """
    
    def __init__(self, scl_pin: int = 22, sda_pin: int = 21, time_ms: int = 100):
        self.__i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = [0,0,0]
        self.__update_enable = True
        self.__count_readings = 0
        
        # acordar o sensor MPU 5060
        self.__i2c.writeto_mem(MPU, PWR_MNGM, bytes([0x00]))
        sleep_ms(5)
    
    
    def __make_signed(self, num: int) -> int:
        """ Recebe um inteiro de 16 bits com sinal e retorna seu valor corrigido """
        if num & (1 << 15): # Verifica se o primeiro bit do número é 1
            return num - (1 << 16) # Usa o complemento de 2 para 16 bits
        else:
            return num
    
    
    def read_gyro(self):
        """ Realizar uma leitura dos dados do giroscópio """
        r = self.__i2c.readfrom_mem(MPU, GYRO_ADDR, 6)
        
        # separa a leitura por eixos e faz a união dos bytes mais e menos significativos
        eixos = [
            r[0] << 8 | r[1],
            r[2] << 8 | r[3],
            r[4] << 8 | r[5]
        ]
        
        leitura = []
        
        for eixo in eixos:
            # torna o valor absoluto, retira ruidos, considera apenas valores acima de zero e converte em um byte (cada eixo)
            leitura.append(max([0, abs(self.__make_signed(eixo)) - 100]) >> 7)
        
        return leitura
    
    
    def update(self):
        """ Consulta os valores do giroscópio em períodos definidos """
        current_time = ticks_ms()
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            # realiza a leitura 10 vezes e calcula retorna a média
            if self.__count_readings < 10:
                # faz 1 leitura e armazena ----------------------------------
                self.__count_readings += 1
            else:
                # calcula a média e retorna ---------------------------------
                self.__count_readings = 0
                self.__update_enable = False

if __name__ == '__main__':
    gyro = Gyroscope()
    
    while True:
        print(gyro.read_gyro())
        sleep(1)