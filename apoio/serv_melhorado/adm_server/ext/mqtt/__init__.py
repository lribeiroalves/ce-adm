""" MQTT Client Factory """

import paho.mqtt.client as mqtt
from flask_socketio import emit
import threading
import signal
import sys
import json
import datetime

from adm_server.ext.socket_io import socketio
from adm_server.ext.database import db
from adm_server.ext.database.models import Readings, EspSensor


broker_address = 'localhost'
broker_port = 1883
mqtt_user = 'flask'
mqtt_passwd = 'flask'
mqtt_topics = [
    'test/server/hello',
    'test/server/read',
    'adm/esp_sensor/server',
    ]
client_mqtt = mqtt.Client()
client_mqtt.username_pw_set(mqtt_user, mqtt_passwd)


# Avalia se a string é um json válido
def is_valid_json(text: str):
    try:
        json.loads(text)
    except ValueError as e:
        return False
    return True


# Função que será chamada sempre que um topico inscrito receber uma mensagem
def on_message(app, client, userdata, message):
    topic = message.topic
    msg = message.payload.decode()
    match topic:
        case 'test/server/hello':
            data = {
                'topic': topic,
                'message': msg
            }
            socketio.emit('mqtt_message', data)
            
        case 'test/server/read':
            if is_valid_json(msg):
                msg = json.loads(msg)
                with app.app_context():
                    new_data = Readings(name=msg['name'], pacote=msg['pacote'], led=msg['led'], adc=msg['adc'], date=datetime.datetime.now())
                    db.session.add(new_data)
                    db.session.commit()
            else:
                print('Not a Valid JSON Object')
        
        case 'adm/esp_sensor/server':
            if is_valid_json(msg):
                msg = json.loads(msg)
                chaves_esperadas = ['addr', 'msg_type', 'temp', 'umid', 'gX', 'gY', 'gZ', 'adc_int', 'adc_dec', 'year', 'month', 'day', 'hour', 'minute', 'second']
                if set(chaves_esperadas) == set(msg.keys()):
                    with app.app_context():
                        new_data = EspSensor()

                        new_data.addr = msg['addr']
                        new_data.msg_type = msg['msg_type']
                        new_data.temp = msg['temp']
                        new_data.umid = msg['umid']
                        new_data.gX = msg['gX']
                        new_data.gY = msg['gY']
                        new_data.gZ = msg['gZ']
                        new_data.adc_int = msg['adc_int']
                        new_data.adc_dec = msg['adc_dec']
                        new_data.year = msg['year']
                        new_data.month = msg['month']
                        new_data.day = msg['day']
                        new_data.hour = msg['hour']
                        new_data.minute = msg['minute']
                        new_data.second = msg['second']
                        new_data.date = datetime.datetime.now()
                        
                        db.session.add(new_data)
                        db.session.commit()
                else:
                    print('A Mensagem recebida não está no padrão esperado.')
            else:
                print('Not a valid JSON')

        case _:
            pass
            

# Função quee será executada para sempre em outro thread 
def loop_mqtt():
    client_mqtt.loop_forever()


# Função chamada ao pressionar Ctrl+C
def signal_handler(sig, frame):
    print('Encerrando a aplicação...')
    client_mqtt.disconnect() # Ao disconectar do broker o método loop forever retorna
    sys.exit(0) # Encerra a aplicação


def init_app(app):
    try:
        client_mqtt.on_message = lambda client, userdata, message: on_message(app, client, userdata, message) # Associa a função de callback para mensagens
        client_mqtt.connect(broker_address)
        for t in mqtt_topics:
            client_mqtt.subscribe(t)

        signal.signal(signal.SIGINT, signal_handler) # Captura o comando Ctrl+c (SIGINT) e chama a função signal handler
        signal.signal(signal.SIGTERM, signal_handler) # Captura encerramento pelo sistema por erro
        threading.Thread(target=loop_mqtt).start() # inicia o loop mqtt em outro thread
    except:
        print('Não foi possível conectar ao Broker MQTT.')
        print('Encerrando a aplicação...')
        sys.exit(1)


