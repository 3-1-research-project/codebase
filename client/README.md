# Client Code

TODO:

## Container

A container for running the clients are pushed to the [GitHub Organization 3-1 Container Registry (called packages)](https://github.com/orgs/3-1-research-project/packages), and it is called `3-1-research-project/client:<insert version number>`

To run a container use the command below and update the port used. Make sure the `<port>` is the same. Also remember to change `<client-x>`, and `<version number>`

```bash
docker run --name <client-x> --detach --env PORT=<port> --publish <port>:<port> 3-1-research-project/client:<version number>
```

### How to limit the amount of CPUs used

If you want to limit the container to use 1 specific cpu, you can specify it as below

```bash
docker run --name <client-x> --env PORT=<port> --publish <port>:<port> --cpuset-cpus="<core number>" 3-1-research-project/client:<version number>
```

Where `<core number>` is the specific core you want to limit to. Note, it is a 0 indexed list meaning if a CPU has 4 cores the possible values are 0, 1, 2, and 3.
