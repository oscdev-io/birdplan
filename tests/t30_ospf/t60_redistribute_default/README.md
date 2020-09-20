# OSPF test for redistribution of the default route


In terms of test "redistribute_only_default_with_kernel":
  - Router r1 should not export the kernel default route to r2 as we don't have redistribute kernel routes.

In terms of test "redistribute_only_default_with_static":
  - Router r1 should not export the static default route to r2 as we don't have redistribute static routes.

In terms of test "redistribute_kernel_without_default":
  - Router r1 should not export the kernel default route to r2 as we don't have redistribute default routes.

In terms of test "redistribute_static_without_default":
  - Router r1 should not export the static default route to r2 as we don't have redistribute default routes.

In terms of test "redistribute_kernel_default_without_accept":
  - Router r1 should export the kernel default route to r2, but r2 should not accept it as it does not accept default routes.

In terms of test "redistribute_static_default_without_accept":
  - Router r1 should export the static default route to r2, but r2 should not accept it as it does not accept default routes.

In terms of test "redistribute_kernel":
  - Router r1 should export the kernel default route to r2, r2 should accept the default route as it accepts default routes.

In terms of test "redistribute_static":
  - Router r1 should export the static default route to r2, r2 should accept the default route as it accepts default routes.


```plantuml
@startuml
hide circle
title OSPF test for redistribution of the default route
left to right direction


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
- fc00:100::1/64

  .. Interface: eth1 ..
- 100.101.0.1/24
+ fc00:101::1/64

  .. Kernel/Static Routes ..
- 0.0.0.0/0 via 100.101.0.2 (eth1)
- ::/0 via fc00:101::2 (eth1)
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
- fc00:100::2/64
}



class "Switch: s1" {}


"Switch: s1" -- "Router: r1": r1 eth0
"Switch: s1" -- "Router: r2": r2 eth0
"Router: r1" --() NC: r1 eth1

@enduml
```
