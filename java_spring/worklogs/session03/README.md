# Session 03 worklog
## Arguments for the choice of virtualization techniques and deployment targets.

We chose to use DigitalOcean as a platform to deploy our server to as you get 200 free credits to host managed service and servers.

As students our budgets are a big concern and therefore DigitalOcean seemed like a solid choice for the purpose of this course.However, it also offers high-performance hardware, fast SSD storage, and a reliable network infrastructure, ensuring that our server can handle high traffic and provide a smooth user experience. Additionally security is a crucial aspect of any web application. By using DigitalOcean's built-in security features such as firewalls, SSH keys, and two-factor authentication, we can ensure that our server is protected against unauthorized access and potential cyber threats

We also chose Vagrant as our virtualization technique as it allows for easily reproduceable environments - both for creating develoment and production environments. In addition it's allowing us to test and deploy the server without worrying about potential conflicts or dependencies as Vagrant takes care of that for us. We combined Vagrant with Docker, a platform for containerizing applications, to streamline deployment and management, as well as to ensure consistency across environments.

In DigitalOcean we have also turned on a Reserved IP address which we can assign a Droplet and then reassign to another Droplet later, as needed. This also allows us to build a failover mechanism with reserved IPs to build a high availability infrastructure for our service. 

Overall, DigitalOcean, Vagrant, and Docker provide a flexible, scalable, and secure solution for hosting our server, while also optimizing our deployment and management processes.
