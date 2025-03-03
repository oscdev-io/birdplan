# BGP action tests

Router r1 should be receiving routes from e1 test cases and advertising to r2-r9.

In terms of test set `t12_prefix_length`:
  - ExaBGP e1 should advertise a route with various prefix sizes to r1, depending on the peer type r1 should either export or not export the route.



## Diagram


```plantuml
@startuml
hide circle
title Test BGP outbound filtering from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

}

class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.3/24
+ fc00:100::3/64

}

class "Switch: s1" {}


"Router: r1" <-> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Switch: s1" <-up- "ExaBGP: e1": e1 eth0


@enduml
```
