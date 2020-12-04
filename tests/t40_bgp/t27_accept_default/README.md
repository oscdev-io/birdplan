# BGP basic test to accept default routes

ExaBGP e1 should be advertising a default route to r1, depending on r1's configuration it should either be accepting or filtering the route.


In the case of "test_accept_default": **(default)**
  - r1 should not be accepting default routes by default, also we do not accept default routes from this peer.

In the case of "test_accept_default_true":
  - r1 should not be accepting default routes as we do not accept default routes from this peer.

In the case of "test_accept_default_false":
  - r1 should not be accepting default routes, also we do not accept default routes from this peer.


# Diagram

```plantuml
@startuml
hide circle
title Test default routes from e1 to r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"ExaBGP: e1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r1": r1 eth0

@enduml
```
