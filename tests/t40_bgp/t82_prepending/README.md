# BGP prepending tests

ExaBGP e1 and e2 (as route reflectors) should be advertising routes to router r1 which in turn should be prepending to router r2.


## Tests for prepending all routes

In terms of test `test_bgp_prepend`:
  - All exported routes should be prepended.


## Tests for BGP prepending of BGP route types

In terms of test `test_bgp_prepend_bgp`:
  - All BGP routes should be prepended.

In terms of test `test_bgp_prepend_bgp_customer`:
  - Customer BGP routes should be prepended.

In terms of test `test_bgp_prepend_bgp_customer_blackhole`:
  - Customer BGP blackhole routes should be prepended.

In terms of test `test_bgp_prepend_bgp_own`:
  - All routes that originated within our federation routes should be prepended.

In terms of test `test_bgp_prepend_bgp_own_blackhole`:
  - All blackhole routes that originated within our federation should be prepended.

In terms of test `test_bgp_prepend_bgp_own_default`:
  - All default routes that originated within our federation should be prepended.

In terms of test `test_bgp_prepend_bgp_peering`:
  - All BGP routes received from peers or routeservers should be prepended.

In terms of test `test_bgp_prepend_bgp_transit`:
  - All BGP routes received from transit should be prepended.

In terms of test `test_bgp_prepend_bgp_transit_default`:
  - All BGP default routes received from transit should be prepended.


## Tests for BGP prepending of route types

In terms of test `test_bgp_prepend_blackhole`:
  - All BGP blackhole routes should be prepended.

In terms of test `test_bgp_prepend_default`:
  - All BGP default routes should be prepended.

In terms of test `test_bgp_prepend_kernel`:
  - All locally originated kernel routes should be prepended.

In terms of test `test_bgp_prepend_kernel_blackhole`:
  - All locally originated kernel blackhole routes should be prepended.

In terms of test `test_bgp_prepend_kernel_default`:
  - All locally originated kernel default routes should be prepended.

In terms of test `test_bgp_prepend_originated`:
  - All locally originated BGP routes should be prepended.

In terms of test `test_bgp_prepend_originated_default`:
  - All locally originated BGP default routes should be prepended.

In terms of test `test_bgp_prepend_static`:
  - All locally originated static routes should be prepended.

In terms of test `test_bgp_prepend_static_blackhole`:
  - All locally originated static blackhole routes should be prepended.

In terms of test `test_bgp_prepend_static_default`:
  - All locally originated static default routes should be prepended.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP prepend large communities from r1 to r2


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


"Router: r1" <-> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Switch: s1" <-up- "ExaBGP: e2": r2 eth0
"Switch: s1" <-up- "ExaBGP: e1": r2 eth0
"Router: r1" --() NC: r2 eth1


@enduml
```
