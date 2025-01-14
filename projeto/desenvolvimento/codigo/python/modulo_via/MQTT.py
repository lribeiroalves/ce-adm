from umqtt.simple import MQTTClient


class MQTT:
    """ Classe para implementação do Cliente MQTT """
    
    def __init__(self, addr: str, user: str, pswd: str, port: int = 1883):
        self.__mqtt_user = user
        self.__mqtt_pswd = pswd
        self.__client = MQTTClient('esp32', addr, port, user, pswd)
        self.__subscribed_topics = []
    
    @property
    def topicos_inscritos(self):
        return self.__subscribed_topics
    
    def conectar(self):
        """ Tenta conectar ao broker MQTT e para a execução caso não consiga """
        try:
            self.__client.connect()
            print('Conectado ao Broker MQTT')
        except OSError as e:
            print(f'Erro ao conectar ao Broker MQTT: {e}')
            while True:
                pass
    
    def desconectar(self):
        """ Cancela todas as assinaturas e desconecta do broker MQTT """
        pass
    
    def assinar_topico(self, topic):
        """ Assina um topico, caso ainda nao exista essa assinatura """
        pass
    
    def cancelar_topico(self, topic):
        """ Cancela a assinatura de um topico, caso ela exista """
        pass
    
    def publicar_mensagem(self, topic, msg):
        """ Publica uma mensagem em um tópico """
        pass


if __name__ == '__main__':
    mqtt_client = MQTT('localhost', 'esp32', 'esp32', 1883)
    print(mqtt_client.topicos_inscritos)
