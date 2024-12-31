from machine import ADC, PWM, Pin
import time

# ---------------------------------------------------------------------------------------------------------------------

# ADC

# Configurar o pino ao qual o sensor está conectado (por exemplo, GPIO 32)
adc_pin = Pin(4, mode=Pin.IN)

# Inicializar o ADC
adc = ADC(adc_pin)

# Configurar a atenuação (opcional, melhora a leitura em diferentes ranges de tensão)
adc.atten(ADC.ATTN_11DB)  # Opções: ADC.ATTN_0DB, ADC.ATTN_2_5DB, ADC.ATTN_6DB, ADC.ATTN_11DB
# A atenuação de 11DB é a máxima e permite leituras de 0V a 3,6V

# Configurar a largura do bit (opcional)
adc.width(ADC.WIDTH_12BIT)  # Opções: ADC.WIDTH_9BIT, ADC.WIDTH_10BIT, ADC.WIDTH_11BIT, ADC.WIDTH_12BIT

# ---------------------------------------------------------------------------------------------------------------------

# PWM

# Configurar o pino GPIO onde o PWM será gerado (por exemplo, GPIO15)
pwm_pin = Pin(15)

# Inicializar a saída PWM
pwm = PWM(pwm_pin)
pwm2 = PWM(Pin(2))

# Configurar a frequência do PWM
pwm.freq(1000)  # 1000 Hz (1 kHz)
pwm2.freq(1000)  # 1000 Hz (1 kHz)

# Configurar o duty cycle do PWM (0-1023)
# pwm.duty(512)  # 50% do duty cycle
# pwm2.duty(512)  # 50% do duty cycle

# ---------------------------------------------------------------------------------------------------------------------

# Alterar o duty cycle ao longo do tempo e ler o valor do ADC

while True:
    for duty in range(0, 1024):
        print(duty)
        pwm.duty(duty)
        pwm2.duty(duty)
        
        valor_adc = adc.read()
        valor_uv = adc.read_u16()
        print("Valor ADC:", valor_adc)
        print("Valor ADC:", valor_uv)
        
        time.sleep(0.1)

"""
O ESP32 possui múltiplos pinos que podem ser usados como entradas ADC (Conversor Analógico-Digital). Existem duas unidades de ADC, ADC1 e ADC2, com um total de 18 canais ADC disponíveis. Aqui estão os pinos que você pode usar para ADC:

ADC1 (8 canais)
GPIO32 (ADC1_CH4)

GPIO33 (ADC1_CH5)

GPIO34 (ADC1_CH6)

GPIO35 (ADC1_CH7)

GPIO36 (ADC1_CH0)

GPIO37 (ADC1_CH1)

GPIO38 (ADC1_CH2)

GPIO39 (ADC1_CH3)

ADC2 (10 canais)
GPIO0 (ADC2_CH1)

GPIO2 (ADC2_CH2)

GPIO4 (ADC2_CH0)

GPIO12 (ADC2_CH5)

GPIO13 (ADC2_CH4)

GPIO14 (ADC2_CH6)

GPIO15 (ADC2_CH3)

GPIO25 (ADC2_CH8)

GPIO26 (ADC2_CH9)

GPIO27 (ADC2_CH7)

Nota:
ADC1 vs ADC2:

ADC1: Pode ser usado para leituras ADC normalmente, mesmo durante o uso do WiFi.

ADC2: Pode ter conflitos quando o WiFi está ativo, pois compartilha recursos de hardware com o WiFi do ESP32.
"""