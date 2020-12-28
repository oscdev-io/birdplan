# BGP importing of connected routes


In the case of `import_connected`:  **(default)**
  - r1 should not be importing any routes by default.

In the case of `import_connected_false`:
  - r1 should not be importing routes from any interfaces.

In the case of `import_connected_list`:
  - r1 should be importing routes from the list of interfaces.

In the case of `import_connected_star`:
  - r1 should be importing routes from the matched interfaces.

In the case of `import_connected_true`:
  - r1 should be importing routes from all interfaces.


## Diagram

```plantuml
@startuml
hide circle
title Test import connected routes on r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::/48

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/48

  .. Interface: eth10 ..
- 100.211.0.1/24
+ fc00:211::1/48
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r1" --() NC: r1 eth2
"Router: r1" --() NC: r1 eth10

@enduml
```
