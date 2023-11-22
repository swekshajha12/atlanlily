# atlanlily

**Problem statement**

    The Atlan platform has many use cases for ingesting and consuming metadata. While most of these use cases involve periodically extracting metadata from modern data sources, there is a growing need to add near-real-time ingestion and consumption on the platform.

    This has led to a series of problem statements, some of which are outlined below:

      **- **(INBOUND, EXTERNAL)**** : A customer uses Monte Carlo as a tool for data observability. They have set it up so that Monte Carlo catches any table health or data reliability issues early on. The customer would like Atlan to also become a near-real-time repository of such issues, with relevant metadata attached to respective assets.
      **- **(INBOUND, INTERNAL)**** : A prospect has a metadata estate spanning 1B metadata assets. While the bulk of this payload is columns in different tables and BI fields (~90% of total), the remaining 10% consists of assets such as databases, schemas, tables, and dashboards. They want to ingest metadata using Atlan’s metadata extraction with an 80-20 rule, where columns become eventually consistent in the metadata lake.
      **- **(OUTBOUND, INTERNAL)**** : There are internal enrichment automation requirements towards metadata into Atlan, such that any change in the Atlan entity triggers similar changes to entities connected downstream in lineage from that entity.
      **- **(OUTBOUND, EXTERNAL)**** : A customer of Atlan wants to enforce data access security and compliance. They require that as soon as an entity is annotated as PII or GDPR in Atlan, their downstream data tools become aware of it and enforce access control while running SQL queries on the data.

    There are many more use-cases similar in nature, where real-time behavior of the Atlan platform is essential. The Atlan team has realized the importance of supporting such capabilities as part of their platform.

    Your task is to create an architecture that supports the above use cases, . You will need to consider the following aspects as you solve the problem statement:

      - Near-real time nature of the solution
      - Schematics when ingesting and consuming metadata
      - Selecting an appropriate metadata store to work with these capabilities
      - Capability for pre-ingest and post-consume transformations where needed on the metastore
      - Authentication and authorization as first-class citizens in the system
      - Tenancy as a problem statement in mind, given customers range from comfort deploying in a multi-tenant setup, to wanting complete isolation in their setup
      - Deploying the solution in a plug-and-play fashion as more use cases come in
      - Solving for SaaS sources and targets such as Slack, JIRA, MS-Teams, Freshdesk, and Okta
      - Adaptability to inbound and outbound consumers to scale as per the volume of metadata change events hitting the platform
      - Cost of deploying the solution proposed
      - Observability of the platform

    The outcome of this task is to architect a solution that takes care of both functional and non-functional aspects mentioned above, and share a working prototype of 1 inbound and 1 outbound case of ingestion and consumption of metadata, while keeping a professional tone.


**What do we want to solve**

    The core of this problem statement is to design a near real time data ingestion and consumption of metadata,
    such that the system is scalable, near real time, extensible and secure.


**Requirements**

    Note: 
        we'll use short forms here which are as follows:
            1. NRT : near real time
            

    Functional Requirements:
        1. NRT ingestion of metadata
        2. NRT transformation 
        3. NRT enrichment to downstream data
        4. NRT consumption
        5. Metadata registry/Storage 
        6. Tenancy
        7. Data access security : PII, GDPR
        8. Authentication
        9. Authorization    


    Non-functional Requirements:
        1. Extensiblility
        2. Observability


**Research**

    1. Metadata:
        Metadata is data's data. It can be classified as technical, business or operational metadata.
        Wherein, technical metadata: datatype, column, table, schema, server etc
                 business metadata: data domain, line of business, business name etc
                 Operational metadata: data Qc or validation    
        Descriptive metadata includes information about who created a resource, as well as what it is about and what it contains. This is best accomplished through the use of semantic annotation.
        Additional data about the way data elements are organized – their relationships and the structure they exist in – is included in structural metadata.
        Administrative metadata contains information about the origin, type, and access rights of resources.

    2. NRT ingestion of metadata:
        This requirement has 2 parts to it i.e: NRT and ingestion
        In order to handle both of these and the nature of problem where we
        we need to ingest data from multiple different sources,

        Options considered:

            1. Kafka connect:
                ecosystem of pluggable connectors
                data integration system and ecosystem
                Horizontally scalable
                Fault tolerant
                Extensible: Abstraction using json files
                Declarative
                
                Connectors:
                    pluggable software component
                    interfaces to external systems and also to kafka
                    Also exist as runtime entities
                    source connectors act as producers
                    sink connectors act as consumers

            2. Kafka streams:
                A producer produces the data into some topic and there are consumers
                that consume that data from topic. 
                This is not as flexible and pluggable as kafka connect 


    3. NRT transformation and enrichment
        Options considered:
            
            1. Spark Structured Streaming
                Reliable
                Active open source community
                Well tested and used
                Scalable
                High throughput
                Fault tolerant
                NRT
                Batch processing framework
                Microbatching
                Not very efficient memory management
                Requires indepth knowledge to handle above
                can have frequent OOMs
                Uses DAG as execution engine
                Good for heavy transformations
                Basic abstraction is RDD (resilient distributed dataset) : leveraged for fault tolerance
                slower than flink
                more vibrant apis and detailed libraries
                Harder to scale than flink, requires manual optimization
                

            2. Apache flink
                stream processing based on Windowing and checkpointing
                Real time
                fault tolerant (check pointing helps)
                Own efficient automatic memory manager
                OOM error would be rare
                controlled cyclic dependency graph as execution engine
                good for light heavy transformations
                Basic abstraction is dataset and datastream api : leveraged for fault tolerance
                faster recovery time and consistency
                faster than spark (higher data processing speed)
                Lesser apis and libraries in different languages
                Easy to scale due to it's automatic optimization power

            
            3. HMT
            

            4. kafka streams
                
                
                


            Yahoo's benchmark:
                In Yahoo!’s tests, Spark’s results were considerably worse than Flink and Storm’s, going up to 70 sec without back-pressure and 120 sec with back-pressure, compared with less than 1 sec for Flink and Storm, as shown in the following chart (percentile latency depicted for the rate 150K/s):
                Reference in references tab below
                
                
                
                
                
                
                


**Calculations**
        Assumptions:
            1. Metadata is coming from multiple sources
            2. Ingestion qps: ~10kps
            3. Consumption qps: ~9Kps
            4. Transformations are not very heavy
            5. Near real time latency of 5 minutes
            6. 20 transformations on 1 metadata post ingestion at 5 times per hour
            7. Enrichment and transformations can be eventually consistent
            
            

**Components**




**Trade-offs**




**HLD**

    source (cdc) -> kafka connect -> topic -> Cold storage
                                           ->  apache flink -> Elastic search/cosmos



**LLD**



**How to run**



**References**
    <i> https://blog.open-metadata.org/how-we-built-the-ingestion-framework-1af0b6ff5c81 </i>
    <i> https://hevodata.com/learn/metadata-driven-data-ingestion/ </i>
    <i> https://github.com/yahoo/streaming-benchmarks </i>
    <i> https://www.infoq.com/news/2015/12/yahoo-flink-spark-storm/ </i>



**TERMS**
    1. CDC
        change data capture 
        there are 2 types of CDC, query based and log based
        query based: queries like new rows since last updated time are used to capture change in data
                     JDBC source sink connector is a CDC connector for RDBMS
        log based: Transaction logs of DB, can capture updates, inserts and can also tell you about
                    DELETEs. This is not possible with query based CDC







