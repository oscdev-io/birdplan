# Basic OSPF test


In terms of test "ospf":
  - Router r1 should export routes to r2 and r2 should insert routes into its RIB.

In terms of test "ospf_no_export_kernel":
  - Router r1 should export routes to r2 and r2 should NOT insert routes into its RIB.


```plantuml
@startuml
hide circle
title Test for basic OSPF routing
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. BIRD static routes ..
- 10.0.0.0/24 via 100.101.0.2 (eth1)
- fc10::/64 via fc00:101::2 (eth1)
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64
}



class "Switch: s1" {}


"Switch: s1" -- "Router: r1": r1 eth0
"Switch: s1" -- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1

@enduml
```
