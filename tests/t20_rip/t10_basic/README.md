# Basic RIP test


In terms of test `rip`: **(default)**
  - Router r1 should install RIP routes into OS RIB.

In terms of test `export_kernel_rip_false`:
  - Router r1 should not install RIP routes into OS RIB.

In terms of test `export_kernel_rip_true`:
  - Router r1 should install RIP routes into OS RIB.


## Diagram

```plantuml
@startuml
hide circle
title Test for basic RIP routing


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64
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

@enduml
```
