# Basic static routing


In terms of test `static`:  **(default)**
  - Router r1 should install static routes into OS RIB.

In terms of test `export_kernel_static_false`:
  - Router r1 should not install static routes into OS RIB.

In terms of test `export_kernel_static_true`:
  - Router r1 should install static routes into OS RIB.


## Diagram

```plantuml
@startuml
hide circle
title Test for basic static routing

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

class "Switch: s1" {}

"Router: r1" -> "Switch: s1": r1 eth0
"Router: r1" --() NC: r1 eth1


@enduml
```
