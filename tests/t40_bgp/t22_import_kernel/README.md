# BGP importing of kernel routes


In the case of `test_import_kernel`: **(default)**
  - r1 should not be importing kernel routes by default.

In the case of `test_import_kernel_true`:
  - r1 should be importing kernel routes and not blackhole routes.

In the case of `test_import_kernel_false`:
  - r1 should not be importing kernel routes.

In the case of `test_import_kernel_blackhole_true`:
  - r1 should be importing kernel blackhole routes but not normal kernel routes.

In the case of `test_import_kernel_blackhole_false`:
  - r1 should not be importing kernel routes.

In the case of `test_import_kernel_default_true`:
  - r1 should be importing kernel default routes but not normal kernel routes.

In the case of `test_import_kernel_default_false`:
  - r1 should not be importing kernel routes.


## Diagram

```plantuml
@startuml
hide circle
title Test import kernel routes on r1


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
