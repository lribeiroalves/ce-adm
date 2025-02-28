from umqtt.simple import MQTTClient
import ujson
import time

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
            print(f'Conectado ao Broker MQTT: {self.__addr}')
        except OSError as e:
            print(f'Erro ao conectar ao Broker MQTT: {e}')
            time.sleep(0.5)
            self.conectar()
    
    
    def desconectar(self):
        """ Desconecta do broker MQTT """
        self.__client.disconnect()
        print(f'Desconectado do broker MQTT: "{self.__addr}"')
    
    
    def definir_cb(self, cb_func, clock=None):
        """ Definir função de callback """
        if callable(cb_func):
            if clock:
                self.__client.set_callback(lambda topic, msg: cb_func(topic, msg, clock))
            else:
                self.__client.set_callback(cb_func)
        else:
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
        """ Cancela a assinatura de um topico, caso ela exista """
        for topic in topics[0:]:
            try:
                self.__subscribed_topics.remove(topic)
            except ValueError as e:
                print(f'Não existe uma assinatura ativa ao topico "{topic}".')
        print('Cancelando assinaturas...')
        
        self.__client.disconnect()
        self.__client.connect()
        for t in self.__subscribed_topics:
            self.__client.subscribe(t)
        for topic in topics[0:]:
            print(f'Assinatura ao topico {topic} cancelada.')
    
    
    def publicar_mensagem(self, topic: str, pub_msg: dict):
        """ Publica uma mensagem (dict) em um tópico """
        json_msg = ujson.dumps(pub_msg)
        if self.__is_connected():
            self.__client.publish(topic=topic, msg=json_msg, retain=False, qos=0)
        else:
            print('Cliente não está conectado ao broker MQTT')
            self.conectar()
    
    
    def chk_msg(self, wait_msg: bool = False):
        """ Verificar novas mensagens """
        if self.__is_connected():
            if not wait_msg:
                self.__client.check_msg()
            else:
                self.__client.wait_msg()
        else:
            print('Cliente não está conectado ao broker MQTT')
            self.conectar()


if __name__ == '__main__':
    from WIFI import WIFI
    import time
    
    # Função de callback para mensagens recebidas via MQTT
    def callback(topic: bytes, msg: bytes):
        if topic.decode() == topico_sub[0]:
            print(topic.decode(), msg.decode())
    
    wifi = WIFI('2GNETVIRTUA_AP188', '194267140')
    wifi.conectar()
    mqtt_client = MQTT(addr='192.168.0.10', user='esp32', pswd='esp32', port=1883)
#     mqtt_client.definir_cb(callback)
    print(mqtt_client.topicos_assinados)
    mqtt_client.conectar()
    mqtt_client.assinar_topicos(['test/esp/topic', 'test/test/topic'])
    print(mqtt_client.topicos_assinados)
    print('Aguardando mensagens...')
    mqtt_client.chk_msg(True)
    mqtt_client.cancelar_topicos(mqtt_client.topicos_assinados)
    print(mqtt_client.topicos_assinados)
    print('Aguardando novas mensagens...')
    mqtt_client.chk_msg(True)
    print(mqtt_client.topicos_assinados)
    print('Publicando Mensagem')
    mqtt_client.publicar_mensagem('test/cli/topic', {'teste':'testando'})
    time.sleep(3)
    mqtt_client.desconectar()
    
    
