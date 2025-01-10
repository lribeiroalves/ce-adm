from umqtt.simple import MQTTClient
import network
from time import sleep

# Endereço do broker MQTT
BROKER_ADRR = '192.168.0.10'


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


# Tratar mensagens recebidas por MQTT
def tratar_msg(topic, msg):
    print(f'Tópico: {topic}, Mensagem: {msg}')
    print(f'Tópico: {topic.decode("utf-8")}, Mensagem: {msg.decode("utf-8")}')


# Conectar broker MQTT e assinar a um topico
def conectar_mqtt(broker_addr, sub_topic):
    client = MQTTClient('esp32', broker_addr)
    client.set_callback(tratar_msg)
    try:
        client.connect()
        print('Conectado ao Broker MQTT')
    except OSError as e:
        print(f'Erro ao conectar ao Broker MQTT: {e}')
        while True:
            pass
    try:
        client.subscribe(sub_topic)
        print(f'Assinado ao tópico: {sub_topic}')
    except OSError as e:
        print(f'Erro ao assinar o tópico {sub_topic}: {e}')
        while True:
            pass
    
    return client


if __name__ == '__main__':
    conectar_wifi('2GNETVIRTUA_AP1811', '194267140')
    client = conectar_mqtt(BROKER_ADRR, 'test/esp32/topic')
    
    print('Aguardando mensagens...')
    while True:
        client.check_msg()
        sleep(0.5)
