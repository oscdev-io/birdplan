# BGP graceful shutdown tests

Router r2 should be receiving routes from r1.

For the inbound test the routes should have local_pref set to 0 automatically.

For the outbound test the routes should include the graceful shutdown community.


## Test Sets

In terms of test set "t10_inbound_configfile":
- Route r2 is setup from the config file to gracefully shutdown peers globally and explicitly.

In terms of test set "t20_outbound_configfile":
- Route r1 is setup from the config file to gracefully shutdown peers globally and explicitly.

In terms of test set "t30_inbound_cmdline":
- Route r2 is setup from the commandline to gracefully shutdown peers with a pattern and explicitly.

In terms of test set "t40_outbound_cmdline":
- Route r1 is setup from the config file to gracefully shutdown peers with a pattern and explicitly.



## Diagram

```plantuml
@startuml
hide circle
title Test BGP graceful shutdown from r1 to r2


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
