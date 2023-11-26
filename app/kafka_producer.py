from functools import partial

from infrastructure.kafka_stream import KafkaStream
from confluent_kafka import Producer, KafkaError
from config import global_config
import ast


class KafkaProducer:
    _instance = None

    def __init__(self):
        self.host = global_config.KAFKA_HOST
        self.port = global_config.KAFKA_PORT
        self.config = global_config.KAFKA_CONFIG
        self.producer = self.initialise_producer(self.host, self.port, self.config)

    @staticmethod
    def initialise_producer(host, port, config):
        if KafkaProducer._instance is None:
            server_dict = {"bootstrap.servers": f"{host}:{port}"}
            server_config = ast.literal_eval(config)
            parameters = {**server_dict, **server_config}
            KafkaProducer._instance = Producer(parameters)
        return KafkaProducer._instance

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
