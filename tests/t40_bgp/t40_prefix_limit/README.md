# BGP prefix limit tests

In terms of test `test_bgp_prefix_limit`:
  - Exabgp e1 should be sending too many prefixes to r1 causing the session to be torn down.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP prefix limits from e1 to r1


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}

class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "Switch: s1" {}


"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0


@enduml
```
