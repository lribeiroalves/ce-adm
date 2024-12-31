from machine import Pin, SoftI2C
from time import sleep_ms, sleep

def signed(num):
    if num & (1 << 15):
        return num - (1 << 16)
    else:
        return num

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

MPU = 0x68
PWR_MNGM = 0x6B
GYRO_ADDR = 0x43

i2c.writeto_mem(MPU, PWR_MNGM, bytes([0x00]))
sleep_ms(5)

while True:
    r = i2c.readfrom_mem(MPU, GYRO_ADDR, 6)
    
    x = r[0] << 8 | r[1]
    y = r[2] << 8 | r[3]
    z = r[4] << 8 | r[5]
    
    x, y, z = max([0, abs(signed(x)) - 100]) >> 7, max([0, abs(signed(y)) - 100]) >> 7, max([0, abs(signed(z)) - 100]) >> 7
    
    print(x, y, z)
    
    sleep(0.1)