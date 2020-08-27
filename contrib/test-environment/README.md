# Docker Compose Test Environemnt

When using this test environment you need to have a directory layout like this ...

```
somewhere/birdplan
somewhere/python-nsnetsim
somewhere/python-birdclient
```

From there you can `cd` into `somewhere/birdplan/contrib/test-environment`.

# Running all tests

To run all tests use the following command...
```bash
docker-compose run birdplan /root/runtest
```

# Running a single test set

To run a single test set use the following command...
```bash
docker-compose run birdplan /root/runtest tests/40-bgp/redistribute_connected
```