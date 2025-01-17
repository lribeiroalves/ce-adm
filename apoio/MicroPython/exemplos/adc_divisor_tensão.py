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
    new_ten = (0.922 * ten) + 0.140 # 0.01 de erro
    fonte = (32.34 * new_ten) - 47.84 # 0.3 de erro
    v = value
    fonte2 = 32.34 * (0.922 * (v * 3.6 / 4095) + 0.140) - 47.84
    print(value)
    print(f'Pino: {ten:.2f} V')
    print(f'Pino Corrigido: {new_ten: .2f} V')
    print(f'Fonte: {fonte:.1f} V\n')
    print(f'{fonte2:.2f}')
    