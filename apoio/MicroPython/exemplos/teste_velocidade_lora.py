def calcular_crc16(data:list[bytes], polinomio=0x8408) -> list[bytes, bytes]:
    if type(data) == list:
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ polinomio
                else:
                    crc >>= 1
        
        crc = ~crc & 0xFFFF
        crc_h = crc >> 8
        crc_l = crc & 0x00FF
        return [crc_h, crc_l, crc]
    else:
        raise AttributeError('Variavel recebida não é do tipo list')


def verificar_crc16(data:list[bytes]) -> list[bytes]:
    if type(data) == list:
        dados_uteis = data[:-2]
        dados_check = data[-2] << 8 | data[-1]
        if dados_check == calcular_crc16(dados_uteis)[2]:
            return dados_uteis
        else:
            return None
    else:
        raise AttributeError('Variavel recebida não é do tipo list')



if __name__ == '__main__':
    from machine import UART
    
    serial = UART(1, baudrate=115200, tx=27, rx=26)
    
    pacote1 = [0x01, 0x03, # addr
               0x10, # type
               25, 1, 25, # date
               0, 0, 0, # time
               85, 125, # umid, temp
               0, 0, 0, # gx, gy, gz
               5, 0, 3, 30, # adc1, adc2
               0xFF, 0xFF, 0xFF, 18 # final de mensagem
               ]

    pacote2 = [0x01, 0x03, # addr
               0x10, # type
               24, 12, 25, # date
               0, 30, 0, # time
               89, 145, # umid, temp
               10, 20, 30, # gx, gy, gz
               4, 99, 2, 45, # adc1, adc2
               0xFF, 0xFF, 0xFF, 18 # final de mensagem
               ]

    pacote3 = [0x01, 0x03, # addr
               0x20, # type
               0x42, # check
               0xFF, 0xFF, 0xFF, 4 # final de mensagem
               ]

    for p in [pacote1, pacote2, pacote3]:
        checksum = calcular_crc16(p)
        for byte in checksum[:2]:
            p.append(byte)
        p.append(0x42)
    
    pacote_completo = pacote1 + pacote2 + pacote3
    print(pacote_completo)
    print(len(pacote_completo))
    
    p = bytes(pacote_completo)
    
    serial.write(p)
