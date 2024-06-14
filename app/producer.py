import pika
import json


connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

channel.queue_declare(
    queue='main_queue', durable=True, arguments={'x-dead-letter-exchange': 'dlx', 'x-message-ttl': 2000}
)
channel.queue_declare(queue='dl_queue')

channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
channel.exchange_declare(exchange='dlx', exchange_type='fanout')

channel.queue_bind(queue='main_queue', exchange='main_exchange', routing_key='email')
channel.queue_bind(queue='dl_queue', exchange='dlx')

def publish(method, body):
    properties = pika.BasicProperties(
        method, delivery_mode=pika.DeliveryMode.Persistent
    )
    body = json.dumps(body)
    channel.basic_publish(
        exchange='main_exchange', routing_key='email', body=body, properties=properties
    )
