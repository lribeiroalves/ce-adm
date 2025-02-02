""" Arquivo de funções auxiliares para os códigos main """

from CRC16 import *
from MQTT import MQTT
from Clock import Clock
from MyDht import MyDht
from Gyroscope import Gyroscope
from ADC import ADC

from machine import UART, Pin
from time import sleep_ms
import ujson

# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}

# Características esperadas das mensagens LoRa
TAMANHO_PACOTE_LEITURA = 18
TAMANHO_PACOTE_REQUIS_HORA = 4
TAMANHO_PACOTE_ENVIO_HORA = 9
FLAG_FINAL_MENSAGEM = [0xFF] * 3

# Tópicos para publicações MQTT
topicos_mqtt_pub = ['adm/esp_sala/server/reading',
                    'adm/esp_sala/server/req_time']


# Criação dos pacotes de dados das leituras realizadas por cada sensor
def criar_pacote(esp:str, clock:Clock = None, adc0:ADC = None, adc1:ADC = None, adc2:ADC = None, adc3:ADC = None, dht:MyDht = None, gyro:Gyroscope = None, occ_pin0:Pin = None, occ_pin1:Pin = None, reset_pin0:Pin = None, reset_pin1:Pin = None):
    if esp == 'sala':
        # Aguardando definição do hardware
        return {'raw': [], 'csv': []}

    elif esp in ['teste', 'controle']:
        time = clock.get_time()
        # dados brutos
        raw = {
            'addr': ESP_ADDR[esp],
            'msg_type': MSG_TYPE['leitura'],
            'ad_sen_int': adc0.readings[0], 'ad_sen_dec': adc0.readings[1],
            'ad_bat_int': adc1.readings[0], 'ad_bat_dec': adc1.readings[1],
            'temp': dht.readings[0], 'umid': dht.readings[1],
            'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
            'year': time['ano'] - 2000, 'month': time['mes'], 'day': time['dia'],
            'hour': time['hora'], 'minute': time['minuto'], 'second': time['segundo']
        }
        # mensagem pronta para o datalog
        csv = f"{raw['day']},{raw['month']},{raw['year']},{raw['hour']},{raw['minute']},{raw['second']},{raw['umid']},{raw['temp']},{raw['gX']},{raw['gY']},{raw['gZ']},{raw['ad_sen_int']},{raw['ad_sen_dec']},{raw['ad_bat_int']},{raw['ad_bat_dec']}\n"
        # mensagem pronta para transmissão LoRa
        lora_msg = [raw['addr'], ESP_ADDR['sala'], raw['msg_type'], raw['day'], raw['month'], raw['year'], raw['hour'], raw['minute'], raw['second'], raw['umid'], raw['temp'], raw['gX'], raw['gY'], raw['gZ'], raw['ad_sen_int'], raw['ad_sen_dec'], raw['ad_bat_int'], raw['ad_bat_dec']]
        lora_msg += FLAG_FINAL_MENSAGEM + [len(lora_msg)] # Adiciona uma flag de final de mensagem
        checksum = calcular_crc16(lora_msg)[0:2]
        for byte in checksum:
            lora_msg.append(byte)
        return {'raw': raw, 'csv': csv, 'lora_msg':lora_msg}


# Funçao para lidar com mensagens recebidas pelos tópicos MQTT
def get_mqtt(topic_coded:bytes, msg_coded:bytes, clock:Clock = None):
    topic, msg = topic_coded.decode(), msg_coded.decode()

    sala_topics = 'adm/server/esp_sala'
    teste_topics = 'adm/server/esp_teste'
    controle_topics = 'adm/server/esp_controle'

    # mensagens direcionadas para o esp da sala
    if topic == f'{sala_topics}/clock':
        new_time = ujson.loads(msg)
        try:
            clock.set_time(ano=new_time['year'], mes=new_time['month'], dia=new_time['day'], hora=new_time['hour'], minuto=new_time['minute'], segundo=new_time['second'])
        except ValueError as e:
            print('Valor recebido não é uma Data/Hora válida. Solicitando novamente')

    # mensagens direcionadas para o esp do sensor em teste
    elif topic == f'{teste_topics}/clock':
        pass

    # mensagens direcionadas para o esp do sensor de controle
    elif topic == f'{controle_topics}/clock':
        pass


# Função para criar o dicionário dos dados de leituras dos end-points para enviar o broker MQTT
def convert_to_dict(buffer:list[bytes]):
    dic = {
        'addr': buffer[0],
        'msg_type': buffer[2],
        'ad_sen_int': buffer[14], 'ad_sen_dec': buffer[15],
        'ad_bat_int': buffer[16], 'ad_bat_dec': buffer[17],
        'temp': buffer[10], 'umid': buffer[9],
        'gX': buffer[11], 'gY': buffer[12], 'gZ': buffer[13],
        'year': buffer[5], 'month': buffer[4], 'day': buffer[3],
        'hour': buffer[6], 'minute': buffer[7], 'second': buffer[8]
    }
    return dic


# Função para separar o buffer recebido via LoRa em mensagens separadas 
def extrair_pacotes(buffer:list[bytes]):
    mensagens_separadas = []
    final = FLAG_FINAL_MENSAGEM
    final_len = len(final)
    buffer_len = len(buffer)
    
    if buffer_len >= final_len + 5:
        for i in range(buffer_len - final_len + 1):
            if buffer[i:i + final_len] == final:
                mensagem = buffer[i - buffer[i + final_len]: i + final_len + 4]
                mensagens_separadas.append(mensagem)
    
    return mensagens_separadas


# Função para lidar com os pacotes recebidos via LoRa
def get_lora(buffer: list[bytes], lora:UART = None, mqtt:MQTT = None, clock:Clock = None):
    pacotes = extrair_pacotes(buffer)
    
    for pacote in pacotes:
        # Separar rssi da mensagem
        lora_msg = pacote[:-1]
        rssi = -(256-pacote[-1])
        
        # Verificar e retirar o checksum (CRC-16) da mensagem
        lora_msg = verificar_crc16(lora_msg)
        
        # Testar a verificação do checksum
        if lora_msg:
            # remover sinalização de final de mensagem
            lora_msg = lora_msg[:-4]
            
            # Verificação do destinatário da mensagem no header
            if lora_msg[1] == ESP_ADDR['sala']:
                # requisição de horário
                if len(lora_msg) == 4 and lora_msg[2] == MSG_TYPE['clock_get']:
                    to_esp = 'teste' if lora_msg[0] == ESP_ADDR['teste'] else 'controle' # Direciona a resposta da mensagem a quem fez a requisição
                    now = clock.get_time()
                    time_set_msg = [ESP_ADDR['sala'], ESP_ADDR[to_esp], MSG_TYPE['clock_set'], now['ano']-2000, now['mes'], now['dia'], now['hora'], now['minuto'], now['segundo']]
                    for byte in calcular_crc16(time_set_msg)[0:2]:
                        time_set_msg.append(byte)
                    lora.write(bytes(time_set_msg))
                    
                # dados das leituras dos end_points
                elif len(lora_msg) == TAMANHO_PACOTE_LEITURA and lora_msg[2] == MSG_TYPE['leitura']:
                    readings_to_server = convert_to_dict(lora_msg)
                    mqtt.publicar_mensagem(topicos_mqtt_pub[0], readings_to_server)
                    
            elif lora_msg[1] in [ESP_ADDR['sensor'], ESP_ADDR['controle']]:
                # Receber definição de horário do esp da sala
                if len(lora_msg) == TAMANHO_PACOTE_ENVIO_HORA and lora_msg[2] == MSG_TYPE['clock_set']:
                    try:
                        clock.set_time(ano = lora_msg[3], mes = lora_msg[4], dia = lora_msg[5], hora = lora_msg[6], minuto = lora_msg[7], segundo = lora_msg[8])
                    except ValueError as e:
                        print('Valor recebido não é uma Data/Hora válida. Solicitando novamente')                    


# Requisição de Horário (Para o programa até setar o clock interno)
def atualizar_clock(esp:str, lora:UART = None, mqtt:MQTT = None, clock:Clock = None):
    if esp == 'sala':
        time_req_msg = {'addr': ESP_ADDR['sala'], 'msg_type': MSG_TYPE['clock_get'], 'check': 0x42}
        while not clock.is_set:
            print('Requisitando horário ao servidor')
            mqtt.publicar_mensagem(topicos_mqtt_pub[1], time_req_msg)
            for _ in range(1000):
                mqtt.chk_msg()
                if clock.is_set:
                    time = clock.get_time()
                    print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
                    break
                sleep_ms(5)
    elif esp == 'via':
        # Construção da mensagem de requisição de hora
        time_req_msg = [ESP_ADDR['teste'], ESP_ADDR['sala'], MSG_TYPE['clock_get'], 0x42]
        time_req_msg += FLAG_FINAL_MENSAGEM + [len(time_req_msg)]
        checksum = calcular_crc16(time_req_msg)[0:2] # Calculo do Checksum
        for byte in checksum:
            time_req_msg.append(byte)
        # Enviar a mensagem construída e agurdar resposta a cada 3s
        while not clock.is_set:
            print('Requisitando horário ao Gateway')
            lora.write(bytes(time_req_msg))
            sleep_ms(3000)
            if lora.any():
                sleep_ms(10)
                buffer = [b for b in lora.read()]
                get_lora(buffer, lora, mqtt, clock)
        time = clock.get_time()
        print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
