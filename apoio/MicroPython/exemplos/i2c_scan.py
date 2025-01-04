from machine import Pin, SoftI2C
import time
from ssd1306 import SSD1306_I2C

# Configuração do I2C
i2c = SoftI2C(scl=Pin(15), sda=Pin(4))

pin = Pin(16, Pin.OUT)
pin.value(0) #set GPIO16 low to reset OLED
pin.value(1) #while OLED is running, must set GPIO16 in high

# Escanear dispositivos I2C no barramento
dispositivos = i2c.scan()

if dispositivos:
    print("Dispositivos I2C encontrados:", [hex(d) for d in dispositivos])
else:
    print("Nenhum dispositivo I2C encontrado")

