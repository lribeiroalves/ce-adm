from machine import Pin, RTC, SPI, SoftI2C
import dht as DHT
import network
from time import sleep, sleep_ms, ticks_ms
from umqtt.simple import MQTTClient
import ujson
from sdcard import SDCard
import os
from ads import ads

# GYROSCOPE SENSOR ADDRESSES
MPU = 0x68
PWR_MNGM = 0x6B
GYRO_ADDR = 0x43

# ADS SENSOR ADDRESS
ADS1115_ADDRESS = 0x48

# NÚMERO DE LEITURAS QUE SERÃO FEITAS POR AMOSTRA
N_LEITURAS_GYRO = 10
N_LEITURAS_ADC = 7
N_LEITURAS_PIN = 10

################################################################################################################################################################################################################################################################################################################################################################################################################################################
class WIFI:
    """
        Classe para implementação da conexão com rede Wifi
        
        on_fail_conn: False (Default) -> Desiste após falha de conexão (20 tentativas de conectar)
        on_fail_conn: True -> Continua tentando conectar indefinidamente
        
    """
    
    def __init__(self, ssid: str, pswd: str, on_fail_conn: bool = False):
        self.__ssid = ssid
        self.__passwd = pswd
        self.__on_fail_conn = on_fail_conn
        self.__wifi = network.WLAN(network.STA_IF)
    
    @property
    def isconnected(self):
        return self.__wifi.isconnected()
    
    def conectar(self):
        """ Ligar a interface Wifi e conectar a uma rede """
        if not self.__wifi.active():
            self.__wifi.active(True)
        self.__wifi.connect(self.__ssid, self.__passwd)
        
        conn_counter = 21 if not self.__on_fail_conn else 0
        while True:
            if not self.__wifi.isconnected():
                conn_counter -= 1
                if conn_counter == 0:
                    print('Não foi possível conectar.')
                    while True:
                        pass
                print(f'Aguardando conexão...')
                sleep(0.5)
            else:
                print(f'Conectado ao WiFi: {self.__wifi.ifconfig()}')
                break
    
    def desconectar(self):
        """ Desconectar e desligar a interface WiFi """
        if self.__wifi.isconnected():
            self.__wifi.disconnect()
            print('WiFi desconectado...')
        if self.__wifi.active():
            self.__wifi.active(False)


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class MQTT:
    """ Classe para implementação do Cliente MQTT """
    
    def __init__(self, addr: str, user: str, pswd: str, port: int = 1883, callback_func = None):
        self.__addr = addr
        self.__mqtt_user = user
        self.__mqtt_pswd = pswd
        self.__client = MQTTClient('esp32', addr, port, user, pswd)
        if callback_func:
            self.__client.set_callback(callback_func)
        else:
            self.__client.set_callback(self.__on_message)
        self.__subscribed_topics = []
    
    
    @property
    def topicos_assinados(self) -> list:
        return self.__subscribed_topics
    
    
    def __is_connected(self):
        """ Verificação da conexão do Cliente MQTT """
        try:
            self.__client.ping()
            return True
        except Exception as e:
            return False
    
    
    def __on_message(self, topic: bytes, msg: bytes):
        """ Função de callback para tratamento das mensagens que chegam aos tópicos assinados """
        if topic == b'test/esp/topic':
            print(msg.decode())
        else:
            print(f'Topic: {topic.decode()} - Message: {msg.decode()}')
    
    
    def conectar(self):
        """ Tenta conectar ao broker MQTT e para a execução caso não consiga """
        try:
            self.__client.connect()
            print(f'Conectado ao Broker MQTT: {self.__addr}')
        except OSError as e:
            print(f'Erro ao conectar ao Broker MQTT: {e}')
            sleep(0.5)
            self.conectar()
    
    
    def desconectar(self):
        """ Desconecta do broker MQTT """
        self.__client.disconnect()
        print(f'Desconectado do broker MQTT: "{self.__addr}"')
    
    
    def definir_cb(self, cb_func, clock=None):
        """ Definir função de callback """
        if callable(cb_func):
            if clock:
                self.__client.set_callback(lambda topic, msg: cb_func(topic, msg, clock))
            else:
                self.__client.set_callback(cb_func)
        else:
            print('É necessário passar um callable com 2 argumentos Ex:"callback_function(topic, msg)"')
    
    
    def assinar_topicos(self, topics: list[str]):
        """ Assina um topico, caso ainda nao exista essa assinatura """
        for topic in topics:
            topic = str(topic)
            if topic not in self.__subscribed_topics:
                self.__client.subscribe(topic)
                self.__subscribed_topics.append(topic)
                print(f'Assinatura ao tópico "{topic}" realizada com sucesso.')
            else:
                print(f'Já existe uma assinatura ativa ao tópico "{topic}".')

    
    def cancelar_topicos(self, topics: list[str]):
        """ Cancela a assinatura de um topico, caso ela exista """
        for topic in topics[0:]:
            try:
                self.__subscribed_topics.remove(topic)
            except ValueError as e:
                print(f'Não existe uma assinatura ativa ao topico "{topic}".')
        print('Cancelando assinaturas...')
        
        self.__client.disconnect()
        self.__client.connect()
        for t in self.__subscribed_topics:
            self.__client.subscribe(t)
        for topic in topics[0:]:
            print(f'Assinatura ao topico {topic} cancelada.')
    
    
    def publicar_mensagem(self, topic: str, pub_msg: dict):
        """ Publica uma mensagem (dict) em um tópico """
        json_msg = ujson.dumps(pub_msg)
        if self.__is_connected():
            self.__client.publish(topic=topic, msg=json_msg, retain=False, qos=0)
        else:
            print('Cliente não está conectado ao broker MQTT')
            self.conectar()
    
    
    def chk_msg(self, wait_msg: bool = False):
        """ Verificar novas mensagens """
        if self.__is_connected():
            if not wait_msg:
                self.__client.check_msg()
            else:
                self.__client.wait_msg()
        else:
            print('Cliente não está conectado ao broker MQTT')
            self.conectar()


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class Clock:
    """ Classe criada com o objetivo de faciliar
        a implementação do uso do RTC interno do ESP32 """
    
    def __init__(self):
        self.__rtc = RTC()
        self.__rtc.datetime((2025, 1, 1, 0, 0, 0, 0, 0))
        self.__keys = ['ano', 'mes', 'dia', 'semana', 'hora', 'minuto', 'segundo', 'm_seg']
        self.__is_set = False
    
    
    @property
    def is_set(self):
        return self.__is_set
    
    
    @is_set.setter
    def is_set(self, value:bool):
        if value == False:
            self.__is_set = False
        else:
            raise ValueError('Esse atributo só pode ser alterado para falso.')
    
    
    def get_time(self):
        """ Retorna as informações do rtc interno em forma de um dicionario """
        return {self.__keys[k]: v for k, v in enumerate(self.__rtc.datetime())}
    
    
    def set_time(self, ano: int, mes: int, dia: int,
                 hora: int, minuto: int, segundo: int):
        """ Define um novo horário para o rtc interno """
        # NECESSÁRIO TRATAR POSSÍVEIS ERROS DE DATAS INSERIDAS PELO USUÁRIO
        if ano < 100:
            ano += 2000
        
        self.__rtc.datetime((ano, mes, dia, 0, hora, minuto, segundo, 0))
        self.__is_set = True


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class CardSD:
    """ Classe para utilização do barramento SPI para comunicação com cartão SD """
    
    def __init__(self, pin_cs: int = 5, pin_sck: int = 18, pin_mosi: int = 23, pin_miso: int = 19):
        self.__spi = SPI(1,baudrate=1000000, phase=0, polarity=0, sck=Pin(pin_sck), mosi=Pin(pin_mosi), miso=Pin(pin_miso))
        self.__sd = SDCard(self.__spi, Pin(pin_cs))
        os.mount(self.__sd, '/sd')
    
    
    def __dir(self, path):
        caminho = '/'.join(path.split('/')[:-1])
        arquivo = path.split('/')[-1]
        
        try:
            diretorio = os.listdir(caminho)
        except OSError:
            raise ValueError('Directory not Found')
        
        return diretorio, arquivo
        
    
    def list_files(self, path):
        """ List all files and directories on the path """
        try:
            for item in os.listdir(path):
                full_path = path + '/' + item
                if os.stat(full_path)[0] & 0x4000:  # Verifica se é um diretório
                    print(f'DIR: {full_path}')
                    self.list_files(full_path)  # Lista arquivos no diretório
                else:
                    print(f'FILE: {full_path}')
        except OSError:
            raise ValueError('Path Fot Found.')
    
    
    def write_data(self, path: str, data: str, mode: str = 'w'):
        """ Escrever no cartão SD - 'mode' pode assumir 'A' ou 'W' para concatenar ao arquivo ou limpar e escrever """
        if mode.lower() in ['a', 'w']:
            # Criar diretório se não existir
            dir_path = '/'.join(path.split('/')[:-1])
            try:
                os.listdir(dir_path)
            except OSError: # Recursivamente cria o diretorio
                directory = ''
                for d in dir_path.split('/')[1:]:
                    directory = f'{directory}/{d}'
                    try:
                        os.listdir(directory)
                    except OSError:
                        os.mkdir(directory)
            # Escrever dados no arquivo
            with open(path, mode.lower()) as file:
                file.write(data)
        else:
            raise ValueError('mode must be "a" or "w"')
    
    
    def read_data(self, full_path):
        """ Tenta ler os dados de um arquivo e retorna um ValueError se nao encontrar o arquivo. """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            with open(full_path, 'r') as file:
                print(file.read())
        else:
            raise ValueError('File Not Found.')
    
    
    def clear_file(self, full_path):
        """ Limpa os dados de um arquivo """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            self.write_data(full_path, '', 'w')
        else:
            raise ValueError('File Not Found.')
    
    
    def delete_from_card(self, full_path):
        """ Delete um arquivo ou diretorio do Cartão SD """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            if os.stat(full_path)[0] & 0X4000:
                for file in os.listdir(full_path):
                    file_path = full_path + '/' + file
                    if os.stat(full_path)[0] & 0X4000:
                        self.delete_from_card(file_path)
                    else:
                        os.remove(file_path)
                os.rmdir(full_path)
            else:
                os.remove(full_path)
        else:
            raise ValueError('File Not Found')


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class MyDht:
    """ Classe para implementação específica do uso do modulo dht
    para leituras de umidade e temperatura em períodos predefinidos"""
    
    def __init__(self, dht_pin: int = 33, time_ms: int = 1000, clock:Clock = None, sd:CardSD = None):
        self.__dht_object = DHT.DHT11(Pin(dht_pin))
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = [0, 0]
        self.__prev_reading = [0, 0]
        self.__update_enable = True
        self.__clock = clock
        self.__sd = sd
        self.__csv = ''
        # if self.__sd and self.__clock: # Create Data logger
        #     time = self.__clock.get_time()
        #     self.__log_path = f'/sd/data_logger/dht/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
        #     self.__sd.write_data(self.__log_path, 'temp,umid,year,month,day,hour,minute,second\n', 'w')
    
    
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
            self.__prev_reading = self.__readings
            self.__readings = [0, 0]
            self.__csv = ''
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
                self.__csv += f'dht,{r[0]},{r[1]},0,{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n'
                # self.__sd.write_data(self.__log_path, f'{r[0]},{r[1]},{time["ano"] - 2000},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]}\n', 'a')
            return r
        except OSError:
            return (self.__prev_reading[0], self.__prev_reading[1])
#             sleep_ms(10)
#             return self.read_dht()
        except Exception as err:
            print(err)
            return (254, 254)
    
    
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


################################################################################################################################################################################################################################################################################################################################################################################################################################################
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
            if self.__count_readings < N_LEITURAS_GYRO:
                # faz 1 leitura e armazena
                r = self.read_gyro()
                for i, v in enumerate(r):
                    self.__readings[i] = max(self.__readings[i], v)
                self.__count_readings += 1
            else:
                # calcula a média e retorna
                self.__count_readings = 0
                self.__update_enable = False


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class ADC:
    """ Classe para implementação específica do uso do sensor ADS1115 """
    def __init__(self, scl_pin: int, sda_pin: int, canal: int = 0, get_pino:bool = False, time_ms: int = 70, clock:Clock = None, sd:CardSD = None):
        self.__i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.__adc = ads.ADS1115(ADS1115_ADDRESS, i2c=self.__i2c)
        self.__canal = canal if canal <= 3 else 0
        self.__get_pino = get_pino
        self.__config()
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__read = 0
        self.__readings = [0,0]
        self.__update_enable = True
        self.__count_readings = 0
        self.__clock = clock
        self.__csv = ''
        self.__sd = sd
        # if self.__sd and self.__clock: # Create Data logger
        #     time = self.__clock.get_time()
        #     self.__log_path = f'/sd/data_logger/adc/canal{self.__canal}/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
        #     self.__sd.write_data(self.__log_path, 'tensao,year,month,day,hour,minute,second,mili_second\n', 'w')
    

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
            self.__readings = [0,0]
            self.__csv = ''
#             self.__sd.write_data(self.__log_path, self.__csv, 'a')
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')
    

    def __config(self):
        """ Configurações iniciais do sensor """
        self.__adc.setVoltageRange_mV(ads.ADS1115_RANGE_6144) # Define o range de leitura de 0 a 6,144V
        self.__adc.setMeasureMode(ads.ADS1115_SINGLE) # Define que as medições serão realizadas em single shot
    

    def __leitura(self, retorna_pino: bool = False, escreve_csv: bool = True):
        """ Leitura única do sensor em mV """
        fator_conversao = 7.946 # Fator de conversão para uso do divisor de tensão
        channels = [ads.ADS1115_COMP_0_GND, ads.ADS1115_COMP_1_GND, ads.ADS1115_COMP_2_GND, ads.ADS1115_COMP_3_GND]
        self.__adc.setCompareChannels(channels[self.__canal]) # Define em qual pino a leitura será realizada
        self.__adc.startSingleMeasurement()
        while self.__adc.isBusy():
            pass
        
        leitura_V = self.__adc.getResult_V()
        leitura_mV = self.__adc.getResult_mV()
        leitura_V, leitura_mV = (0,0) if leitura_V < 0 or leitura_mV < 0 else (leitura_V, leitura_mV)
        leitura_convertida = leitura_V * fator_conversao

        if self.__clock and self.__sd and escreve_csv:
            time = self.__clock.get_time()
            v = leitura_V if retorna_pino else leitura_convertida
            self.__csv += f'adc_{self.__canal},{v},0,0,{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n'
        
        return leitura_V if retorna_pino else leitura_convertida
    

    def update(self):
        """ Realiza as medições e calcula a média """
        current_time = ticks_ms()
        
        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            # realiza a leitura 10 vezes e calcula retorna a média
            if self.__count_readings < N_LEITURAS_ADC:
                self.__read += self.__leitura(self.__get_pino)
                self.__count_readings += 1
            else:
                self.__read = self.__read / N_LEITURAS_ADC
                r_inteiro = int(self.__read)
                r_decimal = self.__read - r_inteiro
                self.__readings[0] = r_inteiro
                self.__readings[1] = int(r_decimal * 100)
                self.__read = 0
                self.__count_readings = 0
                self.__update_enable = False
    

    def leitura_mqtt(self):
        leitura = self.__leitura(self.__get_pino)
        inteiro = int(leitura)
        decimal = leitura - inteiro

        return [inteiro, int(decimal * 100)]
    
    
    def clear_csv(self):
        self.__csv = ''


################################################################################################################################################################################################################################################################################################################################################################################################################################################
class OptoPin:
    """ Classe que implementa a leitura automática de um pino ligado ao sinal de Reset dos SDDs """

    def __init__(self, pin:int, name:str, time_ms:int = 100, sd:CardSD = None, clock:Clock = None):
        self.__pin = Pin(pin)
        self.__name = name
        self.__read_time = time_ms
        self.__previous_time = 0
        self.__readings = 0
        self.__update_enable = True
        self.__count_readings = 0
        self.__clock = clock
        self.__sd = sd
        self.__csv = ''
        # if self.__sd and self.__clock: # Create Data logger
        #     time = self.__clock.get_time()
        #     self.__log_path = f'/sd/data_logger/reset/pin_{pin}/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
        #     self.__sd.write_data(self.__log_path, 'pin_state,year,month,day,hour,minute,second,mili_second\n', 'w')
        

    @property
    def readings(self):
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
            self.__readings = 0
            self.__csv = ''
        else:
            raise ValueError('Esse atributo só pode ser alterado para verdadeiro.')


    def __read(self):
        """ Fazer a leitura do pino """
        pin_state = self.__pin.value()

        if self.__clock and self.__sd:
            time = self.__clock.get_time()
            self.__csv += f'{self.__name},{pin_state},0,0,{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n'
            # self.__sd.write_data(self.__log_path, f'{pin_state},{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n', 'a')
        
        self.__readings = pin_state if not self.__readings else 1


    def update(self):
        """ Controle  fluxo de leituras e retornos """
        current_time = ticks_ms()

        if current_time >= self.__previous_time + self.__read_time and self.__update_enable:
            self.__previous_time = current_time
            if self.__count_readings < N_LEITURAS_PIN:
                self.__read()
                self.__count_readings += 1
            else:
                self.__count_readings = 0
                self.__update_enable = False
    

    def leitura_mqtt(self):
        leitura = self.__pin.value()

        if self.__clock and self.__sd:
            time = self.__clock.get_time()
            self.__csv += f'{self.__name},{leitura},0,0,{time["ano"]},{time["mes"]},{time["dia"]},{time["hora"]},{time["minuto"]},{time["segundo"]},{time["m_seg"]}\n'

        return [leitura]
    
    
    def clear_csv(self):
        self.__csv = ''
        