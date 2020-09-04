# BGP redistribution of BIRD static routes

Router r1 should be exporting the BIRD static routes on r1 interface eth1 to r2, r2 should only get routes from r1 eth1. Router
r2 should not be exporting its own static routes via BGP to r1 as it does not have redistribute:static set to True.


```plantuml
@startuml
hide circle
title Test redistribute statics on r1 (eth1) to r2
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. BIRD static routes ..
- 100.101.0.0/24 via 192.168.1.2 (eth1)
+ fc00:101::/48 via fc01::2 (eth1)

  .. BGP ..
* AS65000
}
note top: Should export BIRD static routes on eth1 to r2


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. Interface: eth1 ..
- 192.168.2.1/24
+ fc02::1/64

  .. BIRD static routes ..
- 100.102.0.0/24 via 192.168.2.2 (eth1)
+ fc00:102::/48 via fc02::2 (eth1)

  .. BGP ..
* AS65001
}
note top: Should get BIRD static routes from r1 eth1, \n should not export own static routes to r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r2" --() NC: r2 eth1

@enduml
```
