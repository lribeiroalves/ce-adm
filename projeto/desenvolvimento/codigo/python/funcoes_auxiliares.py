""" Arquivo de funções auxiliares para os códigos main """

from CRC16 import *
from MQTT import MQTT
from Clock import Clock
from machine import UART

# Endereçamento e tipos de mensagem
ESP_ADDR = {'teste': 0x01, 'controle': 0x02, 'sala': 0x03}
MSG_TYPE = {'leitura': 0x10, 'clock_get': 0x20, 'clock_set': 0x30}

# Características esperadas das mensagens recebidas via LoRa
TAMANHO_PACOTE_LEITURA = 18
TAMANHO_PACOTE_REQUIS_HORA = 4
TAMANHO_PACOTE_ENVIO_HORA = 9


# Função para separar o buffer recebido em mensagens separadas 
def extrair_pacotes(buffer:list[bytes]):
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
                    to_esp = 'teste' if lora_msg[0] == ESP_ADDR['teste'] else 'controle' # Direciona a resposta da mensagem a quem requisitou
                    now = clock.get_time()
                    msg_resposta = [ESP_ADDR['sala'], ESP_ADDR[to_esp], MSG_TYPE['clock_set'], now['ano']-2000, now['mes'], now['dia'], now['hora'], now['minuto'], now['segundo']]
                    for byte in calcular_crc16(msg_resposta)[0:2]:
                        msg_resposta.append(byte)
                    lora.write(bytes(msg_resposta))
                    
                # dados das leituras dos end_points
                elif len(lora_msg) == TAMANHO_PACOTE_LEITURA and lora_msg[2] == MSG_TYPE['leitura']:
                    readings_to_server = criar_pacote(lora_msg, 'via')
                    mqtt.publicar_mensagem(topico_pub[0], readings_to_server)
                    
            elif lora_msg[1] in [ESP_ADDR['sensor'], ESP_ADDR['controle']]:
                # Receber definição de horário do esp da sala
                if len(lora_msg) == TAMANHO_PACOTE_ENVIO_HORA and lora_msg[2] == MSG_TYPE['clock_set']:
                    try:
                        clock.set_time(ano = lora_msg[3], mes = lora_msg[4], dia = lora_msg[5], hora = lora_msg[6], minuto = lora_msg[7], segundo = lora_msg[8])
                        time = clock.get_time()
                        print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
                    except ValueError as e:
                        print('Valor recebido não é uma Data/Hora válida. Solicitando novamente')
                    


# Requisição de Horário (Para o programa até setar o clock interno)
def atualizar_clock(esp:str, clock:Clock = None, mqtt:MQTT = None):
    if esp == 'sala':
        req_time = {'addr': ESP_ADDR['sala'], 'msg_type': MSG_TYPE['clock_get'], 'check': 0x42}
        while not clock.is_set:]
            print('Requisitando horário ao servidor')
            mqtt_client.publicar_mensagem(topico_pub[1], req_time)
            for _ in range(1000):
                mqtt_client.chk_msg()
                if clock.is_set:
                    time = clock.get_time()
                    print(f'Informação de horário recebida: {time["dia"]:02}/{time["mes"]:02}/{time["ano"]:04} - {time["hora"]:02}:{time["minuto"]:02}:{time["segundo"]:02}')
                    break
                sleep_ms(5)
#             if clock.is_set:
#                 clock.set_time(ano=new_time['year'], mes=new_time['month'], dia=new_time['day'], hora=new_time['hour'], minuto=new_time['minute'], segundo=new_time['second'])
            
    elif esp == 'via':
        pass