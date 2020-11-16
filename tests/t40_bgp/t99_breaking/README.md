# Testing BIRD breaking point


e1 (upstream) will send routes to r1 which will amplify the number through routers aN
onto r2.

The number of routers is set in `test_bird.py` using option `num_bird_routers`.

During testing the option `--enable-performance-test` must be specified. For example...
```sh
docker-compose run --rm birdplan /root/runtest "tests/t40_bgp/t99_breaking/test_bird.py --enable-performance-test"
```


# Diagram

```plantuml
@startuml
hide circle
title Test BGP performance from e1 through to r2


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}

skinparam class {
    BorderStyle<<dynamic>> dotted
}

class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

}

class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.3/24
+ fc00:100::3/64
}

class "Router: a1" {
  .. Interface: eth0 ..
- 100.64.0.n/16
+ fc00:100::nnnn/64
}


class "Router: aN" <<dynamic>> {
  .. Interface: eth0 ..
- 100.64.0.n/16
+ fc00:100::nnnn/64
}


"ExaBGP: e1" -down-> "Router: r1"

"Router: r1" -down-> "Router: a1"
"Router: r1" -down-> "Router: aN"

"Router: a1" -down-> "Router: r2"
"Router: aN" -down-> "Router: r2"



@enduml
```
