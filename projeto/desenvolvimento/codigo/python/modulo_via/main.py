from MyDht import MyDht
from Gyroscope import Gyroscope

dht = MyDht()
gyro = Gyroscope()

while True:
    dht.update()
    gyro.update()
    
    if not dht.update_enable and not gyro.update_enable:
        pacote = [dht.readings[0] / 5, dht.readings[1], gyro.readings[0], gyro.readings[1], gyro.readings[2]]
        print(pacote)
        dht.update_enable = True
        gyro.update_enable = True