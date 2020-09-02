# Docker Compose Test Environemnt

When using this test environment you need to have a directory layout like this ...

```
somewhere/birdplan
somewhere/python-nsnetsim
somewhere/python-birdclient
```

Which can be created using...
```
cd somewhere
git clone https://oscdev.io/software/birdplan.git
git clone https://oscdev.io/software/nsnetsim.git python-nsnetsim
git clone https://oscdev.io/software/birdclient.git python-birdclient
```

From there you can `cd` into `somewhere/birdplan/contrib/test-environment`.

# Running all tests

To run all tests use the following command...
```bash
docker-compose run --rm birdplan /root/runtest
```

# Running a single test set

To run a single test set use the following command...
```bash
docker-compose run --rm birdplan /root/runtest tests/40-bgp/redistribute_connected
```

# Increasing verbosity

To increase verbosity to get addtional report data you can use the below examples.

For output of logs...
```bash
 docker-compose run --rm birdplan /root/runtest "-v tests/40-bgp/features/quarantine"
```

For logs and configurations...
```bash
docker-compose run --rm birdplan /root/runtest "-vv tests/40-bgp/features/quarantine"
```

