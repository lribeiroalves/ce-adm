from machine import Pin, SPI
from sdcard import SDCard
import os


class CardSD:
    """ Classe para utilização do barramento SPI para comunicação com cartão SD """
    
    def __init__(self, pin_cs: int = 5, pin_sck: int = 18, pin_mosi: int = 23, pin_miso: int = 19):
        self.__spi = SPI(1,baudrate=1000000, phase=0, polarity=0, sck=Pin(pin_sck), mosi=Pin(pin_mosi), miso=Pin(pin_miso))
        self.__sd = SDCard(self.__spi, Pin(pin_cs))
        os.mount(self.__sd, '/sd')
    
    
    def __dir(self, path):
        caminho = '/'.join(path.split('/')[:-1])
        arquivo = path.split('/')[-1]
        
        try:
            diretorio = os.listdir(caminho)
        except OSError:
            raise ValueError('Directory not Found')
        
        return diretorio, arquivo
        
    
    def list_files(self, path):
        """ List all files and directories on the path """
        try:
            for item in os.listdir(path):
                full_path = path + '/' + item
                if os.stat(full_path)[0] & 0x4000:  # Verifica se é um diretório
                    print(f'DIR: {full_path}')
                    self.list_files(full_path)  # Lista arquivos no diretório
                else:
                    print(f'FILE: {full_path}')
        except OSError:
            raise ValueError('Path Fot Found.')
    
    
    def write_data(self, path: str, data: str, mode: str = 'w'):
        """ Escrever no cartão SD - 'mode' pode assumir 'A' ou 'W' para concatenar ao arquivo ou limpar e escrever """
        if mode.lower() in ['a', 'w']:
            # Criar diretório se não existir
            dir_path = '/'.join(path.split('/')[:-1])
            try:
                os.listdir(dir_path)
            except OSError:
                os.mkdir(dir_path)
            # Escrever dados no arquivo
            with open(path, mode.lower()) as file:
                file.write(data)
        else:
            raise ValueError('mode must be "a" or "w"')
    
    
    def read_data(self, full_path):
        """ Tenta ler os dados de um arquivo e retorna um ValueError se nao encontrar o arquivo. """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            with open(full_path, 'r') as file:
                print(file.read())
        else:
            raise ValueError('File Not Found.')
    
    
    def clear_file(self, full_path):
        """ Limpa os dados de um arquivo """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            self.write_data(full_path, '', 'w')
        else:
            raise ValueError('File Not Found.')
    
    
    def delete_from_card(self, full_path):
        """ Delete um arquivo ou diretorio do Cartão SD """
        diretorio, arquivo = self.__dir(full_path)
        if arquivo in diretorio:
            if os.stat(full_path)[0] & 0X4000:
                for file in os.listdir(full_path):
                    file_path = full_path + '/' + file
                    if os.stat(full_path)[0] & 0X4000:
                        self.delete_from_card(file_path)
                    else:
                        os.remove(file_path)
                os.rmdir(full_path)
            else:
                os.remove(full_path)
        else:
            raise ValueError('File Not Found')


if __name__ == '__main__':
    sd = CardSD()
    sd.list_files('/sd')
    sd.read_data('/sd/data_logger.txt')
    