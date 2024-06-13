import pika

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

def publish():
    channel.basic_publish(exchange='', routing_key='queue', body='This is body')