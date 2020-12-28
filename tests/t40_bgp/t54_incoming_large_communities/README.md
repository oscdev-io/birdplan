# BGP incoming large community tests

In terms of test `test_incoming_large_communities`:
  - Router r1 should be advertising a prefix to router to r2, router r2 should be adding a incoming large community to the prefix it receives.

## Diagram

```plantuml
@startuml
hide circle
title Test BGP incoming large communities from r1 to r2


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "Router: r2" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64

}


class "Switch: s1" {}


"Router: r1" -> "Switch: s1": r1 eth0
"Switch: s1" -> "Router: r2": r2 eth0
"Router: r1" --() NC: r2 eth1

@enduml
```
