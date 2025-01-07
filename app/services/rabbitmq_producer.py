import json, pika
from decouple import config

courier_queue = config('RABBITMQ_QUEUE')

def publish_message(courier_queue: str, message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config('RABBITMQ_HOST'))
    )
    channel = connection.channel()
    channel.queue_declare(queue=courier_queue)
    
    channel.basic_publish(
        exchange='',
        routing_key=courier_queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(content_type="application/json")
    )
    
    print(f' [X] Sent {message} to queue {courier_queue}')
    
    connection.close()
    
