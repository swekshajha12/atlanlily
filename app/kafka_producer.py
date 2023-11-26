from infrastructure.kafka_stream import KafkaStream
from confluent_kafka import Producer, KafkaError
from config import global_config


class KafkaProducer:
    def __init__(self, topic, bootstrap_servers='localhost:9092'):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def produce(self, data):
        # Convert data to bytes if needed
        message_value = str(data).encode('utf-8')

        # Produce the message to the Kafka topic
        self.producer.produce(self.topic, value=message_value, callback=self.delivery_report)

        self.producer.flush()

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')


# Example Usage:
if __name__ == "__main__":
    kafka_producer = KafkaProducer(topic='your_topic')
    data_to_produce = {'user_id': 123, 'review': 'Great product!'}
    kafka_producer.produce(data_to_produce)
