# BGP location-based large community tests

Router r1 should be receiving routes from e1 test cases.


**Tests for BGP location-based large communities:**

In terms of test "test_bgp_stripping_community_location_iso3166":
  - ExaBGP e1 should export a prefix to router to r2, router r2 should add a location-based ISO-3166 large community.

In terms of test "test_bgp_stripping_community_location_unm49":
  - ExaBGP e1 should export a prefix to router to r2, router r2 should add a location-based UN.M49 large community.


```plantuml
@startuml
hide circle
title Test BGP large location-based large communities from e1 to r1


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
