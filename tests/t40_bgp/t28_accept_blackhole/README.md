# BGP basic test to accept blackhole routes

## Peer-based setting

In the case of `test_peer_accept_bgp_own_blackhole`: **(default)**
  - r1 should be accepting our own blackhole routes by default.

In the case of `test_peer_accept_bgp_own_blackhole_true`:
  - r1 should be accepting our own blackhole routes (by default).

In the case of `test_peer_accept_bgp_own_blackhole_false`:
  - r1 should not be accepting our own blackhole routes.

In the case of `test_peer_accept_bgp_customer_blackhole`: **(default)**
  - r1 should be accepting customer blackhole routes by default.

In the case of `test_peer_accept_bgp_customer_blackhole_true`:
  - r1 should be accepting customer blackhole routes (by default).

In the case of `test_peer_accept_bgp_customer_blackhole_false`:
  - r1 should not be accepting customer blackhole routes.

## Global setting

In the case of `test_global_accept_bgp_own_blackhole`: **(default)**
  - r1 should accept our own blackhole routes into the master table by default.

In the case of `test_global_accept_bgp_own_blackhole_true`:
  - r1 should accept our own blackhole routes into the master table (by default).

In the case of `test_global_accept_bgp_own_blackhole_false`:
  - r1 should not accept our own blackhole routes into the master table.

In the case of `test_global_accept_bgp_customer_blackhole`: **(default)**
  - r1 should accept customer blackhole routes into the master table by default.

In the case of `test_global_accept_bgp_customer_blackhole_true`:
  - r1 should accept customer blackhole routes into the master table (by default).

In the case of `test_global_accept_bgp_customer_blackhole_false`:
  - r1 should not accept customer blackhole routes into the master table.


# Diagram

```plantuml
@startuml
hide circle
title Test blackhole routes from e1 to r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/48
}


class "ExaBGP: e1" {
  All peer types
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}

class "ExaBGP: e2" {
  Internal peer types
  .. Interface: eth0 ..
- 100.64.0.3/24
+ fc00:100::3/64
}

class "Switch: s1" {}


"ExaBGP: e1" -down-> "Switch: s1": r1 eth0
"ExaBGP: e2" -down-> "Switch: s1": r1 eth0
"Switch: s1" -down-> "Router: r1": r1 eth0
"Router: r1" --() NC: r1 eth2

@enduml
```
