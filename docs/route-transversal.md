# Route Transversal


```plantuml
@startuml
hide circle
title BirdPlan Route Transversal



class "Table: static" {
  .. Imports ..
- Statically defined routes
  .. Exports ..
+ All routes to master
}

class "Table: direct" {
  .. Imports ..
- All connected routes
  .. Exports ..
+ All routes to master
}

Package OSPF <<Folder>> {
    class "Table: ospf" {
    .. Imports ..
    - All routes from OSPF adjacencies
    - From master based on filters
    .. Exports ..
    + To master based on filters
    }

    class "Table: ospf_direct" {
    .. Imports ..
    - Connected routes from interface match
    .. Exports ..
    + To OSPF table if redistribute:connected
    }
}

Package RIP <<Folder>> {
    class "Table: rip" {
    .. Imports ..
    - All routes from RIP adjacencies
    - From master based on filters
    .. Exports ..
    + To RIP adjacencies based on filters
    + To master based on filters
    }

    class "Table: rip_direct" {
    .. Imports ..
    - Connected routes from interface match
    .. Exports ..
    + To OSPF table if redistribute:connected
    }
}


Package BGP <<Folder>> {

    class "Table: bgp" {
    .. Imports ..
    - Based on filters
    .. Exports ..
    + Based on filters
    }

    class "Table: bgp_direct" {
    .. Imports ..
    - Connected routes from interface match
    .. Exports ..
    + To BGP table if redistribute:connected
    }

    class "Table: bgp_originate" {
    .. Imports ..
    - Statically defined origination routes
    .. Exports ..
    + To BGP table if redistribute:originated
    }

    class "Table: bgp_XXX_peer" {
    .. Imports ..
    - From BGP table based on filters
    .. Exports ..
    + To BGP table based on filters
    }
}


class "Table: master" {
  .. Imports ..
- All
  .. Exports ..
+ All
}


class "Table: kernel" {
  .. Imports ..
- All kernel routes from kernel
- Routes from master based on filters
  .. Exports ..
+ All
}


class "OS: FIB" {
  .. Imports ..
- All
  .. Exports ..
+ All
}




"Table: master" <-up-> "Table: ospf"
"Table: master" <-up-> "Table: rip"
"Table: master" <-up-> "Table: bgp"

"Table: static" -> "Table: master"
"Table: master" <- "Table: direct"

"Table: ospf_direct" -> "Table: ospf"
"Table: rip_direct" -> "Table: rip"

"Table: bgp" <- "Table: bgp_originate"
"Table: bgp_direct" -> "Table: bgp"
"Table: bgp_XXX_peer" <-down-> "Table: bgp"

"Table: kernel" <-up-> "Table: master"
"OS: FIB" <-up-> "Table: kernel"


@enduml
```

# Internal Route Preferences

|  Protocol  |  Pref  |  Description  |
|------------|--------|---------------|
| Direct | 240 | Directly connected interface routes |
| Static | 200 | Statically configured routes |
| Static (originated) | 195 | Originated routes (BirdPlan) |
| OSPF | 150 | IGP; for OSPF intra-area, inter-area and type 1 external routes |
| Babel | 130 | IGP |
| RIP | 120 | IGP |
| BGP | 100 | EGP |
| RPKI | 100 | RPKI routes |
| Inheriteed | 10	 | Routes inherited from other routing daemons |
