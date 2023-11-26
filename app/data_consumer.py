from infrastructure.kafka_stream import KafkaStream

class DataConsumer:
    def __init__(self, topic):
        self.kafka_stream = KafkaStream(topic)

    def consume_data(self):
        # Consume data from Kafka
        data = self.kafka_stream.consume()
        return data