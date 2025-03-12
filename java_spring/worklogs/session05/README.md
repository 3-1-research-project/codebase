# Session 05 worklog 
## Introduce a DB abstraction layer in your ITU-MiniTwit


### 1. Flow
We are using the issues feature on Github to document and solve issues that we find. GitHub issues can help facilitate this by providing a centralized location for tracking and managing work items, such as new features, bug fixes, and improvements. 
We also try to divide issues into smaller problems. Breaking down large work items into smaller, more manageable tasks can help achieve flow by making it easier to move work items through the pipeline. It also helps promote collaboration and reduces the risk of delays or reworks by enabling team members to work on tasks in parallel. Making the tasks smaller also helps with the visibility of who is doing what, since if someone is working on a larger task it is difficult to know what the person is currently doing in this task.

### 2. Feedback
Currently we are only using SSH to monitor our system by quereing our database(manual monitoring). However, we are planning on implementing Prometheus and Grafana. For the future together, Prometheus and Grafana will provide a powerful feedback loop that can help us monitor the health and performance of our system in real-time, quickly identify and respond to issues, and continuously improve the system over time. In the immediate future we are going for reactive monitoring, but would like to upgrade to proactive when possible.

### 3. Continual Learning and Experimentation
In our group we have gained two more members. To get them up to speed we first assigned them a task of reading through our current code and try to understand how our application functions. Afterwards we went through their questions and have now assigned them a small task of implementing of some simple new features for the project, and start implementing them in a new branch. Here we thought of a feature where one can save other users’ tweets, and having a page where you can look at all saved tweets
To facilitate knowledge sharing, we encourage our team members to work on location together, even if on different tasks. we also have a teams channel where questions can be asked if someone is not on location, however we still believe on location is better for knowledge sharing.

### Object-relational mapping (ORM)
Although the implementation of this feature has not yet been realized, we plan to employ Spring Data JPA for the purpose of mapping. Presently, the system lacks the Object-Relational Mapping (ORM) framework, but we intend to integrate it in future iterations. Although the ORM framework is absent the system is still fully functional, but do not have the persistence we want. Here are some of the reasons why we opted for this technology.

Easy to use: Spring Data JPA provides a simple and easy-to-use interface for accessing the database. It uses standard JPA annotations to map objects to tables, which makes it easy to use.

Supports multiple databases: Spring Data JPA supports multiple databases, including MySQL, PostgreSQL, Oracle, and others. This means that we can easily switch to a different database in the future.

Integration with Spring Boot: Spring Data JPA integrates seamlessly with Spring Boot (as we a currently using), which makes it easy to configure and use in our application.

Rich feature set: Spring Data JPA provides a rich feature set, including support for caching, pagination, and auditing. This can help improve the performance and scalability.

### DBMS
We have made a decision to utilize a managed MySQL database solution hosted on Digital Ocean as our preferred database management system (DBMS). Below are some key considerations that influenced our choice.

1. Open source: MySQL is an open-source DBMS.

2. Scalability: MySQL is scalable and can handle large amounts of data. It also supports sharding, which allows us to distribute data across multiple servers, that will be needed for future load on our system.

3. Performance: MySQL is known for its high performance and can handle a large number of transactions per second, which is needed in our twitter application.

4. Community support: MySQL has a large and active community of users and developers, which means that we can find plenty of resources and help online.

We have also consindered upon the possibility of using a NoSQL graph database platform, specifically Neo4j, due to its sophisticated search capabilities and algorithmic recommendation engine that facilitates e.g. which user would like another user content. However, given the current time constraints, we have determined that the process of transitioning to this alternative database management system would be to time-consuming. This would require a mapping of the current database to a CSV file and subsequently design a transformer capable of translating it into a suitable Graph data structure.
