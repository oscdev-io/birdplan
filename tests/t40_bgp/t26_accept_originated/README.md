# BGP basic test to accept originated routes

Test originated routes from r1 to r2.

In the case of `test_accept_originated`: **(default)**
  - r1 should be accepting originated routes by default.

In the case of `test_accept_originated_true`:
  - r1 should be accepting originated routes.

In the case of `test_accept_originated_false`:
  - r1 should not be accepting originated routes.


```plantuml
@startuml
hide circle
title Test BGP originated routes


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
