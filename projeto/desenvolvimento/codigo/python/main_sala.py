from machine import UART, Pin
from time import sleep_ms, ticks_ms
import ujson

from CRC16 import *
from WIFI import WIFI
from MQTT import MQTT
from CardSD import CardSD
from ADC import ADC
from Clock import Clock
from ResetPin import ResetPin
from funcoes_ajuda import atualizar_clock, get_lora, get_mqtt, criar_pacote

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
BROKER_ADRR = '10.156.95.206'
BROKER_PORT = 1883
MQTT_USER = 'esp32'
MQTT_PSWD = 'esp32'


def main(addr):
    # Criar instancias
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

    # Conclusão das instâncias
    sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
    adc0 = ADC(PIN_SCL, PIN_SDA, canal = 0, get_pino = True, sd=sd, clock=clock)
    adc1 = ADC(PIN_SCL, PIN_SDA, canal = 1, get_pino = True, sd=sd, clock=clock)
    adc2 = ADC(PIN_SCL, PIN_SDA, canal = 2, get_pino = True, sd=sd, clock=clock)
    adc3 = ADC(PIN_SCL, PIN_SDA, canal = 3, get_pino = True, sd=sd, clock=clock)
    occ_sensor = ResetPin(PIN_SENSOR_OCC, sd=sd, clock=clock)
    occ_controle = ResetPin(PIN_CONTROLE_OCC, sd=sd, clock=clock)
    reset_sensor = ResetPin(PIN_SENSOR_RESET, sd=sd, clock=clock)
    reset_controle = ResetPin(PIN_CONTROLE_RESET, sd=sd, clock=clock)


    # Criação do arquivo data_logger.txt que armazenará as informações de leituras
    time = clock.get_time()
    logger_path = f'/sd/data_logger/readings/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
    sd.write_data(logger_path, 'day,month,year,hour,minute,second,sys1_t_int,sys1_t_dec,sys1_c_int,sys1_c_dec,sys2_t_int,sys2_t_dec,sys2_c_int,sys2_c_dec,occ_t,occ_c,reset_t,reset_c\n', 'w')
    
    tempo_ini = 0
    tempo_fim = 0
    # Loop
    while True:
        if lora.any(): # Verificar novos pacote LoRa
            sleep_ms(10) #10ms garante pacotes de até 144 Bytes (4 pacotes completos)
            buffer = [b for b in lora.read()]
            get_lora(buffer, lora=lora, mqtt=mqtt_client, clock=clock)
        mqtt_client.chk_msg() # Verificar novas mensagens MQTT
        # Coletar dados de occ e reset
        adc0.update()
        adc1.update()
        adc2.update()
        adc3.update()
        occ_sensor.update()
        occ_controle.update()
        reset_sensor.update()
        reset_controle.update()

        # Verificar se os dados foram coletados, armazenar localmente, criar pacote e enviar ao servidor via MQTT
        if [adc0.update_enable, adc1.update_enable, adc2.update_enable, adc3.update_enable, occ_sensor.update_enable, occ_controle.update_enable, reset_sensor.update_enable, reset_controle.update_enable] == [False] * 8:
            pacote = criar_pacote('sala', clock, adc0, adc1, adc2, adc3, occ_pin0=occ_sensor, occ_pin1=occ_controle, reset_pin0=reset_sensor, reset_pin1=reset_controle)
            # Salvar no SD
            sd.write_data(logger_path,pacote['csv'],'a')
            # Enviar via MQTT
            tempo_fim = ticks_ms()
            mqtt_client.publicar_mensagem('adm/esp_sala/server/readings_sala', pacote['mqtt_msg'])
            print(f'Tempo: {(tempo_fim - tempo_ini) / 1000:.2f} segundos')
            tempo_ini = ticks_ms()
            
            # Habilitar novas leituras
            adc0.update_enable = True
            adc1.update_enable = True
            adc2.update_enable = True
            adc3.update_enable = True
            occ_sensor.update_enable = True
            occ_controle.update_enable = True
            reset_sensor.update_enable = True
            reset_controle.update_enable = True
