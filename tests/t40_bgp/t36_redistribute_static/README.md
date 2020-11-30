# BGP redistribution of BIRD static routes


Router r1 should export its static on interface eth1 to r2 depending on the test case.


In the case of "test_redistribute_static": **(default)**
  - r1 should be exporting its static routes on interface eth1 to r2 as this is default behavior.

In the case of "test_redistribute_static_true":
  - r1 should be exporting its static routes on interface eth1 to r2.

In the case of "test_redistribute_static_false":
  - r1 should not be exporting its static routes to r2 as `redistribute:static` is set to false.


## Diagram

```plantuml
@startuml
hide circle
title Test redistribute statics on r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. BIRD static routes ..
- 100.101.0.0/24 via 192.168.1.2
+ fc00:101::/48 via fc01::2
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1


@enduml
```