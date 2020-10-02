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
docker-compose run --rm birdplan /root/runtest tests/t40_bgp/t10_basic/peertype_customer/test_bgp.py
```

# Increasing verbosity

To increase verbosity to get addtional report data you can use the below examples.

For output of logs...
```bash
 docker-compose run --rm birdplan /root/runtest "-v tests/t40_bgp/t10_basic"
```

For logs and configurations...
```bash
docker-compose run --rm birdplan /root/runtest "-vv tests/t40_bgp/t10_basic"
```

# Writing out expected results

To write out the expected results files, one can use the below ...
```bash
 docker-compose run --rm birdplan /root/runtest "-v tests/t40_bgp/t10_basic --write-expected"
 chown -R user:group tests/t40_bgp/t10_basic
 find tests/t40_bgp/t10_basic -name "*.py" | xargs black
```