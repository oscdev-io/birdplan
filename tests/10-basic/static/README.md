# Basic static routing

In terms of test "static":
  - Router r1 should install static routes into OS FIB.

In terms of test "static_no_export_kernel":
  - Router r1 should not install static routes into OS FIB.


```plantuml
@startuml
hide circle
title Test for basic static routing
left to right direction

class "Router: r1" {
  .. Interface: eth0 ..
- 192.168.0.1/24
+ fc00::1/64

  .. BIRD static routes ..
- 10.0.0.0/24 via 192.168.0.2 (eth0)
+ fc10::/64 via fc00::2 (eth0)
}

class "Switch: s1" {}

"Router: r1" -- "Switch: s1": r1 eth0


@enduml
```
