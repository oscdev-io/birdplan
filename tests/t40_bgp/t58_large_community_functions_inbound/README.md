# BGP large community function tests (inbound)

Router r1 should be receiving routes from e1 test cases.


In terms of test "test_bgp_large_community_localpref_minus_1":
  - Router r1 should receive a route from e1 with the local pref adjustment large community and -1 from the local_pref.

In terms of test "test_bgp_large_community_localpref_minus_2":
  - Router r1 should receive a route from e1 with the local pref adjustment large community and -2 from the local_pref.

In terms of test "test_bgp_large_community_localpref_minus_3":
  - Router r1 should receive a route from e1 with the local pref adjustment large community and -3 from the local_pref.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP functions from e1 to r1


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
"Switch: s1" ->  "Router: r1": r1 eth0


@enduml
```
