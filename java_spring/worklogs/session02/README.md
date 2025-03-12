# Session 02 worklog 
## 1) Refactor ITU-MiniTwit to another language and technology of your choice.
### Language choice
Our motivation for choosing a language was primarily learning something new, and/or improving on it, with respect to what we would likely use in the future, during employment in a company. 

We landed on using Java with the Spring framework. Spring provides a web framework that makes it easy to map the functionality from the original python MiniTwit, and it also provides easy integration with Docker for later containerization. It is also VERY commonly used in enterprise applications worldwide and specifically in Denmark, from our own job experience. Therefore using it while practicing DevOps will provide us with skills we will likely need in the future. 

We did not consider benchmarking different frameworks and picking whatever is fastest, since it doesn't align with our motivations for picking the language (or taking the course for that matter). 

### Functionality mapping
We started our refactoring by mapping all the functionality from the original python MiniTwit into a separate document, that we could as a checklist for our new application. The list can be found [here](https://github.com/Magmose/ITU2023-DevOps/tree/dev/worklogs/session02/original_functionality.md).

### Implementation
We first setup the repository for the code according to our git strategy (which we will outline later in this document), and committed a simple web application with a functioning `.../hello` endpoint to the main branch. Afterwards implementation was done according to the checklist.

## Containerization with Docker


## Distributed Workflow and Git Strategy
Insofar as the tasks each week are meant to iterate on this 'refactored' project, we inted to keep the code in a single Git repository. Since we will be developing it as a group with given tasks, we do not see a reason to have separate diverging repositories for each developer, and have multiple remotes. Instead we will make use of branching for developing new features etc, and merge them together when new features are ready, and the branches are healthy. In particular, we will:
1. Keep a single healthy, working, and production-ready branch 'main', from which we will deploy the server in its different versions. 
2. Keep a single branch 'dev' into which each developer will merge their changes (new features, bug fixes, etc). This server will also be deployed on its own, and will be used for testing the new features and changes. 
3. For each new feature, change, bug-fix etc, the developer in charge of it will branch out from 'dev'. Naming convention for the new branches is that the names should be unique, and give a short meaningful description of what the branch is intended to change/fix/whatever. 

The general workflow for a single developer working with the project will be: 
1. Pull the latest changes from the repository
2. Checkout the dev branch of the project
3. Checkout a new branch from 'dev' with a name corresponding to the task at hand
4. Implement the new feature, change, etc. and commit changes. 
5. Merge the branch into 'dev'. 
6. Test the changes by deploying the dev server again (perhaps done automically, perhaps the code is self-tested), perhaps testing is done by another developer
7. If the developer branch is still healthy, and the feature/change works as intended, then merge 'dev' into 'main'. Otherwise go back to step 4. 

This is loosely based on the "Feature Branching" strategy outlined by Fowler [here](https://martinfowler.com/articles/branching-patterns.html).
