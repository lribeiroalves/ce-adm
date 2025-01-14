from machine import UART

from WIFI import WIFI
from MQTT import MQTT
from MyDht import MyDht
from Gyroscope import Gyroscope
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
ESP_ADDR = 0x01 # Sensor em Teste -> 0x01, sensor de controle -> 0x02, esp da sala técnica -> 0x03
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}

# Criar instancias
wifi = WIFI(ssid='ssid', pswd='pswd')
mqtt_client = MQTT(addr='server_ip', user='esp32', pswd='esp32')
dht = MyDht(PIN_DHT)
gyro = Gyroscope(PIN_SCL, PIN_SDA)
clock = Clock()
sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=1200, tx=PIN_LORA_TX, rx=PIN_LORA_RX)

# Definição do horário inicial do RTC interno
clock.set_time(ano=25, mes=1, dia=3, hora=18, minuto=23, segundo=40)

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
dte = clock.get_time()
logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}.csv'
sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ\n', 'w')


def criar_pacote() -> dict[str:dict[str:bytes], str:str, str:list[bytes]]:
    """ Construção do pacote de dados dos sensores """
    dte = clock.get_time()
    # dados brutos
    raw = {
        'addr': ESP_ADDR,
        'msg_type': MSG_TYPE['leitura'],
        'temp': dht.readings[0], 'umid': dht.readings[1],
        'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
        'year': dte['ano'] - 2000, 'month': dte['mes'], 'day': dte['dia'],
        'hour': dte['hora'], 'minute': dte['minuto'], 'second': dte['segundo']
    }
    # mensagem pronta para o datalog
    csv = f"{raw['day']},{raw['month']},{raw['year']},{raw['hour']},{raw['minute']},{raw['second']},{raw['umid']},{raw['temp']},{raw['gX']},{raw['gY']},{raw['gZ']}\n"
    
    lora_msg = [raw['addr'], raw['msg_type'], raw['day'], raw['month'], raw['year'], raw['hour'], raw['minute'], raw['second'], raw['umid'], raw['temp'], raw['gX'], raw['gY'], raw['gZ']]
    
    return {'raw': raw, 'csv': csv, 'lora_msg':lora_msg}


# Conexão com WiFi e MQTT
wifi.conectar()
mqtt_client.conectar()
topico_pub = 'adm/esp_sensor/server'
topico_sub = ['adm/server/esp_sensor']
mqtt_client.inscrever_topicos(topico_sub)


# Função de callback para mensagens recebidas via MQTT
def callback(topic: bytes, msg: bytes):
    if topic.decode() == topico_sub[0]:
        print(topic.decode(), msg.decode())
        
        
mqtt_client.definir_cb(callback)

# Leitura dos sensores e tratamento dos dados
while True:
    dht.update()
    gyro.update()
    mqtt_client.chk_msg()
    
    if not dht.update_enable and not gyro.update_enable:
        # Criar o pacote com as informações
        pacote = criar_pacote()
        print(pacote)
        # Salvar no SD
        sd.write_data(logger_path, pacote.csv, 'a')
        # Enviar os dados via LoRa
        lora.write(bytes(pacote.lora_msg))
        # Enviar os dados via MQTT
        mqtt_client.publicar_mensagem(topico_pub, pacote.raw)
        # Habilitar novas leituras dos sensores
        dht.update_enable = True
        gyro.update_enable = True
