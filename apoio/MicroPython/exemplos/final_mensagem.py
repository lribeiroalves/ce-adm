def verificar_final_de_mensagem(buffer:list):
    mensagens_separadas = []
    final = [0xFF, 0xFF, 0xFF, 0xFF]
    final_len = len(final)
    buffer_len = len(buffer)
    
    if buffer_len >= final_len + 5:
        for i in range(buffer_len - final_len + 1):
            if buffer[i:i + final_len] == final:
                mensagem = buffer[i - buffer[i + final_len]: i + final_len + 4]
                mensagens_separadas.append(mensagem)
    
    return mensagens_separadas

if __name__ == '__main__':
    m0 = [0x00, 0x05, 0x04]
    m1 = [0x01, 0x03, 0x10, 25, 1, 25, 0, 0, 0, 85, 125, 0, 0, 0, 5, 0, 3, 30, 0xFF, 0xFF, 0xFF, 0xFF, 18, 0x00, 0x00, 0x1]
    m2 = [0xaa, 0x4a, 0x2b, 0x25, 0x58, 0x98, 85, 125, 0, 0, 0, 5, 0, 3, 30, 0xFF, 0xFF, 0xFF]
    m3 = [0x01, 0x03, 0x20, 0x42, 0xFF, 0xFF, 0xFF, 0xFF, 4, 0x00, 0x00, 0x01]
    m4 = [0xaa, 0x4a, 0x2b, 0x25, 0x58, 0x98, 0x85]
    
    pacote = m0 + m1 + m2 + m3 + m4
    
    print(pacote, end='\n'*3)
    
    mensagens = verificar_final_de_mensagem(pacote)
    if mensagens:
        for mensagem in mensagens:
            print(mensagem)
    