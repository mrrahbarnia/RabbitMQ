import pika
import json

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

def publish(method, body):
    channel.queue_declare(queue='persist_queue', durable=True)
    properties = pika.BasicProperties(
        method, delivery_mode=pika.DeliveryMode.Persistent
    )
    body = json.dumps(body)
    channel.basic_publish(
        exchange='', routing_key='persist_queue', body=body, properties=properties
    )
