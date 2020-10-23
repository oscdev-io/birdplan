# BGP redistribution of connected routes


Router r1 should export its connected routes to r2 depending on the test case.

In the case of "redistribute_connected_false_import_connected_true":
  - r1 should import all connected routes into its BGP table but not export them to r2.

In the case of "redistribute_connected_import_connected_true":
  - r1 should import all connected routes into its BGP table but not export them to r2.

In the case of "redistribute_connected_import_connected": **(default)**
  - r1 should not import any connected routes into its BGP table and should not export any to r2.

In the case of "redistribute_connected_true_import_connected_false":
  - r1 should fail to configure with an exception, as importation of connected routes is required.

In the case of "redistribute_connected_true_import_connected_list":
  - r1 should import connected routes from eth1 into its BGP table and export it to r2.

In the case of "redistribute_connected_true_import_connected":
  - r1 should fail to configure with an exception, as importation of connected routes is required.

In the case of "redistribute_connected_true_import_connected_star":
  - r1 should import connected routes from eth1, eth10 into its BGP table and export it to r2.

In the case of "redistribute_connected_true_import_connected_true":
  - r1 should import connected routes from eth0, eth1, eth2, eth10 into its BGP table and export it to r2.


## Diagram

```plantuml
@startuml
hide circle
title Test redistribute connected routes on r1 eth1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::/48

  .. Interface: eth2 ..
- 100.201.0.1/24
+ fc00:201::1/64

  .. Interface: eth10 ..
- 100.211.0.1/24
+ fc00:211::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1
"Router: r1" --() NC: r1 eth2
"Router: r1" --() NC: r1 eth10

@enduml
```
