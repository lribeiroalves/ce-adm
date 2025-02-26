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
from adm_server.ext.database.models import *


broker_address = 'localhost'
broker_port = 1883
mqtt_user = 'flask'
mqtt_passwd = 'flask'
mqtt_topics = [
    'test/server/hello',
    'adm/esp_sala/server/req_time',
    'adm/esp_sala/server/readings_sala',
    'adm/esp_sala/server/readings_teste',
    'adm/esp_sala/server/readings_controle',
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
            
        case 'adm/esp_sala/server/req_time':
            if is_valid_json(msg):
                msg = json.loads(msg)
                if msg['msg_type'] == 0x20 and msg['check'] == 0x42:
                    # Send back time
                    time = datetime.datetime.now()
                    msg = {
                        'year': time.year,
                        'month': time.month,
                        'day': time.day,
                        'hour': time.hour,
                        'minute': time.minute,
                        'second': time.second
                    }
                    msg_json = json.dumps(msg)
                    client_mqtt.publish('adm/server/esp_sala/clock', msg_json)
                else:
                    print('Parâmetros inválidos.')
            else:
                print('Not a Valid JSON Object')
        
        case 'adm/esp_sala/server/readings_teste' | 'adm/esp_sala/server/readings_controle':
            if is_valid_json(msg):
                msg = json.loads(msg)
                chaves_esperadas = ['num_pacote_0', 'num_pacote_1', 'num_pacote_2', 'temp', 'umid', 'gX', 'gY', 'gZ', 'ad_sen_int', 'ad_sen_dec', 'ad_bat_int', 'ad_bat_dec', 'year', 'month', 'day', 'hour', 'minute', 'second']
                if set(chaves_esperadas) == set(msg.keys()):
                    # Converter os bytes de numeração do pacote
                    num_pacote = bytes([msg['num_pacote_0'], msg['num_pacote_1'], msg['num_pacote_2']])
                    num_pacote = int.from_bytes(num_pacote)

                    data_recebida = datetime.date(msg['year'], msg['month'], msg['day'], msg['hour'], msg['minute'], msg['second'])

                    with app.app_context():
                        if topic.split('/')[-1] == 'readings_teste':
                            new_data = EspTeste()
                        else:
                            new_data = EspControle()

                        new_data.num_pacote = num_pacote
                        new_data.temp = msg['temp']
                        new_data.umid = msg['umid']
                        new_data.gX = msg['gX']
                        new_data.gY = msg['gY']
                        new_data.gZ = msg['gZ']
                        new_data.ad_sen_int = msg['ad_sen_int']
                        new_data.ad_sen_dec = msg['ad_sen_dec']
                        new_data.ad_bat_int = msg['ad_bat_int']
                        new_data.ad_bat_dec = msg['ad_bat_dec']
                        new_data.date = data_recebida
                        
                        db.session.add(new_data)
                        db.session.commit()
                else:
                    print('A Mensagem recebida não está no padrão esperado.')
            else:
                print('Not a valid JSON')

        case 'adm/esp_sala/server/readings_sala':
            if is_valid_json(msg):
                msg = json.loads(msg)
                chaves_esperadas = ['num_pacote_0','num_pacote_1','num_pacote_2','sys1_t_int','sys1_t_dec','sys2_t_int','sys2_t_dec','sys1_c_int','sys1_c_dec','sys2_c_int','sys2_c_dec','occ_t','occ_c','reset_t','reset_c', 'year', 'month', 'day', 'hour', 'minute', 'second']
                if set(chaves_esperadas) == set(msg.keys()):
                    # Converter os bytes de numeração do pacote
                    num_pacote = bytes([msg['num_pacote_0'], msg['num_pacote_1'], msg['num_pacote_2']])
                    num_pacote = int.from_bytes(num_pacote)

                    data_recebida = datetime.date(msg['year'], msg['month'], msg['day'], msg['hour'], msg['minute'], msg['second'])

                    with app.app_context():
                        new_data = EspSala()

                        new_data.num_pacote = num_pacote
                        new_data.num_pacote_0 = msg['num_pacote_0']
                        new_data.num_pacote_1 = msg['num_pacote_1']
                        new_data.num_pacote_2 = msg['num_pacote_2']
                        new_data.sys1_t_int = msg['sys1_t_int']
                        new_data.sys1_t_dec = msg['sys1_t_dec']
                        new_data.sys2_t_int = msg['sys2_t_int']
                        new_data.sys2_t_dec = msg['sys2_t_dec']
                        new_data.sys1_c_int = msg['sys1_c_int']
                        new_data.sys1_c_dec = msg['sys1_c_dec']
                        new_data.sys2_c_int = msg['sys2_c_int']
                        new_data.sys2_c_dec = msg['sys2_c_dec']
                        new_data.occ_t = msg['occ_t']
                        new_data.occ_c = msg['occ_c']
                        new_data.reset_t = msg['reset_t']
                        new_data.reset_c = msg['reset_c']
                        new_data.date = data_recebida
                        
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
        print(f'Conectado ao broker MQTT: {broker_address}')
        for t in mqtt_topics:
            client_mqtt.subscribe(t)

        signal.signal(signal.SIGINT, signal_handler) # Captura o comando Ctrl+c (SIGINT) e chama a função signal handler
        signal.signal(signal.SIGTERM, signal_handler) # Captura encerramento pelo sistema por erro
        threading.Thread(target=loop_mqtt).start() # inicia o loop mqtt em outro thread
    except:
        print('Não foi possível conectar ao Broker MQTT.')
        print('Encerrando a aplicação...')
        sys.exit(1)


