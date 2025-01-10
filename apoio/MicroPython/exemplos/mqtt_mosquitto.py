from umqtt.simple import MQTTClient
import network
from time import sleep
from machine import Pin, ADC

# Função para conectar ao WiFi
def conectar_wifi(ssid, senha):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, senha)
    
    while not wlan.isconnected():
        print('aguardando conexão...')
        sleep(0.5)
    
    print('Conectado ao WiFi:', wlan.ifconfig())

# Substitua 'SSID' e 'SENHA' pelas credenciais do seu WiFi
conectar_wifi('Galaxy S22EAA7', 'tbtt6469')

# Endereço do broker MQTT
broker_address = '192.168.204.161'  # Substitua pelo endereço IP do seu broker

# Função para tratar mensagens recebidas
def tratar_mensagem(topic, msg):
    print(f'Tópico: {topic.decode("utf-8")}, Mensagem: {msg.decode("utf-8")}')

# Configuração do cliente MQTT
cliente = MQTTClient('esp32', broker_address)

# Definir a função de callback
cliente.set_callback(tratar_mensagem)

# Tente conectar ao broker MQTT
try:
    cliente.connect()
    print('Conectado ao broker MQTT')
except OSError as e:
    print(f'Erro ao conectar ao broker MQTT: {e}')

adc = ADC(Pin(34))

while True:
    leitura = adc.read()
    cliente.publish('test/topic', f'{leitura}')
    sleep(0.1)