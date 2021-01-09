# BGP importing of BIRD static routes


In the case of `test_import_static`: **(default)**
  - r1 should not be importing static routes by default.

In the case of `test_import_static_true`:
  - r1 should be importing static routes but not blackhole routes.

In the case of `test_import_static_false`:
  - r1 should not be importing static routes.

In the case of `test_import_static_blackhole_true`:
  - r1 should be importing static blackhole routes but not normal static routes.

In the case of `test_import_static_blackhole_false`:
  - r1 should not be importing static routes.


## Diagram

```plantuml
@startuml
hide circle
title Test import static routes on r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/48
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth2


@enduml
```
