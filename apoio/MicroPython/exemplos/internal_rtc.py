from machine import RTC
import time

chaves_rtc = ['ano', 'mes', 'dia', 'semana', 'hora', 'minuto', 'segundo', 'm_seg']

rtc = RTC()

rtc.datetime((2025, 1, 1, 2, 0, 0, 0, 0))

while True:
    tempo = {chaves_rtc[k]: v for k, v in enumerate(rtc.datetime())}
    
#     print(time.time())
    
    for k, v in tempo.items():
        print(f'{k}: {v}')
    time.sleep(5)