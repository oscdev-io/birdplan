# BGP redistribution of originated routes

In the case of `test_redistribute_originated`: **(default)**
  - r1 should not be exporting its originated routes to r2 as this is default behavior.

In the case of `test_redistribute_originated_true`:
  - r1 should be exporting its originated routes to r2.

In the case of `test_redistribute_originated_false`:
  - r1 should not be exporting its originated routes to r2 as `redistribute:originated` is set to false.

In the case of `test_redistribute_originated_default`: **(default)**
  - r1 should not be exporting its originated default routes to r2 as this is default behavior.

In the case of `test_redistribute_originated_default_true`:
  - r1 should be exporting its originated default routes to r2 depending on the test case.

In the case of `test_redistribute_originated_default_false`:
  - r1 should not be exporting its originated default routes to r2 as `redistribute:originated_default` is set to false.


```plantuml
@startuml
hide circle
title Test originated routes from r1


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
