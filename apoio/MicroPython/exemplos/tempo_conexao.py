from WIFI import WIFI
from MQTT import MQTT

import ujson
import time
from random import randint

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


wifi = WIFI(ssid=WIFI_SSID, pswd=WIFI_PSWD)
mqtt = MQTT(addr=BROKER_ADRR, user=MQTT_USER, pswd=MQTT_PSWD, port=BROKER_PORT)

wifi.conectar()
mqtt.conectar()

counter = 0

# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}

# Bytes de contagem dos pacotes MQTT
num_pacote = {
    ESP_ADDR['teste']: [0x00, 0x00, 0x00],
    ESP_ADDR['controle']: [0x00, 0x00, 0x00],
    ESP_ADDR['sala']: [0x00, 0x00, 0x00]
}


def contagem_pacotes(addr:bytes) -> list[bytes, bytes, bytes]:
    """ Função para fazer a contagem dos pacotes enviados via MQTT """
    if num_pacote[addr][2] < 0xFF:
        num_pacote[addr][2] += 1
    else:
        num_pacote[addr][2] = 0
        if num_pacote[addr][1] < 0xFF:
            num_pacote[addr][1] += 1
        else:
            num_pacote[addr][1] = 0
            if num_pacote[addr][0] < 0xFF:
                num_pacote[addr][0] += 1
            else:
                num_pacote[addr][0] = 0
    
    return num_pacote[addr]


while True:
    if not wifi.isconnected:
        print('Wifi caiu')
        wifi.conectar()
        
    
    if counter % 2 == 0:
        addr = 'teste'
    else:
        addr = 'controle'
        
    cp = contagem_pacotes(ESP_ADDR[addr])
    dic_via = {
        'num_pacote_0': cp[0],
        'num_pacote_1': cp[1],
        'num_pacote_2': cp[2],
        'ad_sen_int': randint(12, 28), 'ad_sen_dec': randint(0, 99),
        'ad_bat_int': randint(9, 11), 'ad_bat_dec': randint(0, 99),
        'temp': randint(20, 250), 'umid': randint(70, 80),
        'gX': randint(0, 36), 'gY': randint(0, 36), 'gZ': randint(0, 36)
    }
    mqtt.publicar_mensagem(f'adm/esp_sala/server/readings_{addr}', dic_via)
    
    cp = contagem_pacotes(ESP_ADDR['sala'])
    dic_sala = {
        'num_pacote_0': cp[0],
        'num_pacote_1': cp[1],
        'num_pacote_2': cp[2],
        'sys1_t_int': randint(12, 28), 'sys1_t_dec': randint(12, 28),
        'sys2_t_int': randint(12, 28), 'sys2_t_dec': randint(12, 28),
        'sys1_c_int': randint(12, 28), 'sys1_c_dec': randint(12, 28),
        'sys2_c_int': randint(12, 28), 'sys2_c_dec': randint(12, 28),
        'occ_t': randint(12, 28), 'occ_c': randint(12, 28),
        'reset_t': randint(12, 28), 'reset_c': randint(12, 28)
    }
    mqtt.publicar_mensagem('adm/esp_sala/server/readings_sala', dic_sala)
    
    counter += 1

    time.sleep(0.3)

