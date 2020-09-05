# BGP adding of outgoing large communities

Router r1 should be exporting its static routes to r2 with outgoing large communities, r2 should receive the static routes from r1 with the large communities added.


```plantuml
@startuml
hide circle
title Test outgoing large communities from r1 to r2
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
note top: Should export static routes to r2 with outgoing large communities


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. Interface: eth1 ..
- 192.168.2.1/24
+ fc02::1/64

  .. BGP ..
* AS65001
}
note top: Should get static routes from r1 \n with the large communities added.


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1

@enduml
```
