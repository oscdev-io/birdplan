# BGP community strippings tests

Router r1 should be receiving routes from e1 test cases.


**Tests for BGP community stripping:**

In terms of test "test_bgp_stripping_community":
  - ExaBGP e1 should export a prefix with our ASN in the community to router to r2, router r2 should strip the community and add an informational large community indicating a community was stripped.
  - Except in case of peer_type `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` where the community should not be stripped.

**Tests for BGP large community stripping:**

In terms of test "test_bgp_stripping_large_community_filtered":
  - ExaBGP e1 should export a prefix with a large community containing our ASN and a filtered function to router to r2, router r2 should strip the large community and add an informational large community indicating a large community was stripped.
  - Except in case of peer_type `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` where the large community should not be stripped.

In terms of test "test_accept_default":
  - ExaBGP e1 should export a prefix with a large community containing our ASN and a informational function to router to r2, router r2 should strip the large community and add an informational large community indicating a large community was stripped.
  - Except in case of peer_type `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` where the large community should not be stripped.


```plantuml
@startuml
hide circle
title Test BGP large community stripping from e1 to r1


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
