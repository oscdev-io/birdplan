# OSPF test for stub interface routes


Router r1 should export its stub interface routes on eth1 to r2.


## Diagram

```plantuml
@startuml
hide circle
title OSPF test for stub interface routes


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 (stub) ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64
}



class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth2

@enduml
```
