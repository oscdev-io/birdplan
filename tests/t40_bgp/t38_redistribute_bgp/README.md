# Tests for redistribution of BGP routes

These tests test BGP route redistribution from e1/e2 via r1 to r2.


In terms of test set `t10_bgp`:
  - This test set tests redistribution of BGP routes (covering all routes of all types).

In terms of test set `t12_bgp_own`:
  - This test set tests redistribution of our own BGP routes (originating within our federation).

In terms of test set `t14_bgp_customer`:
  - This test set tests redistribution of BGP routes received from customers.

In terms of test set `t16_bgp_peering`:
  - This test set tests redistribution of BGP routes received from peers.

In terms of test set `t18_bgp_transit`:
  - This test set tests redistribution of BGP routes received from transit providers.

In terms of test set `t20_own_blackhole`:
  - This test set tests redistribution of our own BGP blackhole routes (originating within our federation).

In terms of test set `t22_bgp_customer_blackhole`:
  - This test set tests redistribution of BGP blackhole routes received from customers.

In terms of test set `t24_bgp_own_default`:
  - This test set tests redistribution of our own BGP default routes (originating within our federation).

In terms of test set `t26_bgp_transit_default`:
  - This test set tests redistribution of BGP default routes received from transit providers.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP route redistribution


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

class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.3/24
+ fc00:100::3/64

}

class "ExaBGP: e2" {
  .. Interface: eth0 ..
- 100.64.0.4/24
+ fc00:100::4/64

}

class "Switch: s1" {}

"ExaBGP: e1" -down-> "Switch: s1": e1 eth0
"ExaBGP: e2" -down-> "Switch: s1": e2 eth0
"Router: r1" <-> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r2 eth2


@enduml
```
