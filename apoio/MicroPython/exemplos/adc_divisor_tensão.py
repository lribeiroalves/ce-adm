from machine import Pin, ADC
from time import sleep, sleep_ms

adc = ADC(Pin(34))

adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

def medir():
    v = 0
    
    for c in range(0, 100):
        v += adc.read()
        sleep_ms(10)
    v = v/100
    
    return v

while True:
    value = medir()
    ten = value * 3.6 / 4095
    fonte = round(ten, 2) * 17.242
    print(value)
    print(f'Pino: {ten:.2f} V')
    print(f'Fonte: {fonte:.2f} V\n')
    