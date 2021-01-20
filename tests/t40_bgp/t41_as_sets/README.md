# BGP AS-SET change tests

In terms of test `t10_as_sets_changes`:
  - Test exceptions raised during substantial AS-SET prefix filter changes.

In terms of test `t12_as_sets_changes_ignore`:
  - Test ignoring exceptions raised during substantial AS-SET prefix filter changes.

In terms of test `t14_as_sets_use_cached`:
  - Test using previous cached AS-SET data when generating peer configuration.

## Diagram

```plantuml
@startuml
hide circle
title Test BGP prefix limits from e1 to r1


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}

class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "Switch: s1" {}


"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0


@enduml
```
