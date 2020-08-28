# BGP quarantine feature

Router r1 should be populating the BGP peering table with routes we would export, but not actually export them to r2.
Router r1 should be adding the `ASN:FILTERED:QUARANTINED` community to the incoming routes in the BGP peering table and should not be propagating them to the main BGP table as they're filtered.
Router r2 should be exporting its routes to r1.

## Goals
 - Tag all inbound routes with `ASN:FILTERED:QUARANTINED`
 - Show what routes would be exported, but not export them


```plantuml
@startuml
hide circle
title Test qurantined BGP session
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 192.168.1.1/24
+ fc01::1/64

  .. BIRD static routes ..
- 100.101.0.0/24 via 192.168.1.2 (eth1)
+ fc00:101::/48 via fc01::2 (eth1)

  .. BGP ..
* AS65000
}
note top: Should quarantine routes received by \n r2 and not export routes to r2


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

  .. Interface: eth1 ..
- 192.168.2.1/24
+ fc02::1/64

  .. BIRD static routes ..
- 100.102.0.0/24 via 192.168.2.2 (eth1)
+ fc00:102::/48 via fc02::2 (eth1)

  .. BGP ..
* AS65001
}
note top: Should export routes to r1 but should \n not receive any routes from r1


class "Switch: s1" {}


"Switch: s1" <-down- "Router: r1": r1 eth0
"Switch: s1" <-down- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r2" --() NC: r2 eth1

@enduml
```
