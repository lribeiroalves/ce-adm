from umqtt.simple import MQTTClient
import ujson


class MQTT:
    """ Classe para implementação do Cliente MQTT """
    
    def __init__(self, addr: str, user: str, pswd: str, port: int = 1883, callback_func = None):
        self.__addr = addr
        self.__mqtt_user = user
        self.__mqtt_pswd = pswd
        self.__client = MQTTClient('esp32', addr, port, user, pswd)
        if callback_func:
            self.__client.set_callback(callback_func)
        else:
            self.__client.set_callback(self.__on_message)
        self.__subscribed_topics = []
    
    @property
    def topicos_assinados(self) -> list:
        return self.__subscribed_topics
    
    def __is_connected(self):
        """ Verificação da conexão do Cliente MQTT """
        try:
            self.__client.ping()
            return True
        except Exception as e:
            return False
    
    def __on_message(self, topic: bytes, msg: bytes):
        """ Função de callback para tratamento das mensagens que chegam aos tópicos assinados """
        if topic == b'test/esp/topic':
            print(msg.decode())
        else:
            print(f'Topic: {topic.decode()} - Message: {msg.decode()}')
    
    def conectar(self):
        """ Tenta conectar ao broker MQTT e para a execução caso não consiga """
        try:
            self.__client.connect()
            print('Conectado ao Broker MQTT: {self.__addr}')
        except OSError as e:
            print(f'Erro ao conectar ao Broker MQTT: {e}')
            while True:
                pass
    
    def desconectar(self):
        """ Desconecta do broker MQTT """
        self.__client.disconnect()
        print(f'Desconectado do broker MQTT: "{self.__addr}"')
    
    def definir_cb(self, cb_func):
        """ Definir função de callback """
        try:
            if cb_func.__code__.co_argcount == 2:
                self.__client.set_callback(cb_func)
            else:
                print('A função passada para o callback precisa ter dois argumentos (topic, msg)')
        except AttributeError:
            print('É necessário passar um callable com 2 argumentos Ex:"callback_function(topic, msg)"')
    
    def assinar_topicos(self, topics: list[str]):
        """ Assina um topico, caso ainda nao exista essa assinatura """
        for topic in topics:
            topic = str(topic)
            if topic not in self.__subscribed_topics:
                self.__client.subscribe(topic)
                self.__subscribed_topics.append(topic)
                print(f'Assinatura ao tópico "{topic}" realizada com sucesso.')
            else:
                print(f'Já existe uma assinatura ativa ao tópico "{topic}".')

    
    def cancelar_topicos(self, topics: list[str]):
        """ NÃO UTILIZAR! - BIBLIOTECA umqtt.simple AINDA NAO POSSUI ESSA FUNCIONALIDADE """
        return
        """ Cancela a assinatura de um topico, caso ela exista """
        for topic in topics:
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
    
    def chk_msg(self, wait_msg: bool = False):
        """ Verificar novas mensagens """
        if not wait_msg:
            self.__client.check_msg()
        else:
            self.__client.wait_msg()


if __name__ == '__main__':
    from WIFI import WIFI
    import time
    
    wifi = WIFI('ssid', 'pswd')
    wifi.conectar()
    mqtt_client = MQTT(addr='broker_ip', user='esp32', pswd='esp32', port=1883)
    print(mqtt_client.topicos_assinados)
    mqtt_client.conectar()
    mqtt_client.assinar_topicos(['test/esp/topic', 'test/test/topic'])
    print(mqtt_client.topicos_assinados)
    print('Aguardando mensagens...')
    mqtt_client.chk_msg(True)
    mqtt_client.cancelar_topicos(mqtt_client.topicos_assinados)
    print(mqtt_client.topicos_assinados)
    print('Publicando Mensagem')
    mqtt_client.publicar_mensagem('test/cli/topic', {'teste':'testando'})
    time.sleep(3)
    mqtt_client.desconectar()
    
    
