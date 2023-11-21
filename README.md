# atlanlily

**Problem statement**

    The Atlan platform has many use cases for ingesting and consuming metadata. While most of these use cases involve periodically extracting metadata from modern data sources, there is a growing need to add near-real-time ingestion and consumption on the platform.

    This has led to a series of problem statements, some of which are outlined below:

      - **(INBOUND, EXTERNAL)** : A customer uses Monte Carlo as a tool for data observability. They have set it up so that Monte Carlo catches any table health or data reliability issues early on. The customer would like Atlan to also become a near-real-time repository of such issues, with relevant metadata attached to respective assets.
      - **(INBOUND, INTERNAL)** : A prospect has a metadata estate spanning 1B metadata assets. While the bulk of this payload is columns in different tables and BI fields (~90% of total), the remaining 10% consists of assets such as databases, schemas, tables, and dashboards. They want to ingest metadata using Atlan’s metadata extraction with an 80-20 rule, where columns become eventually consistent in the metadata lake.
      - **(OUTBOUND, INTERNAL)** : There are internal enrichment automation requirements towards metadata into Atlan, such that any change in the Atlan entity triggers similar changes to entities connected downstream in lineage from that entity.
      - **(OUTBOUND, EXTERNAL)** : A customer of Atlan wants to enforce data access security and compliance. They require that as soon as an entity is annotated as PII or GDPR in Atlan, their downstream data tools become aware of it and enforce access control while running SQL queries on the data.

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
        5. Storage
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

    2. NRT ingestion of metadata:
        
                    

**Calculations**


**Components**


**Trade-offs**


**HLD**


**LLD**


**How to run**


**References**







