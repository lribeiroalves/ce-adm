from umqtt.simple import MQTTClient
import network
from time import sleep
from machine import Pin, ADC
import sys

# É necessário abrir a porta 1883 no Firewall da máquina para estabelecer a conexão
# Para isso, basta inserir o seguinte comando no prompt com direitos de administrador
# netsh advfirewall firewall add rule name="Mosquitto" dir=in action=allow protocol=TCP localport=1883


SSID = 'Galaxy S22EAA7'
WIFI_PASS = 'tbtt6469'
MQTT_USER = 'esp32'
MQTT_PASS = 'esp32'


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
conectar_wifi(SSID, WIFI_PASS)

# Endereço do broker MQTT
broker_address = '192.168.154.161'  # Substitua pelo endereço IP do seu broker

# Função para tratar mensagens recebidas
def tratar_mensagem(topic, msg):
    print(f'Tópico: {topic.decode("utf-8")}, Mensagem: {msg.decode("utf-8")}')

# Configuração do cliente MQTT
cliente = MQTTClient('esp32', broker_address, 1883, MQTT_USER, MQTT_PASS)

# Definir a função de callback
cliente.set_callback(tratar_mensagem)

# Tente conectar ao broker MQTT
try:
    cliente.connect()
    print('Conectado ao broker MQTT')
except OSError as e:
    print(f'Erro ao conectar ao broker MQTT: {e}')
    sys.exit(1)

adc = ADC(Pin(34))

while True:
    leitura = adc.read()
    cliente.publish('test/topic', f'{leitura}')
    sleep(0.1)