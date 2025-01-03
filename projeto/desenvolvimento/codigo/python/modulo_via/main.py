from MyDht import MyDht
from Gyroscope import Gyroscope
from Clock import Clock

dht = MyDht()
gyro = Gyroscope()
clock = Clock()

clock.set_time(25, 1, 3, 18, 23, 40)


def make_pack():
    dte = clock.get_time()
    p = {'temperatura': dht.readings[0], 'umidade': dht.readings[1],
              'gX': gyro.readings[0], 'gY': gyro.readings[1], 'gZ': gyro.readings[2],
              'ano': dte['ano'] - 2000, 'mes': dte['mes'], 'dia': dte['dia'],
              'hora': dte['hora'], 'minuto': dte['minuto'], 'segundo': dte['segundo']
         }
    return p

while True:
    dht.update()
    gyro.update()
    
    if not dht.update_enable and not gyro.update_enable:
        pacote = make_pack()
        print(pacote)
        dht.update_enable = True
        gyro.update_enable = True