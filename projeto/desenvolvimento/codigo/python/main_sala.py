from machine import UART
from time import sleep_ms

from WIFI import WIFI
from MQTT import MQTT
from CardSD import CardSD
from CalcADC import CalcADC
from Clock import Clock


# PINOUT
PIN_ADC = 34
PIN_LORA_RX = 23
PIN_LORA_TX = 22
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19

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
# adc = CalcADC(PIN_ADC)
# sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=4800, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
clock = Clock()


# Função para lidar com as mensagens recebidas nos tópicos mqtt assinados
def get_mqtt(topic, msg):
    pass


# Função para lidar com os pacotes recebidos via LoRa
def get_lora(packet: List[bytes], rssi_on:bool = True):
    if rssi_on:
        lora_msg = packet[:-1]
        rssi = packet[-1]
    else:
        lora_msg = packet
        rssi = None


# Definição do horário inicial do RTC interno
clock.set_time(ano=25, mes=1, dia=15, hora=0, minuto=0, segundo=0)

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
# dte = clock.get_time()
# logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}_{dte["hora"]}_{dte["minuto"]}_{dte["segundo"]}.csv'
# sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,adc_int,adc_dec\n', 'w')

# Conexão com WiFi e MQTT
wifi.conectar()
mqtt_client.conectar()
topico_pub = 'adm/esp_sala/server'
topico_sub = ['adm/server/esp_sala']
mqtt_client.assinar_topicos(topico_sub)
mqtt_client.definir_cb(get_mqtt)


# Loop
while True:
    if lora.any(): # Verificar novos pacote LoRa
        sleep_ms(100)
        packet = get_messages.lora([b for b in lora.read()])
    mqtt_client.chk_msg() # Verificar novas mensagens MQTT
    