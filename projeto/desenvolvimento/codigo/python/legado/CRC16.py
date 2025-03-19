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
    data = [0x01, 0xFE, 0x90, 0x7F, 0x3C, 0xFA, 0x07, 0x94, 0xA3]
    data2 = [0x01, 0xFE, 0x90, 0x7F, 0x3C, 0xFA, 0x07, 0xA3, 0x94]
    data_sent = [0x01, 0xFE, 0x90, 0x7F, 0x3C, 0xFA, 0x07, 0x94, 0xA3, 0x29, 0x1D]
    checksum = calcular_crc16(data)
    checksum2 = calcular_crc16(data2)
    print(verificar_crc16(data))
    if checksum:
        print(f'{checksum[0]:x}, {checksum[1]:x}')
        print(f'{checksum2[0]:x}, {checksum2[1]:x}')
    else:
        print('None')