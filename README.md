Refer this for all design related info: https://docs.google.com/document/d/15u3XmUEFG8pfSP2-Lh7dpqqK-JbSCZHGcq6-gfdrvPE/edit?usp=sharing

atlanLily_example/
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

