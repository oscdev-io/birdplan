# BGP basic test with originated routes between peers

Router r1 should be exporting its originated routes to r2, r2 should not be exporting its own originated routes to r1 as redistribute:originated is not set to True.

Router r2 should however be receiving and importing the originated routes from r1.


```plantuml
@startuml
hide circle
title Test originated routes from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP Originated ..
- 100.101.0.0/24 (blackhole)
+ fc00:101::/48 (blackhole)

}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0

@enduml
```