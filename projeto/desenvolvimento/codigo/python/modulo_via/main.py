from MyDht import MyDht

dht = MyDht(pin=33, time_ms=5000)

while True:
    dht.update()
    
    if not dht.update_enable:
        print(dht.readings)
        dht.update_enable = True