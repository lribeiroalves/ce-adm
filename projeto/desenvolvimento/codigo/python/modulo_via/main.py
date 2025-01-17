from machine import UART

from WIFI import WIFI
from MQTT import MQTT
from MyDht import MyDht
from Gyroscope import Gyroscope
from CalcADC import CalcADC
from Clock import Clock
from CardSD import CardSD

# PINOUT
PIN_DHT = 33
PIN_ADC = 34
PIN_SCL = 22
PIN_SDA = 21
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_LORA_RX = 26
PIN_LORA_TX =  27

# Endereçamento e tipos de mensagem
ESP_ADDR = 0x01 # Sensor em Teste -> 0x01, sensor de controle -> 0x02, esp da sala técnica -> 0x03
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
adc = CalcADC(PIN_ADC)
clock = Clock()
sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=4800, tx=PIN_LORA_TX, rx=PIN_LORA_RX)

# Definição do horário inicial do RTC interno
clock.set_time(ano=25, mes=1, dia=15, hora=0, minuto=0, segundo=0)

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
dte = clock.get_time()
logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}.csv'
sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,adc_int,adc_dec\n', 'w')


def criar_pacote() -> dict[str:dict[str:bytes], str:str, str:list[bytes]]:
    """ Construção do pacote de dados dos sensores """
    dte = clock.get_time()
    # dados brutos
    raw = {
        'addr': ESP_ADDR,
        'msg_type': MSG_TYPE['leitura'],
        'adc_int': adc.readings[0], 'adc_dec': adc.readings[1],
        'temp': dht.readings[0], 'umid': dht.readings[1],
        'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
        'year': dte['ano'] - 2000, 'month': dte['mes'], 'day': dte['dia'],
        'hour': dte['hora'], 'minute': dte['minuto'], 'second': dte['segundo']
    }
    # mensagem pronta para o datalog
    csv = f"{raw['day']},{raw['month']},{raw['year']},{raw['hour']},{raw['minute']},{raw['second']},{raw['umid']},{raw['temp']},{raw['gX']},{raw['gY']},{raw['gZ']},{raw['adc_int']},{raw['adc_dec']}\n"
    # mensagem pronta para transmissão LoRa
    lora_msg = [raw['addr'], raw['msg_type'], raw['day'], raw['month'], raw['year'], raw['hour'], raw['minute'], raw['second'], raw['umid'], raw['temp'], raw['gX'], raw['gY'], raw['gZ'], raw['adc_int'], raw['adc_dec']]
    
    return {'raw': raw, 'csv': csv, 'lora_msg':lora_msg}


# Conexão com WiFi e MQTT
# wifi.conectar()
# mqtt_client.conectar()
# topico_pub = 'adm/esp_sensor/server'
# topico_sub = ['adm/server/esp_sensor']
# mqtt_client.assinar_topicos(topico_sub)


# Função de callback para mensagens recebidas via MQTT
def callback(topic: bytes, msg: bytes):
    if topic.decode() == topico_sub[0]:
        print(topic.decode(), msg.decode())
# mqtt_client.definir_cb(callback)


# Leitura dos sensores e tratamento dos dados
while True:
    dht.update()
    gyro.update()
    adc.update()
#     mqtt_client.chk_msg() # Veirificar novas mensagens MQTT
    
    if [dht.update_enable, gyro.update_enable, adc.update_enable] == [0, 0, 0]:
        pacote = criar_pacote() # Criar o pacote com as informações
        sd.write_data(logger_path, pacote['csv'], 'a') # Salvar no SD
        lora.write(bytes(pacote['lora_msg'])) # Enviar os dados via LoRa
#         mqtt_client.publicar_mensagem(topico_pub, pacote['raw']) # Enviar os dados via MQTT
        # Habilitar novas leituras dos sensores
        dht.update_enable = True
        gyro.update_enable = True
        adc.update_enable = True
