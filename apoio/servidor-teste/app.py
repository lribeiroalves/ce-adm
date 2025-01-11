from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
import threading

# Criar o app e o socket
app = Flask(__name__)
app.config['SECRET_KEY'] = '1787d9e9a1445f361e660e6faeb6bedecac8694d23727bd846723e9dd90fb7d2'
socketio = SocketIO(app)

# Configurar o cliente MQTT
broker_address = 'localhost'
client = mqtt.Client()

# Função de callback para mensagens recebidas
def on_message(client, userdata, message): 
    data = {
        'topic': message.topic,
        'message': message.payload.decode()
    }
    socketio.emit('mqtt_message', data)

# Conectar ao broker
client.on_message = on_message
client.connect(broker_address)

# Lista de tópicos inscritos
subscribed_topics = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    topic = request.json.get('topic')
    if topic not in subscribed_topics:
        client.subscribe(topic)
        subscribed_topics.append(topic)
        return {'message': f'Subscribed to {topic}'}, 200
    else:
        return {'message': f'Topic: "{topic}" alredy subscribed.'}, 403


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    topic = request.json.get('topic')
    if topic in subscribed_topics:
        client.unsubscribe(topic)
        subscribed_topics.remove(topic)
        return {'message': f'Unsubscribed from {topic}.'}, 200
    else:
        return {'message': f'There is no subscription to {topic}.'}, 403


def mqtt_loop():
    client.loop_forever()


if __name__ == '__main__':
    threading.Thread(target=mqtt_loop).start()
    socketio.run(app, host='0.0.0.0', port=5000)