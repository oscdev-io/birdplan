# BGP add paths tests

Router r1 should be receiving multiple routes with the same prefix from e1 test cases.

# Diagram

```plantuml
@startuml
hide circle
title Test BGP add paths from e1 to r1


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

"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0

@enduml
```
