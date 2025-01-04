from machine import Pin, SoftI2C
import time
from ssd1306 import SSD1306_I2C

# Configuração do I2C
i2c = SoftI2C(scl=Pin(15), sda=Pin(4))

pin = Pin(16, Pin.OUT)
pin.value(0) #set GPIO16 low to reset OLED
pin.value(1) #while OLED is running, must set GPIO16 in high

# Inicialização do display OLED
oled = SSD1306_I2C(128, 64, i2c)

# Função para limpar o display
def limpar_display():
    oled.fill(0)
    oled.show()

# Função para escrever texto no display
def escrever_texto(texto, linha, coluna):
    oled.text(texto, coluna, linha)
    oled.show()

# Exemplo de uso
limpar_display()
escrever_texto("Ola, Mundo!", 10, 0)
# time.sleep(10)
# limpar_display()
