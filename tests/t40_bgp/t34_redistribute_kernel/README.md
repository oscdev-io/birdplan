# BGP redistribution of kernel routes


Router r1 should export its kernel routes on interface eth1 to r2 depending on the test case.


In the case of "test_redistribute_kernel": **(default)**
  - r1 should not be exporting its kernel routes to r2 as this is default behavior.

In the case of "test_redistribute_kernel_true":
  - r1 should be exporting its kernel routes on interface eth1 to r2.

In the case of "test_redistribute_kernel_false":
  - r1 should not be exporting its kernel routes to r2 as `redistribute:kernel` is set to false.

In the case of "test_redistribute_kernel_blackhole": **(default)**
  - r1 should not be exporting its kernel blackhole routes to r2 as this is default behavior.

In the case of "test_redistribute_kernel_blackhole_true":
  - r1 should be exporting its kernel blackhole routes to r2 depending on the test case.

In the case of "test_redistribute_kernel_blackhole_false":
  - r1 should not be exporting its kernel blackhole routes to r2 as `redistribute:kernel_blackhole` is set to false.

In the case of "test_redistribute_kernel_default": **(default)**
  - r1 should not be exporting its kernel default routes to r2 as this is default behavior.

In the case of "test_redistribute_kernel_default_true":
  - r1 should be exporting its kernel default routes to r2 depending on the test case.

In the case of "test_redistribute_kernel_default_false":
  - r1 should not be exporting its kernel default routes to r2 as `redistribute:kernel_default` is set to false.

## Diagram

```plantuml
@startuml
hide circle
title Test redistribute kernel routes on r1 (eth1) to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. Kernel routes ..
- 100.101.0.0/24 via 192.168.1.3
+ fc00:101::/48 via fc01::3
- 100.103.0.0/24 dev eth1
+ fc00:103::/64 dev eth1
- 100.104.0.0/31 blackhole
+ fc00:104::/127 blackhole
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

@enduml
```
