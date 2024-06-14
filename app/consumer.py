import pika
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

channel.queue_declare(queue='persist_queue', durable=True)

def callback(ch, method, properties, body):
    if properties.content_type == 'sending_email':
        from data.services import send_email
        send_email(email=body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print('Done')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='persist_queue', on_message_callback=callback)
channel.start_consuming()
channel.close()
