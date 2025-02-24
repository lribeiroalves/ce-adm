from machine import UART
from time import sleep_ms, ticks_ms

from CRC16 import *
from WIFI import WIFI
from MQTT import MQTT
from MyDht import MyDht
from Gyroscope import Gyroscope
from ADC import ADC
from Clock import Clock
from CardSD import CardSD
from funcoes_ajuda import atualizar_clock, criar_pacote, get_lora

# PINOUT
PIN_DHT = 33
PIN_SCL = 22
PIN_SDA = 21
PIN_CS = 5
PIN_SCK = 18
PIN_MOSI = 23
PIN_MISO = 19
PIN_LORA_RX = 27
PIN_LORA_TX =  26


def main(addr):
    # Criar instancias
    lora = UART(1, baudrate=115200, tx=PIN_LORA_TX, rx=PIN_LORA_RX)
    clock = Clock()
    atualizar_clock(esp='via', lora=lora, clock=clock) # Requisição inicial de horário
    sd = CardSD(PIN_CS, PIN_SCK, PIN_MOSI, PIN_MISO)
    dht = MyDht(PIN_DHT, sd=sd, clock=clock)
    gyro = Gyroscope(PIN_SCL, PIN_SDA, sd=sd, clock=clock)
    adc0 = ADC(PIN_SCL, PIN_SDA, canal=0, sd=sd, clock=clock)
    adc1 = ADC(PIN_SCL, PIN_SDA, canal=1, sd=sd, clock=clock)


    # Criação do arquivo data_logger.txt que armazenará as informações de leituras
    time = clock.get_time()
    logger_messages_path = f'/sd/data_logger/messages/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
    logger_readings_path = f'/sd/data_logger/readings/{time["ano"]}_{time["mes"]}_{time["dia"]}_{time["hora"]}_{time["minuto"]}_{time["segundo"]}.csv'
    sd.write_data(logger_messages_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,ad_sen_int,ad_sen_dec,ad_bat_int,ad_bat_dec\n', 'w')
    sd.write_data(logger_readings_path, 'name,read_0,read_1,read_2,year,month,day,hour,minute,second,m_sec\n', 'w')

    
    tempo_ini = 0
    tempo_fim = 0
    # Leitura dos sensores e tratamento dos dados
    while True:
        if lora.any():
            sleep_ms(10)
            buffer = [byte for byte in lora.read()]
            get_lora(buffer=buffer, lora=lora, clock=clock)

        dht.update()
        gyro.update()
        adc0.update()
        adc1.update()
        
        if [dht.update_enable, gyro.update_enable, adc0.update_enable, adc1.update_enable] == [0] * 4:
            # Criar o pacote com as informações
            pacote = criar_pacote(esp='teste', clock=clock, adc0=adc0, adc1=adc1, gyro=gyro, dht=dht)

            # Salvar no SD
            sd.write_data(logger_messages_path, pacote['csv'], 'a')
            readings_csv = ''
            for object in [dht, gyro, adc0, adc1]:
                readings_csv += object.csv
            sd.write_data(logger_readings_path, readings_csv, 'a')

            lora.write(bytes(pacote['lora_msg'])) # Enviar os dados via LoRa
            
            tempo_fim = ticks_ms()
            print(f'Tempo: {(tempo_fim - tempo_ini) / 1000:.2f} segundos')
            tempo_ini = ticks_ms()
            
            # Habilitar novas leituras dos sensores
            dht.update_enable = True
            gyro.update_enable = True
            adc0.update_enable = True
            adc1.update_enable = True
