# RIP test for redistribution of connected routes

In the case of `redistribute_connected`: **(default)**
  - r1 should not be exporting its connected routes to r2, as we do not export connected routes by default.

In the case of `redistribute_connected_false`:
  - r1 should not be exporting its connected routes to r2 as `redistribute:connected` is set to False.

In the case of `redistribute_connected_true`:
  - r1 should be exporting its connected routes to r2 as `redistribute:connected` is set to True.

In the case of `redistribute_connected_list`:
  - r1 should be exporting its connected routes on eth1 to r2 as `redistribute:connected` has eth1 in its list.

In the case of `redistribute_connected_star`:
  - r1 should be exporting its connected routes on eth1 and eth10 to r2 as `redistribute:connected` has eth1* in its list.

## Diagram

```plantuml
@startuml
hide circle
title RIP test for redistribution of connected routes


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/64

  .. Interface: eth10 ..
- 100.211.0.1/24
+ fc00:211::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64
}



class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r1" --() NC: r1 eth2
"Router: r1" --() NC: r1 eth10

@enduml
```
