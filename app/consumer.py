import logging
import pika
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

logger = logging.getLogger('backend')

connection = pika.BlockingConnection(
    pika.URLParameters('amqp://guest:guest@rabbitmq/')
)
channel = connection.channel()

channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
channel.exchange_declare(exchange='dlx', exchange_type='fanout')

channel.queue_declare(
    queue='main_queue', durable=True, arguments={'x-dead-letter-exchange': 'dlx', 'x-message-ttl': 2000}
)
channel.queue_declare(queue='dl_queue')

channel.queue_bind(queue='main_queue', exchange='main_exchange', routing_key='email')
channel.queue_bind(queue='dl_queue', exchange='dlx')

def main_callback(ch, method, properties, body):
    if properties.content_type == 'sending_email':
        from data.services import send_email
        try:
            send_email(email=body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.info('Done')
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag)

def dead_letter_callback(ch, method, properties, body):
    # TODO: Use sentry or other observability options in production.
    logger.warning('Hello from dead letter queue...')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='main_queue', on_message_callback=main_callback)
channel.basic_consume(queue='dl_queue', on_message_callback=dead_letter_callback)

channel.start_consuming()
channel.close()
