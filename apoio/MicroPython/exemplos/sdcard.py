from machine import Pin, SPI
import sdcard
import os

spi = SPI(1,baudrate=1000000, phase=0, polarity=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
sd = sdcard.SDCard(spi, Pin(5))
os.mount(sd, '/sd')

def list_files(path):
    for item in os.listdir(path):
        full_path = path + '/' + item
        if os.stat(full_path)[0] & 0x4000:  # Verifica se é um diretório
            print(f'DIR: {full_path}')
            list_files(full_path)  # Lista arquivos no diretório
        else:
            print(f'FILE: {full_path}')


def write_data(path, data):
    # Criar diretório se não existir
    dir_path = '/'.join(path.split('/')[:-1])
    try:
        os.listdir(dir_path)
    except OSError:
        os.mkdir(dir_path)
        
    # Escrever dados no arquivo
    with open(path, 'a') as file:
        file.write(data)
        file.write('\n')


def read_file(path):
    with open(path, 'r') as file:
        print(file.read())


list_files('/sd')
print()
read_file('/sd/data_logger.txt')
print()
write_data('/sd/dir_teste/new_test.txt', 'Nova Mensagem...')
list_files('/sd')
print()
read_file('/sd/dir_teste/new_test.txt')


os.umount('/sd')