# BGP basic test to accept originated routes

Router r1 is configured with originated routes, but should not be exporting them to to r2.


In the case of "test_accept_originated": **(default)**
  - r1 should be accepting originated routes by default.

In the case of "test_accept_originated_true":
  - r1 should be accepting originated routes.

In the case of "test_accept_originated_false":
  - r1 should not be accepting originated routes.


```plantuml
@startuml
hide circle
title Test originated routes from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP Originated ..
- 100.101.0.0/24 (blackhole)
+ fc00:101::/48 (blackhole)

}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0

@enduml
```
