from machine import Pin, SPI
import time
from sx127x import SX127x

# Configuração do SPI
spi = SPI(1, baudrate=5000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

# Configuração dos pinos CS, RST e DIO
cs = Pin(5, Pin.OUT)
rst = Pin(14, Pin.OUT)
dio0 = Pin(26, Pin.IN)

# Inicialização do módulo LoRa
lora = SX127x(spi, cs, rst, dio0)

# Configuração do módulo
lora.set_mode(SX127x.SLEEP_MODE)
lora.set_pa_config(output_power=15)
lora.set_freq(915000000)
lora.set_spreading_factor(7)
lora.set_bandwidth(125000)
lora.set_tx_power(20)
lora.set_crc_on(True)
lora.set_sync_word(0x12)
lora.set_modulation_mode(SX127x.LORA)

# Função para enviar dados
def enviar_dados(msg):
    lora.set_mode(SX127x.STDBY_MODE)
    lora.write_payload([ord(char) for char in msg])
    lora.set_mode(SX127x.TX_MODE)
    time.sleep(1)  # Esperar o envio

# Função para receber dados
def receber_dados():
    lora.set_mode(SX127x.RXCONTINUOUS_MODE)
    while True:
        if lora.irq_received():
            lora.set_mode(SX127x.STDBY_MODE)
            payload = lora.read_payload()
            return bytes(payload).decode('utf-8')

# Exemplo de uso
enviar_dados("Olá, LoRa!")
print("Dados enviados.")

# Aguarda e recebe dados
dados_recebidos = receber_dados()
print("Dados recebidos:", dados_recebidos)
