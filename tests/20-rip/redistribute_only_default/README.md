# RIP redistribution of BIRD default route

Router r1 should NOT advertise its default route on eth1 to router r2 because it is only exporting default and not static and the default route is a static route.


```plantuml
@startuml
hide circle
title Test redistribute default route on r1 (eth1) to r2
left to right direction

class "Router: r1" {
  .. Interface: eth0 ..
- 192.168.0.1/24
+ fc00::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. BIRD static routes ..
- 0.0.0.0/0 via 192.168.1.2 (eth1)
+ ::/0 via fc01::2 (eth1)
}
note top: Should NOT export BIRD static default route on eth1 to r2


class "Router: r2" {
  .. Interface: eth0 ..
- 192.168.0.2/24
+ fc00::2/64
}
note top: Should not get the default route from r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0

"Router: r1" --() NC: r1 eth1

@enduml
```
