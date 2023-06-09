import paho.mqtt.client as mqtt
import requests as r
import json
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Caldeiras/#")

# Onde está sendo enviado os dados gerados pelos "Sensores" para API
def on_message(client, userdata, msg):
    # json_data = msg.payload.decode('utf-8')
    data = msg.payload.decode('utf-8')
    
    headers = {'Content-type': 'application/json'}
    url = 'http://127.0.0.1:8000/api/login'

    try:
        response = r.post(url, data=data, headers=headers)

        if response.status_code == 200:
            print('Dados enviados com sucesso, Código de status: ', response.status_code)
        else:
            print('Erro ao enviar os dados. Código de status:', response.status_code)
    except:
        print('Falha ao enviar dados, tente novamente mais tarde')
        sys.exit()
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()