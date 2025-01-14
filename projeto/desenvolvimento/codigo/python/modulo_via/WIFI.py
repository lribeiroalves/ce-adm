import network
from time import sleep


class WIFI:
    """
        Classe para implementação da conexão com rede Wifi
        
        on_fail_conn: False (Default) -> Desiste após falha de conexão (20 tentativas de conectar)
        on_fail_conn: True -> Continua tentando conectar indefinidamente
        
    """
    
    def __init__(self, ssid: str, pswd: str, on_fail_conn: bool = False):
        self.__ssid = ssid
        self.__passwd = pswd
        self.__on_fail_conn = on_fail_conn
        self.__wifi = network.WLAN(network.STA_IF)
    
    def conectar(self):
        """ Ligar a interface Wifi e conectar a uma rede """
        if not self.__wifi.active():
            self.__wifi.active(True)
        self.__wifi.connect(self.__ssid, self.__passwd)
        
        conn_counter = 21 if not self.__on_fail_conn else 0
        while True:
            if not self.__wifi.isconnected():
                conn_counter -= 1
                if conn_counter == 0:
                    print('Não foi possível conectar.')
                    while True:
                        pass
                print(f'Aguardando conexão...')
                sleep(0.5)
            else:
                print(f'Conectado ao WiFi: {self.__wifi.ifconfig()}')
                break
    
    def desconectar(self):
        """ Desconectar e desligar a interface WiFi """
        if self.__wifi.isconnected():
            self.__wifi.disconnect()
            print('WiFi desconectado...')
        if self.__wifi.active():
            self.__wifi.active(False)
    

if __name__ == '__main__':
    wifi = WIFI('ssid', 'passwd')
    wifi.desconectar()
    wifi.conectar()
    wifi.desconectar()

