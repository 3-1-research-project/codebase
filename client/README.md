# Client Code

TODO:

## Container

A container for running the clients are pushed to the [GitHub Organization 3-1 Container Registry (called packages)](https://github.com/orgs/3-1-research-project/packages), and it is called `3-1-research-project/client:<insert version number>`

To run a container use the command below and update the port used. Make sure the `<port>` is the same. Also remember to change `<client-x>`, and `<version number>`

```bash
docker run --rm --detach --name <client-x> --env PORT=<port> --publish <port>:<port> 3-1-research-project/client:<version number>
```
