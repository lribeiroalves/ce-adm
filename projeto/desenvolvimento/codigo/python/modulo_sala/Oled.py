from machine import Pin, SoftI2C
import time
from ssd1306 import SSD1306_I2C as OLED


class Oled:
    """ Implementação facilitada do Display OLED da Placa Esp32 SX1276 """
    
    def __init__(self, scl: int = 15, sda: int = 4, rst: int = 16):
        self.__i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda))
        self.__rst_pin = Pin(rst, Pin.OUT) # Reset via software no display
        self.__rst_pin.value(0)
        self.__rst_pin.value(1)
        try:
            self.__oled = OLED(128, 64, self.__i2c)
        except:
            raise RuntimeError('Não foi possível se comunicar com o display OLED')
    
    
    def limpar(self):
        """ Limpar o conteúdo da tela do display """
        self.__oled.fill(0)
        self.__oled.show()
    
    
    def escrever(self, texto: str, linha: int = 0, coluna: int = 0):
        """ Escrever uma mensagem na tela do display """
        self.__oled.text(texto, coluna, linha)
        self.__oled.show()


if __name__ == '__main__':
    import time
    
    oled = Oled()
    
    while True:
        oled.escrever('Lucas Ribeiro')
        time.sleep(5)
        oled.limpar()
        time.sleep(1)
        oled.escrever('32384-9',32, 0)
        time.sleep(5)
        oled.limpar()
        time.sleep(1)
        