# BGP outgoing large community tests

ExaBGP e1 and e2 should be advertising various types of routes to r1, which should in turn be advertising to r2 based on the test case.

## Test sets for BGP outgoing large communities

In terms of test set "t10_connected":
  - This test set tests adding a large community to a connected route.

In terms of test set "t12_kernel":
  - This test set tests adding a large community to a kernel route.

In terms of test set "t14_static":
  - This test set tests adding a large community to a static route.

In terms of test set "t16_originated":
  - This test set tests adding a large community to an orginated route.

In terms of test set "t20_bgp":
  - This test set tests adding a large community to a route we received via BGP.

In terms of test set "t22_bgp_own":
  - This test set tests adding a large community to a route originating within our federation that we received via BGP.

In terms of test set "t24_bgp_customer":
  - This test set tests adding a large community to a route originating from a customer.

In terms of test set "t26_bgp_peering":
  - This test set tests adding a large community to a route originating from a peer.

In terms of test set "t28_bgp_transit":
  - This test set tests adding a large community to a route originating from a transit provider.

In terms of test set "t30_community_list":
  - This test set tests adding a large community all advertised routes.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP outgoing large communities from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
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
"Router: r1" --() NC: r2 eth1


@enduml
```
