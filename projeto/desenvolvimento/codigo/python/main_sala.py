from machine import UART, freq
from time import sleep_ms, ticks_ms
from classes_ajuda import *
from funcoes_ajuda import *

# Definir a frequencia de trabalho do ESP32
freq(240000000)

# PINOUT
PIN_LORA_RX = 2
PIN_LORA_TX = 4
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_SCL = 22
PIN_SDA = 21
PIN_SENSOR_RESET = 25
PIN_SENSOR_OCC = 26
PIN_CONTROLE_RESET = 27
PIN_CONTROLE_OCC = 33

# Endereços de Rede e Broker MQTT
WIFI_SSID = 'SCA_Instrumentos'
# WIFI_SSID = 'Galaxy S22EAA7'
# WIFI_SSID = 'ADM_SSV'
# WIFI_SSID = '2GNETVIRTUA_AP1811'
WIFI_PSWD = 'SCAOnline'
# WIFI_PSWD = 'tbtt6469'
# WIFI_PSWD = '244466666'
# WIFI_PSWD = '194267140'
BROKER_ADRR = '10.156.95.206'
BROKER_PORT = 1883
MQTT_USER = 'esp32'
MQTT_PSWD = 'esp32'


def main(addr):
    # Criar instancias de comunicação e de clock interno
    wifi = WIFI(ssid=WIFI_SSID, pswd=WIFI_PSWD)
    mqtt_client = MQTT(addr=BROKER_ADRR, user=MQTT_USER, pswd=MQTT_PSWD, port=BROKER_PORT)
    lora = UART(1, baudrate=115200, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
    clock = Clock()

    # Conexão com WiFi e MQTT
    wifi.conectar()
    mqtt_client.conectar()
    topico_pub = ['adm/esp_sala/server/reading', 'adm/esp_sala/server/req_time']
    topico_sub = ['adm/server/esp_sala', 'adm/server/esp_sala/clock']
    mqtt_client.assinar_topicos(topico_sub)
    mqtt_client.definir_cb(cb_func=get_mqtt, clock=clock)

    # Definição do horário inicial do RTC interno (Requisição ao servidor)
    atualizar_clock(esp='sala', lora=lora, mqtt=mqtt_client, clock=clock)

    # Criar instancias objetos de leitura e escrita
    sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
    adc0 = ADC(PIN_SCL, PIN_SDA, canal = 0, get_pino = True, sd=sd, clock=clock)
    adc1 = ADC(PIN_SCL, PIN_SDA, canal = 1, get_pino = True, sd=sd, clock=clock)
    adc2 = ADC(PIN_SCL, PIN_SDA, canal = 2, get_pino = True, sd=sd, clock=clock)
    adc3 = ADC(PIN_SCL, PIN_SDA, canal = 3, get_pino = True, sd=sd, clock=clock)
    occ_sensor = OptoPin(PIN_SENSOR_OCC, 'occ_s', sd=sd, clock=clock)
    occ_controle = OptoPin(PIN_CONTROLE_OCC, 'occ_c', sd=sd, clock=clock)
    reset_sensor = OptoPin(PIN_SENSOR_RESET, 'reset_s', sd=sd, clock=clock)
    reset_controle = OptoPin(PIN_CONTROLE_RESET, 'reset_c', sd=sd, clock=clock)


    # Criação do arquivo data_logger.txt que armazenará as informações de leituras
    time = clock.get_time()
    logger_messages_path = f'/sd/data_logger/messages/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
#     logger_readings_path = f'/sd/data_logger/readings/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
    sd.write_data(logger_messages_path, 'day,month,year,hour,minute,second,sys1_t_int,sys1_t_dec,sys1_c_int,sys1_c_dec,sys2_t_int,sys2_t_dec,sys2_c_int,sys2_c_dec,occ_t,occ_c,reset_t,reset_c\n', 'w')
#     sd.write_data(logger_readings_path, 'name,read_0,read_1,read_2,year,month,day,hour,minute,second,m_sec\n', 'w')
    
    # definição dos tempos de leituras e escritas em ms
    reading_time = 50
    previous_reading_time = 0
    writing_time = 2000
    previous_writing_time = 0

    tempo_fim = 0
    tempo_ini = 0
    
    csv_readings = '' # armazenamento das mensagens enviadas para o mqtt
    
    while True:
        # Verificar novos pacote LoRa
        if lora.any():
            sleep_ms(10) #10ms garante pacotes de até 144 Bytes (4 pacotes completos)
            buffer = [b for b in lora.read()]
            get_lora(buffer, lora=lora, mqtt=mqtt_client, clock=clock)

        # Verificar novas mensagens MQTT
        mqtt_client.chk_msg()

        # verificar se o tempo de leituras já estourou
        current_time = ticks_ms()
        
        # Realiza leituras após o reading time
        if current_time >= previous_reading_time + reading_time:
            previous_reading_time = current_time
            # realiza as leituras, e retorna um pacote com a mensagem mqtt e a string csv
            pacote = pacote_sala(adc0, adc1, adc2, adc3, occ_sensor, occ_controle, reset_sensor, reset_controle, clock)
            # apagar os registros internos de leituras individuais dos sensores para liberar memoria
            for object in [adc0, adc1, adc2, adc3, occ_sensor, occ_controle, reset_sensor, reset_controle]:
                object.clear_csv()
            # registra as leituras para serem escritas no SD posteriormente
            csv_readings += pacote['csv']
            # Enviar via MQTT
            tempo_fim = ticks_ms()
            mqtt_client.publicar_mensagem('adm/esp_sala/server/readings_sala', pacote['mqtt_msg'])
            print(f'Tempo: {(tempo_fim - tempo_ini) / 1000:.2f} segundos')
            tempo_ini = ticks_ms()
        
        # Realiza a escrita no cartão SD após o writing_time
        if current_time >= previous_writing_time + writing_time:
            previous_writing_time = current_time
            if csv_readings != '':
                # Salvar no SD
                sd.write_data(logger_messages_path, csv_readings, 'a')
            csv_readings = ''
