# Basic BGP test

ExaBGP e1 should be announcing its route to r1 for testing each peer type.

In terms of test "test_bgp":  (default configuration)
  - Router r1 should install BGP routes into OS RIB.

In terms of test "test_export_kernel_bgp_false": (export_kernel:bgp set to False)
  - Router r1 should not install BGP routes into OS RIB.

In terms of test "test_export_kernel_bgp_true": (export_kernel:bgp set to True)
  - Router r1 should install BGP routes into OS RIB.


```plantuml
@startuml
hide circle
title Test for basic BGP routing


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64
}


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64

  .. BGP Announce ..
- 100.64.101.0/24 next-hop 100.101.0.2
- fc00:101::/48 next-hop fc00:101::2
}



class "Switch: s1" {}

"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0


@enduml
```
