# RIP test for redistribution of the default route


## t10_kernel - Kernel default route tests

r3 should not receive any default routes.

In terms of test "accept_default": **(default)**
  - Router r1 should export the kernel default route to r2, but r2 should not accept it as it does not accept default routes by default.

In terms of test "accept_default_false":
  - Router r1 should export the kernel default route to r2, but r2 should not accept it as it has `accept:default` set to false.

In terms of test "accept_default_true":
  - Router r1 should export the kernel default route to r2, r2 should accept the default route as it has `accept:default` set to true.

In terms of test "redistribute_default": **(default)**
  - Router r1 should not export the kernel default route to r2 as we do not redistribute the default route by default.

In terms of test "redistribute_default_false":
  - Router r1 should not export the kernel default route to r2 as we have `redistribute:kernel_default` set to false.

In terms of test "redistribute_default_true":
  - Router r1 should export the kernel default route to r2 as we have `redistribute:kernel_default` set to true.


## t20_static - Static default route tests

r3 should not receive any default routes.

In terms of test "accept_default": **(default)**
  - Router r1 should export the static default route to r2, but r2 should not accept it as it does not accept default routes by default.

In terms of test "accept_default_false":
  - Router r1 should export the static default route to r2, but r2 should not accept it as it has `accept:default` set to false.

In terms of test "accept_default_true":
  - Router r1 should export the static default route to r2, r2 should accept the default route as it has `accept:default` set to true.

In terms of test "redistribute_default": **(default)**
  - Router r1 should not export the static default route to r2 as we do not redistribute the default route by default.

In terms of test "redistribute_default_false":
  - Router r1 should not export the static default route to r2 as we have `redistribute:static_default` set to false.

In terms of test "redistribute_default_true":
  - Router r1 should export the static default route to r2 as we have `redistribute:static_default` set to true.


## t30_rip - RIP default route tests

r3 should not receive any default routes.

In terms of test "redistribute_rip_default": **(default)**
  - Router r1 should export the static default route to r2 and not redistribute it to r3.

In terms of test "redistribute_rip_default_false":
  - Router r1 should export the static default route to r2 and not redistribute it to r3 as `redistribute:rip_default` is set to false.

In terms of test "redistribute_rip_default_true":
  - Router r1 should export the static default route to r2 and redistribute it to r3 as `redistribute:rip_default` is set to true.


## Diagram

```plantuml
@startuml
hide circle
title RIP test for redistribution of the default route


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. Kernel Routes ..
- 0.0.0.0/0 via 100.101.0.2
- ::/0 via fc00:101::2

  .. Static Routes ..
- 0.0.0.0/0 via 100.101.0.3
- ::/0 via fc00:101::3
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64

  .. Interface: eth1 ..
- 100.102.0.1/24
+ fc00:102::1/64
}

class "Router: r3" {
  .. Interface: eth0 ..
- 100.102.0.2/24
+ fc00:102::2/64
}


class "Switch: s1" {}

class "Switch: s2" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r2" -> "Switch: s2": r2 eth1
"Switch: s2" -> "Router: r3": r3 eth0
"Router: r1" --() NC: r1 eth1

@enduml
```
