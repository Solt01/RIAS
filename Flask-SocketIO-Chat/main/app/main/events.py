import json
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import pika
import pickle
import base64

print("Connecting to rabbitmq...",flush=True)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
queue_in_name="channel_out"
queue_out_name="channel_in"
channel.queue_declare(queue=queue_in_name)
channel.queue_declare(queue=queue_out_name)
print("Connected!",flush=True)


@socketio.on('joined', namespace='/chat')
def joined(message):
    # Отправляется клиентами, когда они входят в комнату.
    # Сообщение о состоянии передается всем людям в комнате.
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' вошёл в комнату.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    # Отправлено клиентом, когда пользователь ввел новое сообщение.
    # Сообщение отправляется всем людям в комнате.
    room = session.get('room')
    channel.basic_publish(exchange='', routing_key=queue_out_name, body=json.dumps({'name':session.get('name'),'message':message['msg'],'action':'send'}))
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    # Отправляется клиентами, когда они покидают комнату.
    # Сообщение о состоянии передается всем людям в комнате.
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' покинул комнату.'}, room=room)

def retChat():
    channel.basic_publish(exchange='', routing_key=queue_out_name,
                          body=json.dumps({'action':'get'}))
    body = None
    while (body is None):
        method, properties, body = channel.basic_get(queue_in_name, True)
    return body

