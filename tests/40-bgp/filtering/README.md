# BGP filtering tests

Router r1 should be receiving routes from e1 test cases. As we are dealing with filtering r1's main BGP routing table should be blank and the routes in the BGP peer routing table should all be marked filtered.

Tests done include:
  * Prefix length too long
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * Bogon filtering
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * Bogon ASN filtering
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * AS path too long filtering
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * AS path too short filtering
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * First AS not peer AS
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * Nexthop not peer IP
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver

```plantuml
@startuml
hide circle
title Test BGP filtering from e1 to r1
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP ..
* AS65000
}
note top: Should receive routes from e1 but mark as filtered


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. BGP ..
* AS65001
}
note top: Should be announcing filter test routes to r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "ExaBGP: e1": e1 eth0

@enduml
```
