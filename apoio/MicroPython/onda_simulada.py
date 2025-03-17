from machine import DAC, Pin
import time
import math
import random

dac = DAC(Pin(26))
dac.write(255)
tempo = random.randint(1000, 5000)
prev = 0

# Função para gerar um semi-ciclo negativo de uma senoide
def gerar_senoide():
    
    amostras = 2000
    
    intervalo = 1 / amostras

    # Quando o pino 23 for ativado, começamos a transição
    for i in range(amostras):
        # Gerar valor da senoide (cai para 0 e volta para 1, criando um semi ciclo negativo)
        valor_senoide = int(255 * (1 - math.sin(math.pi * i / amostras)))  # Semi-ciclo negativo

        # Ajusta o valor do DAC (vai de 255 -> 0 -> 255)
        dac.write(valor_senoide)

        # Aguarda o intervalo entre amostras
        time.sleep(intervalo)

while True:
    curr = time.ticks_ms()

    if curr >= tempo + prev:
        prev = curr
        tempo = random.randint(1000, 5000)
        
        ciclos = random.randint(1, 25)
        
        for _ in range(ciclos+1):
            gerar_senoide()
            time.sleep(0.3)
        
        dac.write(255)

        