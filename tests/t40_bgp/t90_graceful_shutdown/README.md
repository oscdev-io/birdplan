# BGP graceful shutdown tests

Router r2 should be receiving routes from r1.

For the inbound test the routes should have local_pref set to 0 automatically.

For the outbound test the routes should include the graceful shutdown community.


## Inbound tests

In terms of test "test_graceful_shutdown_inbound_cmdline_global":
- Route r2 is setup from the commandline to globally quarantine all peers.

In terms of test "test_graceful_shutdown_inbound_cmdline":
- Route r2 is setup from the commandline to quarantine just r1.

In terms of test "test_graceful_shutdown_inbound_configfile_global":
- Route r2 is setup from the config file to globally quarantine all peers.

In terms of test "test_graceful_shutdown_inbound_configfile":
- Route r2 is setup from the config file to quarantine just r1.


## Outbound tests

In terms of test "test_graceful_shutdown_outbound_cmdline_global":
- Router r1 is setup from the commandline to globally advertise the GRACEFUL_SHUTDOWN community.

In terms of test "test_graceful_shutdown_outbound_cmdline":
- Router r1 is setup from the commandline to advertise the GRACEFUL_SHUTDOWN community to r2.

In terms of test "test_graceful_shutdown_outbound_configfile_global":
- Router r1 is setup from the config file to globally advertise the GRACEFUL_SHUTDOWN community.

In terms of test "test_graceful_shutdown_outbound_configfile":
- Router r1 is setup from the config file to advertise the GRACEFUL_SHUTDOWN community to r2.


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
