from umqtt.simple import MQTTClient
import ujson


class MQTT:
    """ Classe para implementação do Cliente MQTT """
    
    def __init__(self, addr: str, user: str, pswd: str, port: int = 1883):
        self.__addr = addr
        self.__mqtt_user = user
        self.__mqtt_pswd = pswd
        self.__client = MQTTClient('esp32', addr, port, user, pswd)
        self.__client.set_callback(self.__on_message)
        self.__subscribed_topics = []
    
    @property
    def topicos_inscritos(self):
        return self.__subscribed_topics
    
    def __is_connected(self):
        """ Verificação da conexão do Cliente MQTT """
        try:
            self.__client.ping()
            return True
        except Exception as e:
            return False
    
    def __on_message(self, topic, msg):
        """ Função de callback para tratamento das mensagens que chegam aos tópicos assinados """
        match topic:
            case 'test/esp/topic':
                print(msg)
            case _:
                print(f'{topic}: {msg}')
    
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
        for topic in self.__subscribed_topics:
            self.__client.unsubscribe(topic)
        self.__client.disconnect()
        print(f'Desconectado do broker MQTT: "{self.__addr}"')
    
    def assinar_topico(self, topic: str):
        """ Assina um topico, caso ainda nao exista essa assinatura """
        topic = str(topic)
        if topic not in self.__subscribed_topics:
            self.__client.subscribe(topic)
            self.__subscribed_topics.append(topic)
            print(f'Assinatura ao tópico "{topic}" realizada com sucesso.')
        else:
            print(f'Já existe uma assinatura ativa ao tópico "{topic}".')
    
    def cancelar_topico(self, topic: str):
        """ Cancela a assinatura de um topico, caso ela exista """
        topic = str(topic)
        if topic in self.__subscribed_topics:
            self.__client.unsubscribe(topic)
            self.__subscribed_topics.remove(topic)
            print(f'Assinatura ao topica "{topic}" cancelada.')
        else:
            print(f'Não existe uma assinatura ativa ao topico "{topic}".')
    
    def publicar_mensagem(self, topic: str, pub_msg: dict):
        """ Publica uma mensagem (dict) em um tópico """
        json_msg = ujson.dumps(pub_msg)
        if self.__is_connected():
            self.__client.publish(topic=topic, msg=json_msg, retain=False, qos=0)
        else:
            print('Cliente não está conectado ao broker MQTT')


if __name__ == '__main__':
    mqtt_client = MQTT(addr='localhost', user='esp32', pswd='esp32', port=1883)
    print(mqtt_client.topicos_inscritos)
