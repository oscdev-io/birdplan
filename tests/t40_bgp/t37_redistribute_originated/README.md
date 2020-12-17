# BGP basic test with originated routes between peers

Router r1 should export its originated routes on interface eth1 to r2 depending on the test case.


In the case of "test_redistribute_originated": **(default)**
  - r1 should not be exporting its originated routes to r2 as this is default behavior.

In the case of "test_redistribute_originated_true":
  - r1 should be exporting its originated routes on interface eth1 to r2.

In the case of "test_redistribute_originated_false":
  - r1 should not be exporting its originated routes to r2 as `redistribute:originated` is set to false.

In the case of "test_redistribute_originated_default": **(default)**
  - r1 should not be exporting its originated default routes to r2 as this is default behavior.

In the case of "test_redistribute_originated_default_true":
  - r1 should be exporting its originated default routes to r2 depending on the test case.

In the case of "test_redistribute_originated_default_false":
  - r1 should not be exporting its originated default routes to r2 as `redistribute:originated_default` is set to false.


```plantuml
@startuml
hide circle
title Test originated routes from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP Originated ..
- 100.108.0.0/24 via 192.168.1.5 (eth1)
+ fc00:108::/48 via fc01::5 (eth1)
- 100.109.0.0/24 via eth1
+ fc00:109::/48 via eth1
- 100.110.0.0/31 blackhole
+ fc00:110::/127 blackhole
- 0.0.0.0/0 via 192.168.1.5 (eth1)
+ ::/0 via fc01::5 (eth1)
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
