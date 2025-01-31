from machine import RTC

class Clock:
    """ Classe criada com o objetivo de faciliar
        a implementação do uso do RTC interno do ESP32 """
    
    def __init__(self):
        self.__rtc = RTC()
        self.__rtc.datetime((2025, 1, 1, 0, 0, 0, 0, 0))
        self.__keys = ['ano', 'mes', 'dia', 'semana', 'hora', 'minuto', 'segundo', 'm_seg']
        self.__is_set = False
    
    
    @property
    def is_set(self):
        return self.__is_set
    
    
    @is_set.setter
    def is_set(self, value:bool):
        if value == False:
            self.__is_set = False
        else:
            raise ValueError('Esse atributo só pode ser alterado para falso.')
    
    
    def get_time(self):
        """ Retorna as informações do rtc interno em forma de um dicionario """
        return {self.__keys[k]: v for k, v in enumerate(self.__rtc.datetime())}
    
    
    def set_time(self, ano: int, mes: int, dia: int,
                 hora: int, minuto: int, segundo: int):
        """ Define um novo horário para o rtc interno """
        # NECESSÁRIO TRATAR POSSÍVEIS ERROS DE DATAS INSERIDAS PELO USUÁRIO
        if ano < 100:
            ano += 2000
        
        self.__rtc.datetime((ano, mes, dia, 0, hora, minuto, segundo, 0))
        self.__setted = True


if __name__ == '__main__':
    import time
    
    rtc = Clock()
    
    counter = 0
    
    while True:
        print(rtc.get_time())
        
        if counter == 3:
            rtc.set_time(25,11,26,12,30,0)
            counter += 1
        else:
            counter += 1
            
        time.sleep(1)
