# Session 04 worklog

### Choice of CI/CD system, i.e., why do you choose your solution instead of any other?

We have choosen Github Actions with a YAML file for configuration and Docker for containerization, here are some of the reasons why we opted for these:

1. Tight Integration with Github: Github Actions is natively integrated with Github, making it easier to automate workflows and manage code in a single place.

2. Easy Configuration with YAML: Github Actions allows to define, build and deployment workflows using a simple YAML file, which makes it easy to understand and maintain our pipeline.

3. Containerization with Docker: Docker is a popular containerization platform that allows us to package our application and its dependencies into a portable container, which can then be deployed to any environment - currently to Digital Ocean.

4. Wide Range of Supported Platforms and Environments: Github Actions supports a wide range of platforms and environments, including Linux, macOS, and Windows, as well as cloud services such as AWS, Azure, and Google Cloud, if we want to migrate in the furture.

5. Community Support: Github Actions has a large and active community of developers, who share their workflows and best practices on Github.

### Secrets
Currently we're also using github secrets, that integrates with the Github Actions. This way we can store secrets that the pipeline requires, in our organazation so that it can be updated on the fly.