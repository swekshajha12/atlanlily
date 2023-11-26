**[Atlanlily](https://atlanhq.notion.site/atlanhq/Atlan-Lily-b08e1aa20972491699b9759a381dbbd3)**

List of contents:



1. [Problem statement](#bookmark=id.g6cuz3ay8q20)
2. [What do we want to solve?](#bookmark=id.92gyconwy5y6)
3. [Requirements](#bookmark=id.syjqief8duaz)
4. [HLD](#bookmark=id.uc0x5usy0y1v)
    1. [Design](#bookmark=id.ho48q4akhsg3)
    2. [Walkthrough](#bookmark=id.6vfmscsvwor6)
5. [Components](#bookmark=id.pyvtdc67kpzx)
    3. [NRT ingestion of metadata](#bookmark=id.59miy5kjkgwu)
        1. [Options Considered](#bookmark=id.shjb1si8l4ke)
        2. [Choice](#bookmark=id.7sj64c9y82ie)
    4. [NRT transformation and enrichment](#bookmark=id.3a1daxihh7bh)
        3. [Options considered](#bookmark=id.5p40q9byh6qu)
        4. [Choice](#bookmark=id.moxcl535lzd1)
    5. [DB](https://docs.google.com/document/d/15u3XmUEFG8pfSP2-Lh7dpqqK-JbSCZHGcq6-gfdrvPE/edit#bookmark=id.cju19lqma8ka)
        5. [Functional and Non functional requirements](#bookmark=id.2czlin4f3zb1)
        6. [Primary Metastore](#bookmark=id.dmyqigzgc09u)
            1. [Functional and Non functional requirement](#bookmark=id.d9m8c1uxu6pb)
            2. [Query pattern](#bookmark=id.nvdsujop4wmp)
            3. [Choice](#bookmark=id.sdhurb4mstyn)
            4. [File format](#bookmark=id.kl76mz7m26os)
        7. [Secondary Metastore](#bookmark=id.4za69l1cbd8)
            5. [Functional and Non functional requirement](#bookmark=id.w58zask95ylr)
            6. [Query pattern](#bookmark=id.vu5hj4yog3ga)
            7. [Options considered](#bookmark=id.51r7aq6i94gx)
            8. [Choice](#bookmark=id.c6b6d6vz7w8q)
    6. [Storage framework](#bookmark=id.r4yhejuhjhbn)
        8. [Why do we need it?](#bookmark=id.z9p75w9az14n)
        9. [Choice](#bookmark=id.lhrirxcyhtuw)
        10. [How does it fit our usecase](#bookmark=id.6cvt2v4ed1yd)
    7. [SQL Engine](#bookmark=id.vcj4w6481gq5)
        11. [Why do we need it?](#bookmark=id.ixz9mpuspgya)
        12. [Options considered](#bookmark=id.qok9ljrr9214)
        13. [Choice](#bookmark=id.q7h7gbnps8x1)
6. [LLD](#bookmark=id.bysszc3xbfkf)
7. [Terms](#bookmark=id.13db5xw6lyla)
8. [References](#bookmark=id.qj21rio61g2d)

**                                             Problem statement**


The Atlan platform has many use cases for ingesting and consuming metadata. While most of these use cases involve periodically extracting metadata from modern data sources, there is a growing need to add near-real-time ingestion and consumption on the platform.


This has led to a series of problem statements, some of which are outlined below:


** (INBOUND, EXTERNAL)** : A customer uses Monte Carlo as a tool for data observability. They have set it up so that Monte Carlo catches any table health or data reliability issues early on. The customer would like Atlan to also become a near-real-time repository of such issues, with relevant metadata attached to respective assets.


**(INBOUND, INTERNAL)** : A prospect has a metadata estate spanning 1B metadata assets. While the bulk of this payload is columns in different tables and BI fields (~90% of total), the remaining 10% consists of assets such as databases, schemas, tables, and dashboards. They want to ingest metadata using Atlan’s metadata extraction with an 80-20 rule, where columns become eventually consistent in the metadata lake.


**(OUTBOUND, INTERNAL)** : There are internal enrichment automation requirements towards metadata into Atlan, such that any change in the Atlan entity triggers similar changes to entities connected downstream in lineage from that entity.


**(OUTBOUND, EXTERNAL)**: A customer of Atlan wants to enforce data access security and compliance. They require that as soon as an entity is annotated as PII or GDPR in Atlan, their downstream data tools become aware of it and enforce access control while running SQL queries on the data.


There are many more use-cases similar in nature, where real-time behavior of the Atlan platform is essential. The Atlan team has realized the importance of supporting such capabilities as part of their platform.


Your task is to create an architecture that supports the above use cases, . You will need to consider the following aspects as you solve the problem statement:

* Near-real time nature of the solution
* Schematics when ingesting and consuming metadata
* Selecting an appropriate metadata store to work with these capabilities
* Capability for pre-ingest and post-consume transformations where needed on the metastore
*  Authentication and authorization as first-class citizens in the system
*  Tenancy as a problem statement in mind, given customers range from comfort deploying in a  multi-tenant setup, to wanting complete isolation in their setup
*  Deploying the solution in a plug-and-play fashion as more use cases come in
*  Solving for SaaS sources and targets such as Slack, JIRA, MS-Teams, Freshdesk, and Okta
*  Adaptability to inbound and outbound consumers to scale as per the volume of metadata change events hitting  the platform
* Cost of deploying the solution proposed
* Observability of the platform

 The outcome of this task is to architect a solution that takes care of both functional and non-functional aspects mentioned above, and share a working prototype of 1 inbound and 1 outbound case of ingestion and consumption of metadata, while keeping a professional tone.


**                                          What do we want to solve**


    The core of this problem statement is to design a near real time data ingestion and consumption of metadata,


    such that the system is scalable, near real time, extensible and secure.


**                                                  Requirements**


    **Functional Requirements:**


        1. NRT ingestion of metadata


        2. NRT transformation 


        3. NRT enrichment to downstream data


        4. NRT consumption


        5. Metadata registry/Storage 


        6. Tenancy


        7. Data access security : PII, GDPR


        8. Authentication


        9. Authorization    


  **  Non-functional Requirements:**


        1. Extensibility


        2. Observability


   


						              


                                                                                     ** HLD**


**For a better view visit: [Excalidraw design link](https://excalidraw.com/#json=d9k_w2IyPC7CysyV_E3pd,CGoNaI0r3oYio3c4N0uGrw)**




<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



**                                                        **


**                                             Walkthrough of HLD**


**	**

1. Using kafka connect’s wide variety of connectors, we connect to different types of data sources. 
2. The CDC data in kafka’s topic is bifurcated along 2 routes:
    1. First is pump and dump, where we send this raw data directly to S3, where it’s stored as parquet files
    2. We also use apache Flink to do pre ingest transformations before writing it to Mongo db.
3. Flink is used to do post consume transformations on top of this data and stored in S3.
4. This data stored in S3  is used by Trino which is an sql engine to power dashboarding and run complex queries and aggregations giving the user near real time behavior. This also supports multiple tenant setup.
5. When the user does any change on the assets using the dashboard, it’s written to a kafka topic, which is then sent to Trino and Mongo db. 
6. Trino writes back the data to S3 which then updates everything on s3 and logs, audits, etc.
7. Non sensitive data is written to Mongo db for eventual consistency in search for light and discreet query patterns

**						**


**                                                Components**


**	**


**                            NRT ingestion of metadata**


This requirement has 2 parts to it i.e: **_NRT and ingestion_**


In order to handle both of these and the nature of problem where we need to ingest data from multiple different   sources, I considered the following options


** Options considered:**


<table>
  <tr>
   <td><strong><em>Kafka connect</em></strong>
   </td>
   <td><strong><em>Kafka streams</em></strong>
   </td>
  </tr>
  <tr>
   <td>Good Ecosystem of pluggable connectors
   </td>
   <td>It is a distributed messaging system
   </td>
  </tr>
  <tr>
   <td>Data integration system and ecosystem: 
<p>
<strong>Data-centric pipeline</strong>: Connect uses   meaningful data abstractions to pull or push data to Kafka.
   </td>
   <td> Used more for event/data streaming and processing. 
   </td>
  </tr>
  <tr>
   <td>Horizontally scalable:
<p>
<strong>Flexibility and scalability</strong>: Connect runs with streaming and batch-oriented systems on a single node (standalone) or scaled to an organization-wide service (distributed).
   </td>
   <td>Horizontally scalable, flexible and scalable
   </td>
  </tr>
  <tr>
   <td>Fault tolerant
   </td>
   <td>Fault tolerant
   </td>
  </tr>
  <tr>
   <td><strong>Reusability and extensibility</strong>: leverages existing connectors or extends them to fit your needs and provides lower time to production.
   </td>
   <td><strong>Not extensible</strong>: It is an API for writing client applications that transform data in Apache Kafka. You usually do this by publishing the transformed data onto a new topic. The data processing itself happens within your client application, not on a Kafka broker.
   </td>
  </tr>
  <tr>
   <td>Open source 
   </td>
   <td>Open source
   </td>
  </tr>
  <tr>
   <td>Works on source-> sink concept
   </td>
   <td>Works on producer &lt;– consumer concept
   </td>
  </tr>
  <tr>
   <td>Fast
   </td>
   <td>Fast
   </td>
  </tr>
</table>



               


**Choice: KAFKA CONNECT**


**Kafka Connect** can ingest entire databases or collect metrics from all your application servers into Kafka topics, making the data available for stream processing with low latency. An export connector can deliver data from Kafka topics into secondary indexes like Elasticsearch, or into batch systems–such as Hadoop for offline analysis.


Its ecosystem of connectors gives the extensibility to connect to different types of dbs and systems (RDBMS, ORACLE, POSTGRES, MYSQL, MESSAGE QUEUES etc  ) to capture data, is easy to deploy and integrate with external systems. Scalability and fault tolerance are another reason that this should be used over kafka streams.


The use case for kafka streams is more on the side of producing data in a topic, then writing a consumer to process that data according to application logic which doesn’t fit our use case. And even if we were to use kafka streams, it wouldn't be as flexible and extensible to connect with different external systems as kafka connect.


           


**                                            NRT transformation and enrichment**


**Options considered**


<table>
  <tr>
   <td><strong>Kafka streams</strong>
   </td>
   <td><strong>Apache Flink</strong>
   </td>
   <td><strong>Apache spark</strong>
   </td>
   <td><strong>ksqlDB</strong>
   </td>
  </tr>
  <tr>
   <td>Real time
   </td>
   <td>Real time
   </td>
   <td>Near real time
   </td>
   <td>Near real time
   </td>
  </tr>
  <tr>
   <td>Smaller community
   </td>
   <td>Smaller community
   </td>
   <td>Big community
   </td>
   <td>Smaller community
   </td>
  </tr>
  <tr>
   <td>Support for scala, java, python 
   </td>
   <td>Support for scala, java, python, sql
   </td>
   <td>Support for scala, R, java, python, sql etc
   </td>
   <td>Support for sql
   </td>
  </tr>
  <tr>
   <td>Low latency, high throughput
   </td>
   <td>Low latency, high throughput
   </td>
   <td>High latency, low throughput
   </td>
   <td>Low latency, high throughput
   </td>
  </tr>
  <tr>
   <td>No inbuilt support for advanced stream processing features like windowing, aggregation or state management
   </td>
   <td>Inbuilt support for advanced stream processing features like windowing, aggregation and state management
   </td>
   <td>Inbuilt support for advanced stream processing features like windowing, aggregation and state management
   </td>
   <td>Inbuilt support for advanced stream processing features like windowing, aggregation and state management
   </td>
  </tr>
  <tr>
   <td>No guarantee of order of messages
   </td>
   <td>Guarantee of order of messages
   </td>
   <td>Guarantee of order of messages
   </td>
   <td>No guarantee of order of messages
   </td>
  </tr>
  <tr>
   <td>No support for batch processing
   </td>
   <td>Support for batch processing
   </td>
   <td>Support for batch processing
   </td>
   <td>No Support for batch/micro batch processing
   </td>
  </tr>
  <tr>
   <td>inefficient with long-running or high-cardinality aggregation
   </td>
   <td>efficient with long-running or high-cardinality aggregation
   </td>
   <td>efficient with long-running or high-cardinality aggregation
   </td>
   <td>inefficient with long-running or high-cardinality aggregation
   </td>
  </tr>
  <tr>
   <td>Exactly once delivery
   </td>
   <td>Exactly once delivery
   </td>
   <td>Exactly once delivery
   </td>
   <td>Exactly once delivery
   </td>
  </tr>
  <tr>
   <td>High availability
   </td>
   <td>High availability
   </td>
   <td>High availability
   </td>
   <td>High availability
   </td>
  </tr>
  <tr>
   <td>Fault tolerant
   </td>
   <td>Fault tolerant
   </td>
   <td>Fault tolerant
   </td>
   <td>Fault tolerant
   </td>
  </tr>
  <tr>
   <td>Horizontally Scalable
   </td>
   <td>Horizontally Scalable
   </td>
   <td>Horizontally Scalable
   </td>
   <td>Horizontally Scalable
   </td>
  </tr>
  <tr>
   <td>Lower learning curve, easy to adopt
   </td>
   <td>Slightly higher learning curve, 
   </td>
   <td>Slightly higher learning curve
   </td>
   <td>Lower learning curve, easier to adopt
   </td>
  </tr>
  <tr>
   <td>Excellent analytics capabilities
   </td>
   <td>Excellent analytics capabilities
   </td>
   <td>Excellent analytics capabilities
   </td>
   <td>Excellent analytics capabilities
   </td>
  </tr>
  <tr>
   <td>Streaming processing
   </td>
   <td>Streaming + batch processing
   </td>
   <td>batch/micro batch processing
   </td>
   <td>Streaming processing
   </td>
  </tr>
  <tr>
   <td>NA
   </td>
   <td>Better support for  windowing and state management
   </td>
   <td>Less
   </td>
   <td>NA
   </td>
  </tr>
  <tr>
   <td>NA
   </td>
   <td>NA
   </td>
   <td>Can have frequent OOMs
   </td>
   <td>NA
   </td>
  </tr>
  <tr>
   <td>Easier to scale
   </td>
   <td>Easier to scale
   </td>
   <td>Harder to scale
   </td>
   <td>Easier to scale
   </td>
  </tr>
</table>



                


                


                


Note:


**_Yahoo's benchmark:_**


**_Yahoo!’s tests, Spark’s results were considerably worse than Flink and Storm’s, going up to 70 sec without back-pressure and 120 sec with back-pressure, compared with less than 1 sec for Flink and Storm, as shown in the following chart (percentile latency depicted for the rate 150K/s):_**


**_Reference in references tab below_**


                


**CHOICE: FLINK**


**	**


There were many more streaming technologies like storm, aws glue etc but these 4 seemed good options to me given their adoption, development, community, speed and features.


Out of these, my final choices were **Flink **and** ksqlDB **as both of them provide **_real time processing_**, are **_easy to set up_**, **_scalable_** and have many other features which fit our use case. **_The deciding factors were_**:



1. **_ksqlDB_** isn't well-suited for the complex transformations needed for feature engineering whereas Flink has extensive inbuilt support for complex transformations and is fast.
2. **_ksqlDB_** is inefficient with long-running or high-cardinality aggregation. Routing, filtering, and running basic transformations over streaming data are the strengths of **_ksqlDB_**, and while it can perform some aggregations, it will suffer under [more complex scenarios](https://www.jesse-anderson.com/2019/10/why-i-recommend-my-clients-not-use-ksql-and-kafka-streams/#:~:text=Solved%20right%3F%20No,the%20current%20time.) requiring large amounts of state which is not the case with **_flink._** 
3. **_ksqlDB_** is easier to set up but its native support for sql can be a big limiting factor in adoption and expressing every processing logic in SQL can prove to be a challenge whereas **_flink_** provides support for sql, python, java and scala. 
4. **_Flink_** provides both real time processing as well as batch processing which can be executed on a use case basis. This is not there in **_ksqlDB ._**

**                                                              **


**                                                                     DataBase**


**Functional requirements:**



1. Data storage
2. Querying capabilities
3. Transformations
4. Data lineage
5. Security compliant
6. Near real time

**Non functional Requirements:**



1. Cost efficient
2. Scalable
3. Reliable
4. Easy to maintain
5. High availability

We’ll be using 2 datastores here, 

* **_data lake_**: which would support heavy queries, transformations, data security compliance, audit, serve as a store for all time data
*  **secondary data store** for keeping recent data and support for light querying in real time

**                                                         Primary metastore**


Instead of NoSQL or SQL based databases, I decided to go for a filesystem based db because of our requirement to


Store data and metadata of all time and provide transformations and querying capability on top. Also our use case required us to have a data lake and a s3 type of storage would be apt for this.


**Functional requirement:**

1. Store all time data
2. Audit
3. Security
4. Complex queries 
5. Complex transformations (joins, aggregations)
6. Near real time

**Non-functional requirement:**

1. Scalable
2. Cost efficient
3. Fault tolerant

**Query pattern:**


SELECT

    u.user_id,

    u.gender,

    COUNT(*) as rating_count

FROM

    user_ratings u

WHERE

    u.rating = 3

    AND u.timestamp >= DATE_SUB(NOW(), INTERVAL 6 MONTH)

GROUP BY

    u.user_id, u.gender;


**	**


**	**


**Choice: AWS S3**


S3 fulfills most of our requirement like:


                                                        	



*  High availability,
*  low latency
* Managed deployment
* Cost effective
* Reliable, fault tolerant    
* Cost analysis: 	~$1000/month for 50TB/month
    * Ref: [link](https://aws.amazon.com/s3/pricing/?p=pm&c=s3&z=4)

Although the cost of other similar storage like gcs, azure blog storage is similar and is subject to existing cloud infra


If there is already some cloud setup, then options can be weighed accordingly.


**File format: Avro/parquet**


Avro and Parquet understand the schema of the data they store. When you write a file in these formats, you need to specify your schema. When you read the file back, it tells you the schema of the data stored within. This is super useful for a framework like Spark/flink, which can use this information to give you a fully formed data-frame with minimal effort.


**                                             Secondary Metastore**


**	Functional requirement:**

1. Real time 
2. Recent data storage
3. Unstructured data
4. Low latency
5. Querying 

**Non-functional requirement:**

1. Scalable
2. Reliable
3. Fault tolerant

**Query pattern:**


    SELECT


        user_id,


        rating,


        timestamp


    FROM


        user_ratings


    WHERE


        user_id = 123


    ORDER BY


        timestamp DESC


    LIMIT 1;


**_Why do we need a secondary metastore?_**


			


We need a secondary metastore because we also have the requirement to make the ingested data  available to                      users in real time which can handle light to medium queries on the recent data. 


**OPTIONS**


**           **


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Elastic search</strong>
   </td>
   <td><strong>Mongo db</strong>
   </td>
   <td><strong>Cosmos DB</strong>
   </td>
   <td><strong>Postgresql</strong>
   </td>
   <td><strong>Cassandra</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Type</strong>
   </td>
   <td>
<strong>Search and Analytics</strong>
<p>

<strong>Engine</strong>
   </td>
   <td>
<strong>NoSQL </strong>
<p>

<strong>Document </strong>
<p>

<strong>Database</strong>
   </td>
   <td>
<strong>Globally Distributed Multi-Model Database Service</strong>
   </td>
   <td>
<strong>Relational Database </strong>
<p>

<strong>Management</strong>
<p>

<strong>System (RDBMS)</strong>
   </td>
   <td><strong>Wide-Column Store NoSQL Database</strong>
   </td>
  </tr>
  <tr>
   <td>
<strong>Data Model</strong>
   </td>
   <td>
<strong>Document</strong>
   </td>
   <td>
<strong>Document</strong>
   </td>
   <td><strong>Multi-Model (Document, Graph, Key-Value, Table)</strong>
   </td>
   <td>
<strong>Relational (Table)</strong>
   </td>
   <td><strong>Wide-Column Store NoSQL Database</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Query Language</strong>
   </td>
   <td><strong>Elasticsearch Query DSL</strong>
   </td>
   <td><strong>JSON-like Query Language</strong>
   </td>
   <td>
<strong>SQL, MongoDB, </strong>
<p>

<strong>Cassandra, gremlin</strong>
   </td>
   <td><strong>SQL</strong>
   </td>
   <td>
<strong>CQL</strong>
<p>

<strong> (Cassandra Query</strong>
   </td>
  </tr>
  <tr>
   <td>
<strong>Scalability</strong>
   </td>
   <td>
<strong>Horizontal Scaling</strong>
   </td>
   <td>
<strong>Horizontal Scaling</strong>
   </td>
   <td>
<strong>Automatic and </strong>
<p>

<strong>Instant scalability</strong>
   </td>
   <td>
<strong>Horizontal Scaling</strong>
   </td>
   <td>
<strong>Horizontal Scaling</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Consistency model</strong>
   </td>
   <td>
<strong>Eventual Consistency</strong>
   </td>
   <td>
<strong>Eventual Consistency</strong>
   </td>
   <td><strong>Multiple Consistency Models (Strong, Bounded, Eventual)</strong>
   </td>
   <td>
<strong>ACID </strong>
<p>

<strong>(Strong Consistency)</strong>
   </td>
   <td>
<strong>Eventual Consistency</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Global Distribution</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>Yes</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>Yes</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Multi-Model Support</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>Yes</strong>
   </td>
   <td>
<strong>No</strong>
   </td>
   <td>
<strong>Yes</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Data types</strong>
   </td>
   <td>
<strong>Dynamic</strong>
   </td>
   <td>
<strong>Dynamic</strong>
   </td>
   <td>
<strong>Dynamic</strong>
   </td>
   <td><strong>static</strong>
   </td>
   <td>
<strong>Dynamic</strong>
   </td>
  </tr>
  <tr>
   <td>
<strong>Use Cases</strong>
   </td>
   <td><strong>Full-Text Search, Real-Time Analytics</strong>
   </td>
   <td><strong>Content Management, Catalogs, Real-Time Big Data</strong>
   </td>
   <td><strong>Global Applications, Multi-Model Support</strong>
   </td>
   <td><strong>Transactional Applications, Data Warehousing</strong>
   </td>
   <td><strong>Time-Series Data, High Write Throughput</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Ecosystem Integration</strong>
   </td>
   <td>
<strong>Limited</strong>
   </td>
   <td>
<strong>Limited</strong>
   </td>
   <td><strong>Azure Ecosystem Integration</strong>
   </td>
   <td><strong>Extensive Community Ecosystem</strong>
   </td>
   <td>
<strong>Limited</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Community Support</strong>
   </td>
   <td>
<strong>Good</strong>
   </td>
   <td>
<strong>Good</strong>
   </td>
   <td>
<strong>Good</strong>
   </td>
   <td>
<strong>Excellent</strong>
   </td>
   <td>
<strong>Good</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Fault tolerance</strong>
   </td>
   <td><strong>Yes</strong>
   </td>
   <td><strong>Yes</strong>
   </td>
   <td><strong>Yes</strong>
   </td>
   <td><strong>Yes</strong>
   </td>
   <td><strong>Yes</strong>
   </td>
  </tr>
</table>



**	**Initially, the main options in my head were **cassandra + elastic search, cosmos db and mongo db**


**Choice: Mongo db (M40)**	


Mongo db fits our functional as well as non functional requirements and is easy to maintain, operate and scale. It also fits the query pattern that we need in real time.


**                                                        Storage framework**


**Why do we need it?**


A storage framework is a storage layer designed to run on top of an existing data lake and improve its reliability, security, and performance. In most cases they support ACID  transactions, scalable metadata, unified streaming, and batch data processing among other features.


There are multiple such platforms in the market like delta lake, apache hudi etc but due to its ease of setup with S3 and certain features as per our requirements as I’ll explain below, I decided to use **delta lake.**


**Choice: Delta Lake**


It is a unified data management system for handling transactional real-time and batch big data, by extending Parquet data files with a file-based transaction log for ACID transactions and scalable metadata handling.




<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")



**Why Delta lake and how does it fit in our requirement:**



1. **ACID Transactions:** 
    1. Protect your data with serializability, the strongest level of isolation
    2. The beauty of ACID transactions is that users can trust the data that is stored in Delta Lake. A data analyst making use of Delta Lake tables to perform ETL on his or her data to ready it for dashboarding can count on the fact that the KPIs he or she is seeing represent the actual state of the data.
2. **Scalable Metadata**: Handle petabyte-scale tables with billions of partitions and files with ease
3. **Time Travel**: Access/revert to earlier versions of data for audits, rollbacks, or reproduce
4. **Open Source**: Community driven, open standards, open protocol, open discussions
5. **Unified Batch/Streaming**: Exactly once semantics ingestion to backfill to interactive queries
6. **Schema Evolution / Enforcement**: 
    3. Prevent bad data from causing data corruption
    4. Allows you to make automatic changes to a table schema as well as support merge, update and delete operation.
7. **Audit History**: Delta Lake log all change details providing a fill audit trail, data versioning
8. **DML Operations**: SQL, Scala/Java and Python APIs to merge, update and delete datasets
9. **Open format : **Since it access parquet files, it’s language agnostic
10.  **GDPR and CCPA compliance:** Compliance often requires point deletes, or deleting individual records within a large collection of data. Delta Lake speeds up point deletions in large data lakes with ACID transactions, allowing you to locate and remove personally identifiable information (PII) in response to consumer GDPR or CCPA requests.

**                                                     SQL Engine**

**Why SQL Engine:**

	**Requirements:**



1. Multi tenant setup
1. Quick access to data lake
2. Standard sql interface
3. Process massive amounts of data from different sources  such as user logs and clickstream data
4. Real time
5. Scalable

Options considered:


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Presto (and Trino)</strong>
   </td>
   <td><strong>Druid</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Query Processing</strong>
   </td>
   <td>Distributed SQL queries
   </td>
   <td>Specialized for real-time analytics
   </td>
  </tr>
  <tr>
   <td><strong>Data Model</strong>
   </td>
   <td>General-purpose, supports various data models
   </td>
   <td>Specialized for columnar storage, time-series
   </td>
  </tr>
  <tr>
   <td><strong>Latency</strong>
   </td>
   <td>Low-latency interactive queries
   </td>
   <td>Optimized for real-time analytics
   </td>
  </tr>
  <tr>
   <td><strong>Use Cases</strong>
   </td>
   <td>Ad-hoc analytics, interactive queries
   </td>
   <td>Real-time analytics, time-series data
   </td>
  </tr>
  <tr>
   <td><strong>Connector Architecture</strong>
   </td>
   <td>Supports a wide range of connectors
   </td>
   <td>Built-in support for various data sources
   </td>
  </tr>
  <tr>
   <td><strong>Performance</strong>
   </td>
   <td>High-performance for interactive and ad-hoc queries
   </td>
   <td>Efficient for real-time analytics
   </td>
  </tr>
  <tr>
   <td><strong>SQL Support</strong>
   </td>
   <td>ANSI SQL compliant
   </td>
   <td>SQL-like querying with extensions
   </td>
  </tr>
  <tr>
   <td><strong>Community</strong>
   </td>
   <td>Active open-source community
   </td>
   <td>Active open-source community
   </td>
  </tr>
  <tr>
   <td><strong>In-Memory Storage</strong>
   </td>
   <td>Limited in-memory storage (depends on the query)
   </td>
   <td>Uses in-memory storage to accelerate queries
   </td>
  </tr>
  <tr>
   <td><strong>Data Ingestion</strong>
   </td>
   <td>Supports data ingestion from various sources
   </td>
   <td>Built-in support for data ingestion
   </td>
  </tr>
</table>


**Choice: Trino**

Out of these, I decided to use Trino because of the following reasons:



1. Open source
2. Parallel processing sql query engine
3. Designed for analytics over large distributed datasets (object storage, databases etc)
4. Highly performant
5. Support for numerous connectors
6. Rich ecosystem of integrations and tools to use
7. Easy to deploy
8. Embedded query engine in data platform for analytics and data processing workloads
9. Central access point for reporting, dashboarding, and analytics of all connected sources     

**There are **connectors available using which we can connect **Trino** to delta lake and power our **dashboard’s querying capabilities ** on huge amounts of data which is **reliable, near real time** and also use the connector to [INSERT](https://trino.io/docs/current/sql/insert.html), [DELETE](https://trino.io/docs/current/sql/delete.html), [UPDATE](https://trino.io/docs/current/sql/update.html), and [MERGE](https://trino.io/docs/current/sql/merge.html) data in Delta Lake tables depending on user activity.


Trino also supports **_multi-tenant setup_** which is a requirement on our side


                                                 **LLD**


Let’s take the use case of user reviews and user as our metadata and data 


Note that this is not exhaustive.



#### 1. Data/metadata Ingestion (Kafka Producer):



* Class: KafkaProducerService
* Responsibilities:
    * Connect to the Kafka broker.
    * Produce user review data to the specified Kafka topic.
* Methods:
    * connect_to_kafka_broker(): Establish a connection to the Kafka broker.
    * produce_data(data): Produce user review data to the Kafka topic.


#### 2. User Review Transformation (Flink Job):



* Class: FlinkUserReviewTransformationJob
* Responsibilities:
    * Consume user review data from the Kafka topic.
    * Apply light transformations using Flink.
    * Produce transformed data to a new Kafka topic or output stream.
* Methods:
    * consume_from_kafka_topic(): Consume user review data from the Kafka topic.
    * apply_transformations(data): Apply Flink transformations.
    * produce_transformed_data(data): Produce transformed data to a new Kafka topic or output stream.


#### 3. Data Storage (Parquet Files):



* Class: ParquetFileStorageService
* Responsibilities:
    * Receive transformed data from Flink.
    * Store data in local Parquet files.
* Methods:
    * store_data(data): Store transformed data in local Parquet files.


#### 4. Docker Configuration:



* File: docker-compose.yml
* Services:
    * kafka-broker: Represents the Kafka broker.
    * flink-taskmanager: Represents the Flink task manager.
    * my-onion-app: Represents the main application.
    * local-db: Represents the local database service.


#### 5. Communication Flow:



* User Review Ingestion:
    * KafkaProducerService connects to the Kafka broker and produces user review data to the specified topic.
* User Review Transformation:
    * FlinkUserReviewTransformationJob consumes data from the Kafka topic.
    * Applies light transformations using Flink.
    * Produces transformed data to a new Kafka topic or output stream.
* Data Storage:
    * ParquetFileStorageService receives transformed data from Flink.
    * Stores data in local Parquet files.


#### 6. Dependencies:



* confluent_kafka: Python library for Kafka integration.
* apache-flink: Flink libraries for Python.
* pyarrow: Python library for Parquet file handling.


#### 7. Error Handling:



* Logging and error handling mechanisms should be implemented in each component.
* Implement retries for Kafka and Flink operations to handle transient errors.
* Define strategies for handling schema evolution in Parquet files.


#### 8. Scalability:



* Kafka and Flink can be scaled horizontally to handle increased data loads.
* Consider partitioning strategies for Kafka topics.
    * Desired Throughput/partition speed


#### 9. Security:



* Implement secure communication between components (e.g., SSL for Kafka).
* Set up authentication and authorization mechanisms.


#### 10. Testing Strategy:



* Unit tests for individual components.
* Integration tests for the entire data pipeline.
* Consider testing against mock Kafka and Flink environments.


#### 11. Deployment:



* Use Docker Compose for deploying the entire application.
* Configuration files should be externalized for easy environment-specific adjustments.


#### 12. Monitoring and Observability:



* Implement logging for each component.
* Use tools like Prometheus and Grafana for monitoring Flink.
* Set up Kafka monitoring tools.

**TERMS**


    1. **CDC**


        change data capture 


        there are 2 types of CDC, query based and log based


        query based: queries like new rows since last updated time are used to capture change in data


        log based: Transaction logs of DB, can capture updates, inserts and can also tell you about


        DELETEs. This is not possible with query based CDC


2.** Metadata:**


        Metadata is data's data. It can be classified as technical, business or operational metadata.


        Wherein, technical metadata: datatype, column, table, schema, server etc 


        business metadata: data domain, line of business, business name etc


        Operational metadata: data Qc or validation    


        Descriptive metadata includes information about who created a resource, as well as what it is about and what it   


        contains. This is best accomplished through the use of semantic annotation.


        Additional data about the way data elements are organized – their relationships and the structure they exist in –          is included in structural metadata.


        Administrative metadata contains information about the origin, type, and access rights of resources.


**References**

*  [https://blog.open-metadata.org/how-we-built-the-ingestion-framework-1af0b6ff5c81](https://blog.open-metadata.org/how-we-built-the-ingestion-framework-1af0b6ff5c81)
*  [https://hevodata.com/learn/metadata-driven-data-ingestion/](https://hevodata.com/learn/metadata-driven-data-ingestion/)
*  [https://github.com/yahoo/streaming-benchmarks](https://github.com/yahoo/streaming-benchmarks)
*  [https://www.infoq.com/news/2015/12/yahoo-flink-spark-storm/](https://www.infoq.com/news/2015/12/yahoo-flink-spark-storm/)
*  [https://redpanda-data.medium.com/comparing-ksqldb-spark-sql-and-flink-sql-b4e495dc34fd](https://redpanda-data.medium.com/comparing-ksqldb-spark-sql-and-flink-sql-b4e495dc34fd)
*  [https://towardsdev.com/creating-a-realtime-cdc-pipeline-with-kafka-spark-14c9883ebf81](https://towardsdev.com/creating-a-realtime-cdc-pipeline-with-kafka-spark-14c9883ebf81)
*  [https://www.xomnia.com/post/why-you-should-dive-into-delta-lake/](https://www.xomnia.com/post/why-you-should-dive-into-delta-lake/)
*  [https://hudi.apache.org](https://hudi.apache.org)
* [https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison?utm_source=linkedin&utm_medium=cpc&utm_campaign=li-hudi-iceberg-delta&li_fat_id=4192b709-7a61-4177-9250-5e6c063648fb](https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison?utm_source=linkedin&utm_medium=cpc&utm_campaign=li-hudi-iceberg-delta&li_fat_id=4192b709-7a61-4177-9250-5e6c063648fb)
*  [https://www.chaossearch.io/blog/how-to-integrate-bi-data-visualization-tools-data-lake](https://www.chaossearch.io/blog/how-to-integrate-bi-data-visualization-tools-data-lake)
* [https://docs.confluent.io/platform/current/connect/index.html](https://docs.confluent.io/platform/current/connect/index.html)
* [https://www.confluent.io/blog/ksqldb-architecture-and-advanced-features/](https://www.confluent.io/blog/ksqldb-architecture-and-advanced-features/)
* [https://www.montecarlodata.com/blog-top-data-lake-vendors/](https://www.montecarlodata.com/blog-top-data-lake-vendors/)
* [https://docs.delta.io/latest/delta-storage.html](https://docs.delta.io/latest/delta-storage.html)
* [https://db-engines.com/en/system/Apache+Druid%3BSnowflake%3BTrino](https://db-engines.com/en/system/Apache+Druid%3BSnowflake%3BTrino)
* [https://trino.io/docs/current/connector/delta-lake.html](https://trino.io/docs/current/connector/delta-lake.html)
* [https://docs.confluent.io/operator/current/co-loadbalancers.html#:~:text=External%20access%20to%20Kafka%20using,to%20produce%20or%20consume%20data.](https://docs.confluent.io/operator/current/co-loadbalancers.html#:~:text=External%20access%20to%20Kafka%20using,to%20produce%20or%20consume%20data.)
* [https://trino.io/Presto_SQL_on_Everything.pdf](https://trino.io/Presto_SQL_on_Everything.pdf)

			 


	
