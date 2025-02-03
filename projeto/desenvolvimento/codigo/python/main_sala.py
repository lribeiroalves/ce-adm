from machine import UART, Pin
from time import sleep_ms
import ujson

from CRC16 import *
from WIFI import WIFI
from MQTT import MQTT
from CardSD import CardSD
from ADC import ADC
from Clock import Clock
from funcoes_ajuda import atualizar_clock, get_lora, get_mqtt, criar_pacote

# PINOUT
PIN_LORA_RX = 23
PIN_LORA_TX = 22
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_SCL = 22
PIN_SDA = 21
PIN_SENSOR_RESET = 36
PIN_SENSOR_OCC = 39
PIN_CONTROLE_RESET = 34
PIN_CONTROLE_OCC = 35

# # Endereçamento e tipos de mensagem
# ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
# MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}

# Endereços de Rede e Broker MQTT
WIFI_SSID = 'SCA_Instrumentos'
# WIFI_SSID = 'Galaxy S22EAA7'
# WIFI_SSID = 'ADM_SSV'
# WIFI_SSID = '2GNETVIRTUA_AP1811'
WIFI_PSWD = 'SCAOnline'
# WIFI_PSWD = 'tbtt6469'
# WIFI_PSWD = '244466666'
# WIFI_PSWD = '194267140'
BROKER_ADRR = '192.168.0.112'
BROKER_PORT = 1883
MQTT_USER = 'esp32'
MQTT_PSWD = 'esp32'

# Criar instancias
wifi = WIFI(ssid=WIFI_SSID, pswd=WIFI_PSWD)
mqtt_client = MQTT(addr=BROKER_ADRR, user=MQTT_USER, pswd=MQTT_PSWD, port=BROKER_PORT)
adc0 = ADC(PIN_SCL, PIN_SDA, canal = 0)
adc1 = ADC(PIN_SCL, PIN_SDA, canal = 1)
adc2 = ADC(PIN_SCL, PIN_SDA, canal = 2)
adc3 = ADC(PIN_SCL, PIN_SDA, canal = 3)
occ_sensor = Pin(PIN_SENSOR_OCC)
occ_controle = Pin(PIN_CONTROLE_OCC)
reset_sensor = Pin(PIN_SENSOR_RESET)
reset_controle = Pin(PIN_CONTROLE_RESET)
sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=115200, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
clock = Clock()

# Conexão com WiFi e MQTT
wifi.conectar()
mqtt_client.conectar()
topico_pub = ['adm/esp_sala/server/reading', 'adm/esp_sala/server/req_time']
topico_sub = ['adm/server/esp_sala']
mqtt_client.assinar_topicos(topico_sub)
mqtt_client.definir_cb(cb_func=get_mqtt, clock=clock)

# Definição do horário inicial do RTC interno (Requisição ao servidor)
atualizar_clock(esp='sala', lora=lora, mqtt=mqtt_client, clock=clock)

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
time = clock.get_time()
logger_path = f'/sd/data_logger/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,adc_int,adc_dec\n', 'w')

# Loop
while True:
    if lora.any(): # Verificar novos pacote LoRa
        sleep_ms(10) #10ms garante pacotes de até 144 Bytes (4 pacotes completos)
        buffer = [b for b in lora.read()]
        get_lora(buffer, lora=lora, mqtt=mqtt_client, clock=clock)
    mqtt_client.chk_msg() # Verificar novas mensagens MQTT

    # Coletar dados de occ e reset

    # Verificar se os dados foram coletados, armazenar localmente, criar pacote e enviar ao servidor via MQTT
    