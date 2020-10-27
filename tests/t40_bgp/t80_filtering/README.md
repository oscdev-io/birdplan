# BGP filtering tests

Router r1 should be receiving routes from e1 test cases.


**Tests for AS-PATH too long:**

In terms of test "test_bgp_as_path_too_long":
  - ExaBGP e1 should export a prefix with too many ASNs in the AS-PATH to router to r2, router r2 should filter the prefix and add a large community indicating the reason.
  - Except in case of peer_type `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` where the prefix should be accepted.

TODO


```plantuml
@startuml
hide circle
title Test BGP filtering from e1 to r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}

"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0

@enduml
```
