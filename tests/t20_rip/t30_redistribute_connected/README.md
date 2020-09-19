# RIP test for redistribution of connected routes

Router r1 should export its connected routes on eth1 to r2.


```plantuml
@startuml
hide circle
title RIP test for redistribution of connected routes
left to right direction


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


"Switch: s1" -- "Router: r1": r1 eth0
"Switch: s1" -- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1

@enduml
```
