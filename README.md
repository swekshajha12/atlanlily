Refer this for all design related info: https://docs.google.com/document/d/15u3XmUEFG8pfSP2-Lh7dpqqK-JbSCZHGcq6-gfdrvPE/edit?usp=sharing

This service follows onion architecture and is aligned as follows:

```
atlanLily/
│
├── app/
│   ├── __init__.py
│   ├── kafka_producer.py
│   ├── flink_transformations.py
│   ├── data_consumer.py
│   └── database_writer.py
│
├── domain/
│   ├── __init__.py
│   ├── user_review.py
│   ├── metadata.py
│   └── user_data.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── kafka_stream.py
│   └── local_database.py
│
├── main.py
├── Dockerfile
└── docker-compose.yml
└── requirements.txt
```


**Instructions:**

1. Clone the Repository:
    Clone the sample project repository to your local machine:
    git clone https://github.com/swekshajha12/atlanlily

2. Install requirements
   pip install -r requirements.txt

   
3. Build the Docker Image:
   Build the Docker image using the provided Dockerfile:
   docker build -t app .

4. Run Docker Compose:
   Run the Docker Compose configuration to start the application:
   docker-compose up

6. Start Kafka:
   Ensure that Kafka is up and running. 
   You can use Docker Compose or any other method to start Kafka. Modify the KAFKA_BOOTSTRAP_SERVERS variable accordingly.

7. Create a Kafka Topic:
   kafka-topics --create --topic user_reviews_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

8. Produce Messages to Kafka Topic:
   Use the Kafka console producer or any other method to produce sample messages to the topic.
   kafka-console-producer --topic user_reviews_topic --bootstrap-server localhost:9092
   Enter sample messages in the console.

9. Start Flink:
   Ensure that Flink is running. You can use Docker Compose or any other method to start Flink.

10. Submit Flink Job:
   Build the Flink job JAR file using your application code.

11. Submit the Flink job to the Flink cluster.
   ./bin/flink run -c your.package.name.FlinkUserReviewTransformationJob path/to/your/application.jar

12. Start the Python Application:
   Ensure that the Python dependencies are installed (confluent_kafka, pyarrow).
   python main.py
This application should connect to Kafka, consume messages from the user_reviews_topic, perform light transformations, and store the data in local Parquet files.

13. Verify Data in Parquet Files:
    Check the local directory specified in the application for Parquet files.

14. Verify that the transformed data is stored correctly.

15. Stop the Application:
   To stop the running containers, use the following command:
   docker-compose down
   



