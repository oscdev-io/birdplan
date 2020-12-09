# RIP test for redistribution of kernel routes


In the case of "redistribute_kernel": **(default)**
  - Router r1 should not be exporting its kernel routes to r2.

In the case of "redistribute_kernel_false":
  - Router r1 should not be exporting its kernel routes to r2.

In the case of "redistribute_kernel_true":
  - Router r1 should be exporting its kernel routes to r2, but not the default route.


## Diagram

```plantuml
@startuml
hide circle
title RIP test for redistribution of kernel routes


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. Kernel static routes ..
- 192.168.20.0/24 via 192.168.1.2
+ fc20:/64 via fc01::2
- 192.168.30.0/24 dev eth1
+ fc30::/64 dev eth1
- 0.0.0.0/0 via 100.101.0.2
+ ::/0 via fc00:101::2
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
