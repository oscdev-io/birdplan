# BGP redistribution of BIRD static routes


Router r1 should export its static on interface eth1 to r2 depending on the test case.


In the case of "test_redistribute_static": **(default)**
  - r1 should not be exporting its static routes to r2 as this is default behavior.

In the case of "test_redistribute_static_true":
  - r1 should be exporting its static routes on interface eth1 to r2.

In the case of "test_redistribute_static_false":
  - r1 should not be exporting its static routes to r2 as `redistribute:static` is set to false.

In the case of "test_redistribute_static_blackhole": **(default)**
  - r1 should not be exporting its static blackhole routes to r2 as this is default behavior.

In the case of "test_redistribute_static_blackhole_true":
  - r1 should be exporting its static blackhole routes to r2 depending on the test case.

In the case of "test_redistribute_static_blackhole_false":
  - r1 should not be exporting its static blackhole routes to r2 as `redistribute:static_blackhole` is set to false.

In the case of "test_redistribute_static_default": **(default)**
  - r1 should not be exporting its static default routes to r2 as this is default behavior.

In the case of "test_redistribute_static_default_true":
  - r1 should be exporting its static default routes to r2 depending on the test case.

In the case of "test_redistribute_static_default_false":
  - r1 should not be exporting its static default routes to r2 as `redistribute:static_default` is set to false.


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
  - 100.105.0.0/24 via 192.168.1.4 (eth1)
  + fc00:105::/48 via fc01::4 (eth1)
  - 100.106.0.0/24 via eth1
  + fc00:106::/48 via eth1
  - 100.107.0.0/31 blackhole
  + fc00:107::/127 blackhole
  - 0.0.0.0/0 via 192.168.1.4 (eth1)
  + ::/0 via fc01::4 (eth1)
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
