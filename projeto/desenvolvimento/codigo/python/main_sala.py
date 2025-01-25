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


# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}


# Endereços de Rede e Broker MQTT
# WIFI_SSID = 'SCA_Instrumentos'
# WIFI_SSID = 'Galaxy S22EAA7'
# WIFI_SSID = 'ADM_SSV'
WIFI_SSID = '2GNETVIRTUA_AP1811'
# WIFI_PSWD = 'SCAOnline'
# WIFI_PSWD = 'tbtt6469'
# WIFI_PSWD = '244466666'
WIFI_PSWD = '194267140'
BROKER_ADRR = '192.168.0.10'
BROKER_PORT = 1883
MQTT_USER = 'esp32'
MQTT_PSWD = 'esp32'


# Criar instancias
wifi = WIFI(ssid=WIFI_SSID, pswd=WIFI_PSWD)
mqtt_client = MQTT(addr=BROKER_ADRR, user=MQTT_USER, pswd=MQTT_PSWD, port=BROKER_PORT)
# adc = ADC(PIN_SCL, PIN_SDA, canal = 0)
# sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
lora = UART(1, baudrate=4800, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
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
def criar_pacote():
    pass


# Função para lidar com os pacotes recebidos via LoRa
TAMANHO_PACOTE_LEITURA = 16
def get_lora(packet: List[bytes], rssi_on:bool = True):
    if rssi_on:
        lora_msg = packet[:-1]
        rssi = -(256-packet[-1])
    else:
        lora_msg = packet
        rssi = None
    
    # Verificação do checksum (CRC-16)
    lora_msg = verificar_crc16(lora_msg)
    
    
    if lora_msg and lora_msg[1] == ESP_ADDR['sala']:
    # Implementar respostas para as mensagens
        # requisição de horário
        if len(lora_msg) == 4 and lora_msg[2] == MSG_TYPE['clock_get']:
            to_esp = 'teste' if lora_msg[0] == ESP_ADDR['teste'] else 'controle' # Direciona a mensagem como resposta a quem enviou apenas
            now = clock.get_time()
            set_time = [ESP_ADDR['sala'], ESP_ADDR[to_esp], MSG_TYPE['clock_set'], now['ano']-2000, now['mes'], now['dia'], now['hora'], now['minuto'], now['segundo']]
            for byte in calcular_crc16(set_time)[0:2]:
                set_time.append(byte)
            print(set_time)
            lora.write(bytes(set_time))
        # dados dos end_points
        elif len(lora_msg) == TAMANHO_PACOTE_LEITURA and lora_msg[2] == MSG_TYPE['leitura']:
            pass
 

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
# dte = clock.get_time()
# logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}_{dte["hora"]}_{dte["minuto"]}_{dte["segundo"]}.csv'
# sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,adc_int,adc_dec\n', 'w')


# Loop
while True:
    if lora.any(): # Verificar novos pacote LoRa
        sleep_ms(100)
        packet = [b for b in lora.read()]
        get_lora(packet)
    mqtt_client.chk_msg() # Verificar novas mensagens MQTT
    