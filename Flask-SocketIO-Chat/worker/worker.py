import base64
import json
import pickle
import pika
import time
from pymemcache.client.base import Client
from pymongo import MongoClient
time.sleep(30)

print("Connecting to rabbitmq...",flush=True)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
queue_in_name="channel_in"
queue_out_name="channel_out"
channel.queue_declare(queue=queue_in_name)
channel.queue_declare(queue=queue_out_name)
print("Connected!",flush=True)

print("Connecting to memcached...",flush=True)
memcached = Client('memcached')
print("Connected!",flush=True)
memcached.set('chat_his',base64.b64encode(pickle.dumps([])))

client = MongoClient("mongodb://mongo:27017/")
db = client.chat_db
collection = db.users
posts = db.posts
posts.delete_many({})


def callback(ch, method, properties, body):
    global memcached
    request = json.loads(body)
    if request['action'] == 'send':
        chat_his = pickle.loads(base64.b64decode(memcached.get('chat_his')))
        chat_his += [{request['name']: request['message']}]
        memcached.set('chat_his', base64.b64encode(pickle.dumps(chat_his)))
        posts.insert_one({request['name']: request['message']}).inserted_id
    else:
        chat_his = pickle.loads(base64.b64decode(memcached.get('chat_his')))
        channel.basic_publish(exchange='', routing_key=queue_out_name,
                              body=json.dumps(chat_his))

channel.basic_consume(queue=queue_in_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()