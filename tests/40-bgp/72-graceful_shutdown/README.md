# BGP graceful shutdown tests

Router r1 should be receiving routes from r2 that include the graceful shutdown community.

Tests done include:
  * Graceful shutdown
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver

```plantuml
@startuml
hide circle
title Test BGP graceful shutdown from r2 to r1
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP ..
* AS65000
}
note top: Should receive routes from r2 with the graceful shutdown \n community and set them with local_pref 0


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. BIRD static routes ..
- 100.102.0.0/24 via 192.168.2.2 (eth1)
+ fc00:102::/48 via fc02::2 (eth1)

  .. BGP ..
* AS65001
}
note top: Should be announcing test routes to r1 with \n the graceful shutdown community included


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Router: r2" --() NC: r2 eth1

@enduml
```
