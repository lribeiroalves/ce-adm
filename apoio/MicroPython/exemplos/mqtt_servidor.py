from umqtt.simple import MQTTClient
import network
from time import sleep
import ujson
from machine import Pin, ADC

# Configurar ADC
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

# Configurar LED
led = Pin(23, Pin.OUT)
led.value(0)

# Endereço do broker MQTT
BROKER_ADRR = '192.168.0.10'
TOPIC = 'test/server/read'


# Conectar o WiFi
def conectar_wifi(ssid: str, password: str):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    
    for c in range(11):
        if not wifi.isconnected():
            if c == 10:
                print('Não foi possível conectar.')
                while True:
                    pass
            print('Aguardando conexão...')
            sleep(1)
        else:
            print(f'Conectado ao WiFi: {wifi.ifconfig()}')
            break


# Conectar broker MQTT e assinar a um topico
def conectar_mqtt(broker_addr):
    client = MQTTClient('esp32', broker_addr)
    try:
        client.connect()
        print('Conectado ao Broker MQTT')
    except OSError as e:
        print(f'Erro ao conectar ao Broker MQTT: {e}')
        while True:
            pass
    return client


if __name__ == '__main__':
    conectar_wifi('2GNETVIRTUA_AP1811', '194267140')
    client = conectar_mqtt(BROKER_ADRR)
    
    counter = 0
    c = 0
    while True:
        led.value(not led.value())
        pacote = {
            'pacote': counter,
            'name': 'esp32',
            'led': led.value(),
            'adc': adc.read()
        }
        counter+=1
        c+=1
        msg = ujson.dumps(pacote)
        client.publish(TOPIC, msg)
        print(pacote)
        if c >= 50:
            c = 0
            sleep(10)
        else:
            sleep(0.1)
    
