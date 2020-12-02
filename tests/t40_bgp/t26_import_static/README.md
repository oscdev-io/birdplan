# BGP importing of BIRD static routes


Router r1 should import its static routes on interface eth1 but not export to r2.


In the case of "test_import_static": **(default)**
  - r1 should not be importing static routes by default.

In the case of "test_import_static_true":
  - r1 should be importing static routes but not blackhole routes.

In the case of "test_import_static_false":
  - r1 should not be importing static routes.

In the case of "test_import_static_blackhole_true":
  - r1 should be importing static blackhole routes but not normal static routes.

In the case of "test_import_static_blackhole_false":
  - r1 should not be importing static routes.


## Diagram

```plantuml
@startuml
hide circle
title Test import statics on r1 to r2


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
- 100.103.0.0/24 dev eth1
+ fc00:103::/48 dev eth1
- 100.104.0.0/24 blackhole
+ fc00:104::/48 blackhole
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
