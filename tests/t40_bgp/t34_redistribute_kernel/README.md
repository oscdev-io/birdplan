# BGP redistribution of kernel routes


In the case of `test_redistribute_kernel`: **(default)**
  - r1 should not be exporting its kernel routes to r2 as this is default behavior.

In the case of `test_redistribute_kernel_true`:
  - r1 should be exporting its kernel routes on interface eth2 to r2.

In the case of `test_redistribute_kernel_false`:
  - r1 should not be exporting its kernel routes to r2 as `redistribute:kernel` is set to false.

In the case of `test_redistribute_kernel_blackhole`: **(default)**
  - r1 should not be exporting its kernel blackhole routes to r2 as this is default behavior.

In the case of `test_redistribute_kernel_blackhole_true`:
  - r1 should be exporting its kernel blackhole routes to r2 depending on the test case.

In the case of `test_redistribute_kernel_blackhole_false`:
  - r1 should not be exporting its kernel blackhole routes to r2 as `redistribute:kernel_blackhole` is set to false.

In the case of `test_redistribute_kernel_default`: **(default)**
  - r1 should not be exporting its kernel default routes to r2 as this is default behavior.

In the case of `test_redistribute_kernel_default_true`:
  - r1 should be exporting its kernel default routes to r2 depending on the test case.

In the case of `test_redistribute_kernel_default_false`:
  - r1 should not be exporting its kernel default routes to r2 as `redistribute:kernel_default` is set to false.

## Diagram

```plantuml
@startuml
hide circle
title Test redistribute kernel routes on r1


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
