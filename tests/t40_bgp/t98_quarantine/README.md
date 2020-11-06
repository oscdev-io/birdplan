# BGP quarantine tests

Router r2 should receive routes from r1.

For the inbound test the routes received should be filtered automatically.

For the outbound test no routes should be advertised.


## Inbound tests

In terms of test "test_quarantine_inbound_cmdline":
- Route r2 is setup from the commandline to quarantine just r1.

In terms of test "test_quarantine_inbound_configfile":
- Route r2 is setup from the config file to quarantine just r1.


## Outbound tests

In terms of test "test_quarantine_outbound_cmdline":
- Router r1 is setup from the commandline to quarantine r2 and should not advertise any routes.

In terms of test "test_quarantine_outbound_configfile":
- Router r1 is setup from the config file to quarantine r2 and should not advertise any routes.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP quarantine from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64

  .. BIRD static routes ..
- 100.101.0.0/24 via 192.168.1.2 (eth1)
+ fc00:101::/48 via fc01::2 (eth1)
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

}

class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Router: r1" --() NC: r2 eth1
"Switch: s1" -> "Router: r2": r2 eth0


@enduml
```
