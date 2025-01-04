from machine import Pin, SoftI2C

sda_pin = 21
scl_pin = 22
list_rst_pin = None # must be a list of rst pins of the devices

# Configuração do I2C
i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))

# Alguns dispositivos I2C precisam de um reset via software antes de iniciar a comunicação
if list_rst_pin:
    for pin in list_rst_pin:
        pino = Pin(pin, Pin.OUT)
        pino.value(0)
        pino.value(1)

# Escanear dispositivos I2C no barramento
dispositivos = i2c.scan()

if dispositivos:
    print("Dispositivos I2C encontrados:", [hex(d) for d in dispositivos])
else:
    print("Nenhum dispositivo I2C encontrado")

