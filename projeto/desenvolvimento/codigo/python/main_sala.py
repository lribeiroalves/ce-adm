from machine import UART
from time import sleep_ms
import ujson

from CRC16 import *
from WIFI import WIFI
from MQTT import MQTT
from CardSD import CardSD
from ADC import ADC
from Clock import Clock


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


# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}


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
# adc = ADC(PIN_SCL, PIN_SDA, canal = 0)
# sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=115200, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
clock = Clock()


# Função para lidar com as mensagens recebidas nos tópicos mqtt assinados
new_time = None
def get_mqtt(topic, msg):
    topic, msg = topic.decode(), msg.decode()
    
    if topic == topico_sub[0]:
        global new_time
        new_time = ujson.loads(msg)


# Conexão com WiFi e MQTT
wifi.conectar()
mqtt_client.conectar()
topico_pub = ['adm/esp_sala/server/reading', 'adm/esp_sala/server/req_time']
topico_sub = ['adm/server/esp_sala']
mqtt_client.assinar_topicos(topico_sub)
mqtt_client.definir_cb(get_mqtt)


# Definição do horário inicial do RTC interno (Requisição ao servidor)
req_time = {'addr': ESP_ADDR['sala'], 'msg_type': MSG_TYPE['clock_get'], 'check': 0x42}
while True:
    print('Requisitando horário ao servidor')
    mqtt_client.publicar_mensagem(topico_pub[1], req_time)
    for _ in range(2000):
        mqtt_client.chk_msg()
        if new_time:
            break
        sleep_ms(5)
    if new_time:
        clock.set_time(ano=new_time['year'], mes=new_time['month'], dia=new_time['day'], hora=new_time['hour'], minuto=new_time['minute'], segundo=new_time['second'])
        time = clock.get_time()
        print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
        break


# Construção dos pacotes de transmissão e registro local
def criar_pacote(msg: list[bytes], tipo: str):
    if tipo == 'via':
        pacote = {
                'addr_from': msg[0], 'addr_to': msg[1],
                'msg_type': msg[2],
                'day': msg[3], 'month': msg[4], 'year': msg[5],
                'hour': msg[6], 'minute': msg[7], 'second': msg[8],
                'umid': msg[9], 'temp': msg[10],
                'gX': msg[11], 'gY': msg[12], 'gZ': msg[13],
                'ad_sen_int': msg[14], 'ad_sen_dec': msg[15],
                'ad_bat_int': msg[16], 'ad_bat_dec': msg[17]
        } 
        return pacote
    elif tipo == 'sala':
        pass


# Função para separar o buffer recebido em cada mensagem 
def separar_buffer(buffer:list):
    mensagens_separadas = []
    final = [0xFF, 0xFF, 0xFF]
    final_len = len(final)
    buffer_len = len(buffer)
    
    if buffer_len >= final_len + 5:
        for i in range(buffer_len - final_len + 1):
            if buffer[i:i + final_len] == final:
                mensagem = buffer[i - buffer[i + final_len]: i + final_len + 4]
                mensagens_separadas.append(mensagem)
    
    return mensagens_separadas
 

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
# dte = clock.get_time()
# logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}_{dte["hora"]}_{dte["minuto"]}_{dte["segundo"]}.csv'
# sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,adc_int,adc_dec\n', 'w')


# Loop
while True:
    if lora.any(): # Verificar novos pacote LoRa
        sleep_ms(10) #10ms garante pacotes de até 144 Bytes (4 pacotes completos)
        buffer = [b for b in lora.read()]
        get_lora(buffer)
    mqtt_client.chk_msg() # Verificar novas mensagens MQTT
    