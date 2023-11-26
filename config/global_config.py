# Example configuration for Kafka
KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'your_group_id',
    # Add more Kafka configurations as needed
}

# Example configuration for Flink
FLINK_CONFIG = {
    'jobmanager.rpc.address': 'localhost',
    'flink.taskmanager.host': 'localhost',
    # Add more Flink configurations as needed
}
