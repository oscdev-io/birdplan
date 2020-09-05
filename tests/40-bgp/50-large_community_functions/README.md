# BGP filtering tests

Router r1 should be receiving routes from e1 test cases. As we are dealing with filtering r1's main BGP routing table should be blank and the routes in the BGP peer routing table should all be marked filtered.

Tests done include:
  * NOEXPORT for PEER_ASN
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * NOEXPORT for the transit peer type
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * NOEXPORT for the peer peer type
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * NOEXPORT for the customer peer type
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * PREPEND 1x
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * PREPEND 2x
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
  * PREPEND 3x
    * Peer types: customer, peer, transit, rrclient, rrserver, rrserver-rrserver, routecollector, routeserver
```plantuml
@startuml
hide circle
title Test BGP large community functions from e1 to r1 to r2
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BGP ..
* AS65000
}
note top: r1 should get the NOEXPORT route from e1 \n and advertise to the peers on the right


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. BGP ..
* AS65002
* Type: customer
}


class "Router: r3" {
  .. Interface: eth0 ..
- 100.64.0.3/24
+ fc00:100::3/64

  .. BGP ..
* AS65003
* Type: peer
}


class "Router: r4" {
  .. Interface: eth0 ..
- 100.64.0.4/24
+ fc00:100::4/64

  .. BGP ..
* AS65004
* Type: transit
}


class "Router: r5" {
  .. Interface: eth0 ..
- 100.64.0.5/24
+ fc00:100::5/64

  .. BGP ..
* AS65000
* Type: rrclient
}


class "Router: r6" {
  .. Interface: eth0 ..
- 100.64.0.6/24
+ fc00:100::6/64

  .. BGP ..
* AS65000
* Type: rrserver
}


class "Router: r7" {
  .. Interface: eth0 ..
- 100.64.0.7/24
+ fc00:100::7/64

  .. BGP ..
* AS65000
* Type: rrserver-rrserver
}


class "Router: r8" {
  .. Interface: eth0 ..
- 100.64.0.8/24
+ fc00:100::8/64

  .. BGP ..
* AS65008
* Type: routecollector
}


class "Router: r9" {
  .. Interface: eth0 ..
- 100.64.0.9/24
+ fc00:100::9/64

  .. BGP ..
* AS65009
* Type: routeserver
}


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.10/24
+ fc00:100::10/64

  .. BGP ..
* AS65001
}
note top: Advertise a NOEXPORT LC function from e1 to r1


class "Switch: s1" {}


"Switch: s1" -up- "Router: r1": r1 eth0
"Switch: s1" -up- "ExaBGP: e1": e1 eth0
"Switch: s1" -down- "Router: r2": r2 eth0
"Switch: s1" -down- "Router: r3": r3 eth0
"Switch: s1" -down- "Router: r4": r4 eth0
"Switch: s1" -down- "Router: r5": r5 eth0
"Switch: s1" -down- "Router: r6": r6 eth0
"Switch: s1" -down- "Router: r7": r7 eth0
"Switch: s1" -down- "Router: r8": r8 eth0
"Switch: s1" -down- "Router: r9": r9 eth0



@enduml
```
