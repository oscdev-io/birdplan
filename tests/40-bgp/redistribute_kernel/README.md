# BGP redistribution of kernel routes

Router r1 should be exporting the kernel routes on r1 interface eth1 to r2, r2 should only get routes from r1 eth1. Router
r2 should not be exporting its own kernel routes via BGP to r1 as it does not have redistribute:kernel set to True.


```plantuml
@startuml
hide circle
title Test redistribute kernel routes on r1 (eth1) to r2
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. Kernel routes ..
- 100.101.0.0/24 via 192.168.1.2 (eth1)
+ fc00:101::/48 via fc01::2 (eth1)
- 100.103.0.0/24 dev eth1
+ fc00:103::/64 dev eth1

  .. BGP ..
* AS65000
}
note top: Should export kernel routes on eth1 to r2


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. Interface: eth1 ..
- 192.168.2.1/24
+ fc02::1/64

  .. Kernel routes ..
- 100.102.0.0/24 via 192.168.2.2 (eth1)
+ fc00:102::/48 via fc02::2 (eth1)
- 100.104.0.0/24 dev eth1
+ fc00:104::/64 dev eth1

  .. BGP ..
* AS65001
}
note top: Should get kernel routes from r1 eth1, \n should not export own kernel routes to r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r2" --() NC: r2 eth1

@enduml
```
