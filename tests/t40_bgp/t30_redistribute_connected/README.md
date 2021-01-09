# BGP redistribution of connected routes


In the case of `redistribute_connected`: **(default)**
  - r1 should import eth2 connected routes into its BGP table and export them to r2.

In the case of `redistribute_connected_false`:
  - r1 should import eth2 connected routes into its BGP table but not export them to r2.

In the case of `redistribute_connected_true`:
  - r1 should import eth2 connected routes into its BGP table and export them to r2.


## Diagram

```plantuml
@startuml
hide circle
title Test redistribute connected routes on r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/48
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth2

@enduml
```
