from machine import UART
from time import sleep

from CRC16 import *
from WIFI import WIFI
from MQTT import MQTT
from MyDht import MyDht
from Gyroscope import Gyroscope
from ADC import ADC
from Clock import Clock
from CardSD import CardSD

# PINOUT
PIN_DHT = 33
PIN_SCL = 22
PIN_SDA = 21
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_LORA_RX = 26
PIN_LORA_TX =  27

# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}

# Endereços de Rede e Broker MQTT
# WIFI_SSID = 'SCA_Instrumentos'
# WIFI_SSID = 'Galaxy S22EAA7'
WIFI_SSID = '2GNETVIRTUA_AP1811'
# WIFI_PSWD = 'SCAOnline'
# WIFI_PSWD = 'tbtt6469'
WIFI_PSWD = '194267140'
BROKER_ADRR = '192.168.0.10'
BROKER_PORT = 1883
MQTT_USER = 'esp32'
MQTT_PSWD = 'esp32'

# Criar instancias
wifi = WIFI(ssid=WIFI_SSID, pswd=WIFI_PSWD)
mqtt_client = MQTT(addr=BROKER_ADRR, user=MQTT_USER, pswd=MQTT_PSWD, port=BROKER_PORT)
dht = MyDht(PIN_DHT)
gyro = Gyroscope(PIN_SCL, PIN_SDA)
adc = ADC(PIN_SCL, PIN_SDA)
adc2 = ADC(PIN_SCL, PIN_SDA, canal=1, get_pino=True)
clock = Clock()
sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=4800, tx=PIN_LORA_TX, rx=PIN_LORA_RX)


# Variáveis globais de controle
clock_setted = False


# Função para lidar com os pacotes recebidos via LoRa
def get_lora(packet:list[bytes], rssi_on:bool = True):
    if rssi_on:
        lora_msg = packet[:-1]
        rssi = -(256-packet[-1])
    else:
        lora_msg = packet
        rssi = None
    
    # Verificação do checksum (CRC-16)
    lora_msg = verificar_crc16(lora_msg)
    
    
    if lora_msg and lora_msg[1] == ESP_ADDR['teste']:
        # Receber clock set do esp da sala
        if len(lora_msg) == 9 and lora_msg[2] == MSG_TYPE['clock_set']:
            global clock_setted
            clock.set_time(ano = lora_msg[3], mes = lora_msg[4], dia = lora_msg[5], hora = lora_msg[6], minuto = lora_msg[7], segundo = lora_msg[8])
            time = clock.get_time()
            print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
            clock_setted = True
            

# Requisição de hora
req_time = [ESP_ADDR['teste'], ESP_ADDR['sala'], MSG_TYPE['clock_get'], 0x42] # Construção da mensagem de requisição de hora
checksum = calcular_crc16(req_time)[0:2] # Calculo do Checksum
for byte in checksum:
    req_time.append(byte)
while not clock_setted:
    lora.write(bytes(req_time))
    sleep(1)    
    if lora.any():
        sleep(0.05)
        packet = [b for b in lora.read()]
        get_lora(packet)


# Criação do arquivo data_logger.txt que armazenará as informações de leituras
dte = clock.get_time()
logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}_{dte["hora"]}_{dte["minuto"]}_{dte["segundo"]}.csv'
sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,ad_sen_int,ad_sen_dec,ad_bat_int,ad_bat_dec\n', 'w')


def criar_pacote() -> dict[str:dict[str:bytes], str:str, str:list[bytes]]:
    """ Construção do pacote de dados dos sensores """
    dte = clock.get_time()
    # dados brutos
    raw = {
        'addr': ESP_ADDR['teste'],
        'msg_type': MSG_TYPE['leitura'],
        'ad_sen_int': adc.readings[0], 'ad_sen_dec': adc.readings[1],
        'ad_bat_int': adc2.readings[0], 'ad_bat_dec': adc2.readings[1],
        'temp': dht.readings[0], 'umid': dht.readings[1],
        'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
        'year': dte['ano'] - 2000, 'month': dte['mes'], 'day': dte['dia'],
        'hour': dte['hora'], 'minute': dte['minuto'], 'second': dte['segundo']
    }
    # mensagem pronta para o datalog
    csv = f"{raw['day']},{raw['month']},{raw['year']},{raw['hour']},{raw['minute']},{raw['second']},{raw['umid']},{raw['temp']},{raw['gX']},{raw['gY']},{raw['gZ']},{raw['ad_sen_int']},{raw['ad_sen_dec']},{raw['ad_bat_int']},{raw['ad_bat_dec']}\n"
    # mensagem pronta para transmissão LoRa
    lora_msg = [raw['addr'], ESP_ADDR['sala'], raw['msg_type'], raw['day'], raw['month'], raw['year'], raw['hour'], raw['minute'], raw['second'], raw['umid'], raw['temp'], raw['gX'], raw['gY'], raw['gZ'], raw['ad_sen_int'], raw['ad_sen_dec'], raw['ad_bat_int'], raw['ad_bat_dec']]
    lora_msg += [0xFF, 0xFF, 0xFF, len(lora_msg)] # Adiciona uma tag de final de mensagem
    checksum = calcular_crc16(lora_msg)[0:2]
    for byte in checksum:
        lora_msg.append(byte)
    
    return {'raw': raw, 'csv': csv, 'lora_msg':lora_msg}


# Conexão com WiFi e MQTT
# wifi.conectar()
# mqtt_client.conectar()
# topico_pub = 'adm/esp_sensor/server'
# topico_sub = ['adm/server/esp_sensor']
# mqtt_client.assinar_topicos(topico_sub)


# Função de callback para mensagens recebidas via MQTT
# def callback(topic: bytes, msg: bytes):
#     if topic.decode() == topico_sub[0]:
#         print(topic.decode(), msg.decode())
# mqtt_client.definir_cb(callback)


# Leitura dos sensores e tratamento dos dados
while True:
    dht.update()
    gyro.update()
    adc.update()
    adc2.update()
#     mqtt_client.chk_msg() # Veirificar novas mensagens MQTT
    
    if [dht.update_enable, gyro.update_enable, adc.update_enable, adc2.update_enable] == [0] * 4:
        pacote = criar_pacote() # Criar o pacote com as informações
        sd.write_data(logger_path, pacote['csv'], 'a') # Salvar no SD
        lora.write(bytes(pacote['lora_msg'])) # Enviar os dados via LoRa
#         mqtt_client.publicar_mensagem(topico_pub, pacote['raw']) # Enviar os dados via MQTT
        # Habilitar novas leituras dos sensores
        dht.update_enable = True
        gyro.update_enable = True
        adc.update_enable = True
        adc2.update_enable = True
