# Basic OSPF test


In terms of test `ospf`:  **(default)**
  - Router r1 should export routes to r2 and r2 should insert routes into its RIB.

In terms of test `ospf_no_export_kernel`:
  - Router r1 should export routes to r2 and r2 should NOT insert routes into its RIB.

This setup uses OSPF v3 explicitly specified for IPv4.


## Diagram

```plantuml
@startuml
hide circle
title Test for basic OSPF routing


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
