from machine import RTC
import time

rtc = RTC()

rtc.datetime((2024, 12, 28, 5, 23, 18, 0, 0))

while True:
    grtc = rtc.datetime()
    tempo = {
        'dia':grtc[2],
        'mes':grtc[1],
        'ano':grtc[0] - 2000,
        'hora':grtc[4],
        'minuto':grtc[5],
        'segundo':grtc[6]
        }
    
    print(time.time())
    
    for k, v in tempo.items():
        print(f'{k}: {v}')
    time.sleep(5)