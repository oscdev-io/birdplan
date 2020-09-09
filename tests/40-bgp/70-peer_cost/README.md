# BGP peer cost tests

Router r1 should be receiving routes from e1 test cases with a local pref -5 (cost = 5).

Tests done include:
  * Cost
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver

```plantuml
@startuml
hide circle
title Test BGP peer cost from e1 to r1
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP ..
* AS65000
}
note top: Should receive routes from e1 with a local pref -5 \n (cost = 5)


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. BGP ..
* AS65001
}
note top: Should be announcing a prefix to r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "ExaBGP: e1": e1 eth0

@enduml
```
