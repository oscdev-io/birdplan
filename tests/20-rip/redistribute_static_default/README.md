# RIP redistribution of BIRD static default route

Router r1 should advertise its default route on eth1 to router r2 and router r3. Router r2 should reject the incoming route into the master table and OS RIB as it does not have `accept:default` set to `True`, router r3 should accept the route into the master table and export it to the OS RIB as it has `accept:default` set to `True`.


```plantuml
@startuml
hide circle
title Test redistribute static default route on r1 (eth1) to r3
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
note top: Should export BIRD static default route on eth1 to r2 and r3


class "Router: r2" {
  .. Interface: eth0 ..
- 192.168.0.2/24
+ fc00::2/64
}
note top: Should get BIRD static default route from r1, but not export to the master table


class "Router: r3" {
  .. Interface: eth0 ..
- 192.168.0.3/24
+ fc00::3/64
}
note top: Should get BIRD static default route from r1 and export to the master table and OS RIB


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Switch: s1" <-down- "Router: r3": r3 eth0

"Router: r1" --() NC: r1 eth1

@enduml
```
