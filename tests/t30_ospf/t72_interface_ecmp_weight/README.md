# OSPF tests for interface ECMP weight

We're testing router r2, r3, r4 connected to r5, r6, r7 via 4 links.


In the case of `t10_basic`:
  - Test OSPF interface ECMP weight between routers using default values.

In the case of `t20_conffile`:
  - Test OSPF interface ECMP weight when set in a configuration file.

In the case of `t30_commandline`:
  - Test OSPF interface ECMP weight when overridden from commandline.

In the case of `t32_commandline_pattern`:
  - Test OSPF interface ECMP weight when overridden from commandline using an interface pattern.


## Diagram

```plantuml
@startuml
hide circle
title OSPF test for interface ECMP weight


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth2..
- 100.127.0.1/24
+ fc00:127::1/64
}

class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64

  .. Interface: eth1 (L1) ..
- 100.102.0.2/24
- fc00:102::2/64

  .. Interface: eth2 (L2) ..
- 100.103.0.2/24
- fc00:103::2/64

  .. Interface: eth3 (L2) ..
- 100.104.0.2/24
- fc00:104::2/64

  .. Interface: eth4 (L2) ..
- 100.105.0.2/24
- fc00:105::2/64
}


class "Router: r3" {
  .. Interface: eth0 ..
- 100.64.0.3/24
- fc00:100::3/64

  .. Interface: eth1 (L1) ..
- 100.102.0.3/24
- fc00:102::3/64

  .. Interface: eth2 (L2) ..
- 100.103.0.3/24
- fc00:103::3/64

  .. Interface: eth3 (L2) ..
- 100.104.0.3/24
- fc00:104::3/64

  .. Interface: eth4 (L2) ..
- 100.105.0.3/24
- fc00:105::3/64
}

class "Router: r4" {
  .. Interface: eth0 ..
- 100.64.0.4/24
- fc00:100::4/64

  .. Interface: eth1 (L1) ..
- 100.102.0.4/24
- fc00:102::4/64

  .. Interface: eth2 (L2) ..
- 100.103.0.4/24
- fc00:103::4/64

  .. Interface: eth3 (L2) ..
- 100.104.0.4/24
- fc00:104::4/64

  .. Interface: eth4 (L2) ..
- 100.105.0.4/24
- fc00:105::4/64
}

class "Router: r5" {
  .. Interface: eth0 ..
- 100.110.0.5/24
- fc00:200::5/64

  .. Interface: eth1 (L1) ..
- 100.102.0.5/24
- fc00:102::5/64

  .. Interface: eth2 (L2) ..
- 100.103.0.5/24
- fc00:103::5/64

  .. Interface: eth3 (L2) ..
- 100.104.0.5/24
- fc00:104::5/64

  .. Interface: eth4 (L2) ..
- 100.105.0.5/24
- fc00:105::5/64
}

class "Router: r6" {
  .. Interface: eth0 ..
- 100.110.0.6/24
- fc00:200::6/64

  .. Interface: eth1 (L1) ..
- 100.102.0.6/24
- fc00:102::6/64

  .. Interface: eth2 (L2) ..
- 100.103.0.6/24
- fc00:103::6/64

  .. Interface: eth3 (L2) ..
- 100.104.0.6/24
- fc00:104::6/64

  .. Interface: eth4 (L2) ..
- 100.105.0.6/24
- fc00:105::6/64
}

class "Router: r7" {
  .. Interface: eth0 ..
- 100.110.0.7/24
- fc00:200::7/64

  .. Interface: eth1 (L1) ..
- 100.102.0.7/24
- fc00:102::7/64

  .. Interface: eth2 (L2) ..
- 100.103.0.7/24
- fc00:103::7/64

  .. Interface: eth3 (L2) ..
- 100.104.0.7/24
- fc00:104::7/64

  .. Interface: eth4 (L2) ..
- 100.105.0.7/24
- fc00:105::7/64
}

class "Router: r8" {
  .. Interface: eth0 ..
- 100.110.0.8/24
- fc00:200::8/64
}

class "Switch: s1" {}
class "Switch: s2" {}
class "Switch: s3" {}
class "Switch: s4" {}
class "Switch: s5" {}
class "Switch: s6" {}


"Router: r1" -down-> "Switch: s1": r1 eth0
"Router: r1" --() NC: r1 eth2

"Switch: s1" -down-> "Router: r2": r2 eth0
"Switch: s1" -down-> "Router: r3": r3 eth0
"Switch: s1" -down-> "Router: r4": r4 eth0

"Router: r2" -down-> "Switch: s2": r2 eth1
"Router: r3" -down-> "Switch: s2": r3 eth1
"Router: r4" -down-> "Switch: s2": r4 eth1

"Router: r2" -down-> "Switch: s3": r2 eth2
"Router: r3" -down-> "Switch: s3": r3 eth2
"Router: r4" -down-> "Switch: s3": r4 eth2

"Router: r2" -down-> "Switch: s4": r2 eth3
"Router: r3" -down-> "Switch: s4": r3 eth3
"Router: r4" -down-> "Switch: s4": r4 eth3

"Router: r2" -down-> "Switch: s5": r2 eth4
"Router: r3" -down-> "Switch: s5": r3 eth4
"Router: r4" -down-> "Switch: s5": r4 eth4



"Switch: s2" -down-> "Router: r5": r5 eth1
"Switch: s2" -down-> "Router: r6": r6 eth1
"Switch: s2" -down-> "Router: r7": r7 eth1

"Switch: s3" -down-> "Router: r5": r5 eth2
"Switch: s3" -down-> "Router: r6": r6 eth2
"Switch: s3" -down-> "Router: r7": r7 eth2

"Switch: s4" -down-> "Router: r5": r5 eth3
"Switch: s4" -down-> "Router: r6": r6 eth3
"Switch: s4" -down-> "Router: r7": r7 eth3

"Switch: s5" -down-> "Router: r5": r5 eth4
"Switch: s5" -down-> "Router: r6": r6 eth4
"Switch: s5" -down-> "Router: r7": r7 eth4

"Router: r5" -down-> "Switch: s6": r5 eth0
"Router: r6" -down-> "Switch: s6": r6 eth0
"Router: r7" -down-> "Switch: s6": r7 eth0

"Switch: s6" -down-> "Router: r8": r8 eth0


@enduml
```
