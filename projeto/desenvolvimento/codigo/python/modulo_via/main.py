from MyDht import MyDht
from Gyroscope import Gyroscope
from Clock import Clock
from CardSD import CardSD

dht = MyDht()
gyro = Gyroscope()
clock = Clock()
sd = CardSD()

# Definição do horário inicial do RTC interno
clock.set_time(25, 1, 3, 18, 23, 40)

# Criação do arquivo data_logger.txt que armazenará as informações de leituras
dte = clock.get_time()
logger_path = f'/sd/data_logger/{dte["ano"]}_{dte["mes"]}_{dte["dia"]}.csv'
sd.write_data(logger_path, 'day,month,year,hour,minute,second,umid,temp,gX,gY,gZ\n', 'w')


def make_pack():
    dte = clock.get_time()
    p = {'temp': dht.readings[0], 'umid': dht.readings[1],
              'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
              'year': dte['ano'] - 2000, 'month': dte['mes'], 'day': dte['dia'],
              'hour': dte['hora'], 'minute': dte['minuto'], 'second': dte['segundo']
         }
    return p


def make_datalog(pacote):
    return f"{pacote['day']},{pacote['month']},{pacote['year']},{pacote['hour']},{pacote['minute']},{pacote['second']},{pacote['umid']},{pacote['temp']},{pacote['gX']},{pacote['gY']},{pacote['gZ']}\n"


while True:
    dht.update()
    gyro.update()
    
    if not dht.update_enable and not gyro.update_enable:
        pacote = make_pack()
        print(pacote)
        datalog = make_datalog(pacote)
        sd.write_data(logger_path, datalog, 'a')
        dht.update_enable = True
        gyro.update_enable = True
