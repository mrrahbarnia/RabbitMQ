import pika

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

channel.queue_declare(queue='queue')

def callback(ch, method, properties, body):
    print('Hello')
    print(method)
    print(properties)
    print(body)

channel.basic_consume(queue='queue', on_message_callback=callback)
channel.start_consuming()
channel.close()

