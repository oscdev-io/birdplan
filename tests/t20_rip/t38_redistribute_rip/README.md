# Test for no redistribution of RIP routes


In the case of `redistribute_rip`: **(default)**
  - r2 should be exporting its RIP routes to r3, but not the default route.

In the case of `redistribute_rip_false`:
  - r2 should not be exporting any RIP routes to r3.

In the case of `redistribute_rip_true`:
  - r2 should be exporting its RIP routes to r3, but not the default route.


## Diagram

```plantuml
@startuml
hide circle
title Test for no redistribution of RIP routes


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth2 ..
- 100.101.0.1/24
+ fc00:101::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.102.0.1/24
+ fc00:102::1/64
}


class "Router: r3" {
  .. Interface: eth0 ..
- 100.102.0.2/24
+ fc00:102::2/64
}


class "Switch: s1" {}
class "Switch: s2" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0

"Router: r2" -> "Switch: s2": r2 eth1
"Switch: s2" -> "Router: r3": r3 eth0

"Router: r1" --() NC: r1 eth2

@enduml
```
