from app.kafka_producer import KafkaProducer
from app.flink_transformations import FlinkTransformations
from app.data_consumer import DataConsumer
from app.database_writer import DatabaseWriter
from domain.user_review import UserReview
from domain.metadata import Metadata
from domain.user_data import UserData

# Set up dependencies
kafka_producer = KafkaProducer(topic="user_reviews")
flink_transformations = FlinkTransformations()
data_consumer = DataConsumer(topic="user_reviews")
database_writer = DatabaseWriter(storage_path="/path/to/local/database")

# Simulate data production
user_reviews_data = [{"user_id": 1, "review_text": "Great product!"}]
metadata_data = [{"technical": "Tech", "business": "Biz", "logical": "Log"}]
user_data = [{"user_id": 1, "username": "user1"}]

# Produce data to Kafka
kafka_producer.produce({"user_review": user_reviews_data, "metadata": metadata_data, "user_data": user_data})

# Transform data using Flink
transformed_data = flink_transformations.transform(
    UserReview(*user_reviews_data[0]),
    Metadata(*metadata_data[0]),
    UserData(*user_data[0])
)

# Consume and write to local database
consumed_data = data_consumer.consume_data()
database_writer.write_to_database(consumed_data)
