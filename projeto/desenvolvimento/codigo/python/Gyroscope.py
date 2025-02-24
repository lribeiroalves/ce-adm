from machine import Pin, SoftI2C
from time import sleep, sleep_ms, ticks_ms
from Clock import Clock
from CardSD import CardSD

# SENSOR ADRRESSES
MPU = 0x68
PWR_MNGM = 0x6B
GYRO_ADDR = 0x43

# NÚMERO DE LEITURAS QUE SERÃO FEITAS POR AMOSTRA
N_LEITURAS = 10

class Gyroscope:
    """ Classe que implementa as funções de leitura do giroscopio
        do sensor MPU 5060 em tempos predefinidos """
    
    def __init__(self, scl_pin: int = 22, sda_pin: int = 21, time_ms: int = 100, sd:CardSD = None, clock:Clock = None):
        self.__i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = [0,0,0]
        self.__update_enable = True
        self.__count_readings = 0
        self.__clock = clock
        self.__sd = sd
        self.__csv = ''
        # if self.__sd and self.__clock: # Create Data logger
            # time = self.__clock.get_time()
            # self.__log_path = f'/sd/data_logger/gyro/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
            # self.__sd.write_data(self.__log_path, 'gX,gY,gZ,year,month,day,hour,minute,second\n', 'w')
        
        # acordar o sensor MPU 5060
        self.__i2c.writeto_mem(MPU, PWR_MNGM, bytes([0x00]))
        sleep_ms(5)
    
    
    @property
    def readings(self):
        for v in self.__readings:
            v = 0xfe if v == 0xff else v
        
        return self.__readings
    

    @property
    def csv(self):
        return self.__csv

    
    @property
    def update_enable(self):
        return self.__update_enable
    
    
    @update_enable.setter
    def update_enable(self, flag: bool):
        if flag == True:
            self.__update_enable = True
            self.__readings = [0, 0, 0]
            self.__csv = ''
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')        
    
    
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
        
        if self.__clock and self.__sd:
            time = self.__clock.get_time()
            # self.__sd.write_data(self.__log_path, f'{leitura[0]},{leitura[1]},{leitura[2]},{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]}\n', 'a')
            self.__csv += f'gyro,{leitura[0]},{leitura[1]},{leitura[2]},{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n'
        
        return leitura
    
    
    def update(self):
        """ Consulta os valores do giroscópio em períodos definidos """
        current_time = ticks_ms()
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            # realiza a leitura 10 vezes e calcula retorna a média
            if self.__count_readings < N_LEITURAS:
                # faz 1 leitura e armazena
                r = self.read_gyro()
                for i, v in enumerate(r):
                    self.__readings[i] = max(self.__readings[i], v)
                self.__count_readings += 1
            else:
                # calcula a média e retorna
                self.__count_readings = 0
                self.__update_enable = False


if __name__ == '__main__':
    from CardSD import CardSD
    from Clock import Clock
    
    sd = CardSD()
    clock = Clock()
    
    # Exemplo de aplicação da classe Giroscope
    gyro = Gyroscope(sd=sd, clock=clock)
    while True:
        gyro.update()
        if not gyro.update_enable:
            print(gyro.readings)
            gyro.update_enable = True
        