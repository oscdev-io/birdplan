# OSPF tests for interface cost


In the case of `t10_basic`:
  - Test OSPF interface cost between routers using default values.

In the case of `t20_conffile`:
  - Test OSPF interface cost when set in a configuration file.

In the case of `t30_commandline`:
  - Test OSPF interface cost when set in a configuration file.

In the case of `t32_commandline_pattern`:
  - Test OSPF interface cost when overridden from commandline using an interface pattern.


## Diagram

```plantuml
@startuml
hide circle
title OSPF test for interface cost


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

  .. Interface: eth1 ..
- 100.102.0.2/24
- fc00:102::2/64
}


class "Router: r3" {
  .. Interface: eth0 ..
- 100.64.0.3/24
- fc00:100::3/64

  .. Interface: eth1 ..
- 100.102.0.3/24
- fc00:102::3/64
}

class "Router: r4" {
  .. Interface: eth0 ..
- 100.64.0.4/24
- fc00:100::4/64

  .. Interface: eth1 ..
- 100.102.0.4/24
- fc00:102::4/64
}

class "Router: r5" {
  .. Interface: eth0 ..
- 100.64.0.5/24
- fc00:100::5/64

  .. Interface: eth1 ..
- 100.102.0.5/24
- fc00:102::5/64
}

class "Router: r6" {
  .. Interface: eth0 ..
- 100.64.0.6/24
- fc00:100::6/64

  .. Interface: eth1 ..
- 100.102.0.6/24
- fc00:102::6/64
}

class "Router: r7" {
  .. Interface: eth0 ..
- 100.64.0.7/24
- fc00:100::7/64

  .. Interface: eth1 ..
- 100.102.0.7/24
- fc00:102::7/64
}

class "Router: r8" {
  .. Interface: eth0 ..
- 100.102.0.1/24
- fc00:102::1/64
}

class "Switch: s1" {}
class "Switch: s2" {}


"Router: r1" -down-> "Switch: s1": r1 eth0
"Router: r1" --() NC: r1 eth1

"Switch: s1" -down-> "Router: r2": r2 eth0
"Switch: s1" -down-> "Router: r3": r3 eth0
"Switch: s1" -down-> "Router: r4": r4 eth0
"Switch: s1" -down-> "Router: r5": r5 eth0
"Switch: s1" -down-> "Router: r6": r6 eth0
"Switch: s1" -down-> "Router: r7": r7 eth0

"Router: r2" -down-> "Switch: s2": r2 eth1
"Router: r3" -down-> "Switch: s2": r3 eth1
"Router: r4" -down-> "Switch: s2": r4 eth1
"Router: r5" -down-> "Switch: s2": r5 eth1
"Router: r6" -down-> "Switch: s2": r6 eth1
"Router: r7" -down-> "Switch: s2": r7 eth1


"Switch: s2" -down-> "Router: r8": r8 eth0



@enduml
```
