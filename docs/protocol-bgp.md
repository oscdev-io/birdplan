# BGP Configuration

Below are configuration options that apply to the BGP protocol.

Remember to set the `router_id`, see [Configuration](configuration.md).



# accept

The `accept` key contains a dictionary of routes we will accept into the master table from our BGP table. Namely...

* `default` - Allows us to accept a default route from BGP. The default is `False`.

Below is a configuration example...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      accept:
        default: True
...
```


# asn

Our BGP ASN. This is mandatory.

One can specify the ASN as per below...
```yaml
router_id: 0.0.0.1

bgp:
  asn: 65000
```


## graceful_shutdown

Add the graceful_shutdown community to all outgoing prefixes for all peers.

This in essence should result in all peers setting their local_pref to 0 for routes we advertise.

We will also ensure that all received routes have a local_pref of 0.

This will result hopefully in traffic being drained from this router.

This is also a peer-specific option (below), which will activate global_shutdown on a single peer.

An example is however below...

```yaml
...

bgp:
  graceful_shutdown: True
  peers:
    peer1:
      asn: 65000
...
```


# import

The `import` key contains a dictionary of the routes to import into the main BGP table.

* `connected` routes are kernel device routes for the interfaces listed. A list of interfaces must be provided. This can be a pattern
like `eth*`.

* `kernel` routes are those statically added to the kernel.

* `static` routes are those setup in the static protocol.


One can specify the ASN as per below...
```yaml
router_id: 0.0.0.1

bgp:
  asn: 65000
  import:
    connected:
      interfaces:
        - eth9
        - ppp*
    static: True
```


# originate

Origination of BGP prefixes, generally we set these to `blackhole` to avoid TTL loops.

Origination can be specified as per below example...
```yaml
...

bgp:
  originate:
    - '100.101.0.0/24 blackhole'
    - 'fc00:101::/48 blackhole'
```


# prefix_import_maxlen4

Default maximum IPv4 prefix length to import from a BGP peer without filtering. Defaults to `24`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_maxlen4: 25
...
```


# prefix_import_minlen4

Default minimum IPv4 prefix length to import from a BGP peer without filtering. Defaults to `8`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_minlen4: 7
...
```


# prefix_export_maxlen4

Default maximum IPv4 prefix length to export to a BGP peer. Defaults to `24`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_maxlen4: 25
...
```


# prefix_export_minlen4

Default minimum IPv4 prefix length to export to a BGP peer. Defaults to `8`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_minlen4: 7
...
```


# prefix_import_maxlen6

Default maximum IPv6 prefix length to import from a BGP peer without filtering. Defaults to `48`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_maxlen6: 47
...
```


# prefix_import_minlen6

Default minimum IPv6 prefix length to import from a BGP peer without filtering. Defaults to `16`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_minlen6: 15
...
```


# prefix_export_maxlen6

Default maximum IPv6 prefix length to export to a BGP peer. Defaults to `48`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_maxlen6: 47
...
```


# prefix_export_minlen6

Default minimum IPv6 prefix length to export to a BGP peer. Defaults to `16`.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_minlen6: 15
...
```


# aspath_import_maxlen

Default maximum AS-PATH length to allow from a BGP peer without filtering. Defaults to `100`.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  aspath_import_maxlen: 90
...
```


# aspath_import_minlen

Default minimum AS-PATH length to allow from a BGP peer without filtering. Defaults to `1`.

You probably NEVER want to change this.

An example of this usage is below...
```yaml
...

bgp:
  aspath_import_minlen: 2
...
```


# community_import_maxlen

Default maximum number of communities before the prefix gets filtered. Defaults to `100`.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  community_import_maxlen: 90
...
```


# extended_community_import_maxlen

Default maximum number of extended communities before the prefix gets filtered. Defaults to `100`.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  extended_community_import_maxlen: 90
...
```


# large_community_import_maxlen

Default maximum number of large communities before the prefix gets filtered. Defaults to `100`.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  large_community_import_maxlen: 90
...
```


# rr_cluster_id

Route reflector cluster ID, this must be specified if we have peers of type `rrclient` or `rrserver-rrserver`.

One can specify the route reflector cluster ID as per below...
```yaml
router_id: 0.0.0.1

bgp:
...
  rr_cluster_id: 0.0.0.1
```



# peers

The `peers` key contains a dictionary of our peers, with the below options.


## asn

The peer ASN. This is mandatory.

An example is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
...
```


## accept

The `accept` key contains a dictionary of routes we will accept. Namely...

* `default` - Allows us to accept a default route from the BGP peer. The default is `False` for everything but a `rrserver-rrserver` peer.
An exception will be raised if this is set to `True` for peers of type `customer`, `peer` and `routeserver`.

Below is a configuration example...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      accept:
        default: True
...
```



## connect_delay_time

Delay in seconds between protocol startup and the first attempt to connect. Default: 5 seconds.

You probably don't want to change this, it is primarily used for testing.

An example is however below...

```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      connect_delay_time: 60
...
```


## connect_retry_time

Time in seconds to wait before retrying a failed attempt to connect. Default: 120 seconds.

You probably don't want to change this.

An example is however below...

```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      connect_retry_time: 60
...
```


## cost

This is the value to reduce the LOCAL_PREF by. Refer to [BGP Appendix](protocol-bgp-appendix.md) for a list of the local preferences.

You need to know exactly what you're doing by setting this, or the result can be disasterous.

This is only supported for peer types of `customer`, `peer`, `routeserver` and `transit`.

An example is however below...

```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      cost: 5
...
```


## description

Description of this peer. This is mandatory.

You can specify the description as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
...
```

## error_wait_time

Minimum and maximum delay in seconds between a protocol failure (either local or reported by the peer) and automatic restart. Doesn't apply when disable after error is configured. If consecutive errors happen, the delay is increased exponentially until it reaches the maximum. Default: 60, 300.

You probably don't want to change this unless you know what you're doing.

An example is however below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      error_wait_time: 120, 900
...
```


## filter

Filtering of routes received from a peer. Options available are below...

* `prefixes` will filter on a list of allowed prefixes
* `origin_asns` will filter on a list of allowed origin ASN's
* `peer_asns` will filter on the first ASN in the AS-PATH, but only really makes sense for `routeserver`.
* `as_sets` will filter on a list of as-sets, resolving them at the same time.

In the context of peer types `customer` and `peer` the above forms the ALLOW list. Everything other than what is specified will be filtered.

In the context of peer types `transit` and `routeserver` the above forms the DENY list. Everything specified will be filtered.

In the context of peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` and `routecollector` the above makes no sense. But will form a DENY list.

An example is however below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      filter:
        as-set: AS-EXAMPLE
        origin_asns:
          - 65009
        peer_asns:
          - 65000
        prefixes:
          - "100.141.0.0/24"
          - "fc00:141::/64"
...
```


## graceful_shutdown

Add the graceful_shutdown community to all outgoing prefixes for this peer.

This in essence should result in the peer setting its local_pref to 0 for routes we advertise.

We will also ensure that all received routes have a local_pref of 0.

This will result hopefully in traffic being drained from this peer.

This is also a global option (above), which will activate global_shutdown on all peers.

An example is however below...

```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      graceful_shutdown: True
...
```


## incoming_large_communities

Large communites to add to incoming prefixes.

You can specify the large communities as a list as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      incoming_large_communities:
        - 65001:5000:1
        - 65001:5000:2
...
```


## location

The location option is used in setting the location-based large communities (route learned), filtering routes to peers in certain locations (location-based selective no-export) and prepending of advertised routes (location-based prepending).

This is only supported for peer types `customer`, `peer`, `routecollector`, `routeserver`, `transit`.

You can specify the peer location using the below configuration...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      location:
        unm49: 999
        iso3166: 999
...
```


## multihop

Configure multihop for a BGP session to a neighbor that isn't directly connected. This is the number of hops it would take to reach the peer.

For iBGP sessions the value defaults to 2.

This should only be specified for iBGP.

You can specify the neighbors address as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      multihop: 2
...
```


## neighbor4

The peers IPv4 address. This option AND/OR the associated `neighbor6` option is mandatory.

You can specify the neighbors address as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      neighbor4: 192.168.0.1
...
```


## neighbor6

The peers IPv6 address. This option AND/OR the associated `neighbor4` option is mandatory.

You can specify the neighbors address as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      neighbor6: fc00::1
...
```


## outgoing_large_communities

**The first method we can use to specify outgoing large communities is just with a list:**

This will result in the large communities being added for all outbound prefixes.

An example of this is below...
```yaml
  peers:
    peer1:
      asn: 65000
      description: Some peer
      outgoing_large_communities:
        - 65000:5000:1
        - 65000:5000:2
```

**The second method is we can use a dict to do fine grained outgoing large communities based on route type:**

Route types...

* `default` will match the default route.
* `connected` will match connected routes.
* `static` will match static routes. This will not match default routes.
* `kernel` will match kernel routes. This will not match default routes.
* `originated` will match originated routes. This will not match default routes.

Internal route types...

* `bgp` will match all BGP routes.
* `bgp_own` will match BGP routes that originated from our ASN.
* `bgp_customer` will match our customer routes.
* `bgp_peering` will match our peers routes.
* `bgp_transit` will match our transit providers routes.

An example of this is below...
```yaml
  peers:
    peer1:
      asn: 65000
      description: Some peer
      outgoing_large_communities:
        static:
          - 65000:5000:1
        bgp_customer:
          - 65000:5000:2
```


# passive

Set the BGP session to passive or non-passive.

This defaults to `True` for `customer` and `rrclient` peer types and `False` for all other peer types.

```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      passive: True
...
```


## password

BGP session password. You probably want to add quotes around any non-alphanumeric characters.

An example of using the password option is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      password: "test123"
...
```


## prefix_limit4

IPv4 prefix limit for the peer. This is only supported for peer types `customer` and `peer`.

An example of specifying a prefix limit is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prefix_limit4: 100
...
```


## prefix_limit6

IPv6 prefix limit for the peer. This is only supported for peer types `customer` and `peer`.

An example of specifying a prefix limit is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prefix_limit6: 100
...
```


# prefix_import_maxlen4

Maximum IPv4 prefix length to import without filtering. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_maxlen4: 25
...
```


# prefix_import_minlen4

Minimum IPv4 prefix length to import without filtering. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_minlen4: 7
...
```


# prefix_export_maxlen4

Maximum IPv4 prefix length to export. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_maxlen4: 25
...
```


# prefix_export_minlen4

Minimum IPv4 prefix length to export. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_minlen4: 7
...
```


# prefix_import_maxlen6

Maximum IPv6 prefix length to import without filtering. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_maxlen6: 47
...
```


# prefix_import_minlen6

Minimum IPv6 prefix length to import without filtering. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_import_minlen6: 15
...
```


# prefix_export_maxlen6

Maximum IPv6 prefix length to export. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_maxlen6: 47
...
```


# prefix_export_minlen6

Minimum IPv6 prefix length to export. Defaults to global setting.

An example of this usage is below...
```yaml
...

bgp:
  prefix_export_minlen6: 15
...
```


# aspath_import_maxlen

Maximum AS-PATH length to allow without filtering. Defaults to global setting.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  aspath_import_maxlen: 90
...
```


# aspath_import_minlen

Minimum AS-PATH length to allow without filtering. Defaults to global setting.

You probably NEVER want to change this.

An example of this usage is below...
```yaml
...

bgp:
  aspath_import_minlen: 2
...
```


# community_import_maxlen

Maximum number of communities before the prefix gets filtered. Defaults to global setting.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  community_import_maxlen: 90
...
```


# extended_community_import_maxlen

Maximum number of extended communities before the prefix gets filtered. Defaults to global setting.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  extended_community_import_maxlen: 90
...
```


# large_community_import_maxlen

Maximum number of large communities before the prefix gets filtered. Defaults to global setting.

You probably only want to change this if you know exactly what you're doing!

An example of this usage is below...
```yaml
...

bgp:
  large_community_import_maxlen: 90
...
```







## prepend

This option controls AS-PATH prepending in various ways. The prepending count must be between 1 and 10.

NOTE: Currently our own ASN will be prepended. Support for the first AS is not yet added.

**The first method we can use to specify outbound prepending is just with a number:**

This will result in our own ASN being prepended for the number of times specified.

An example of this is below...
```yaml
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prepend: 2
```

**The second method is we can use a dict to do fine grained prepending based on route type:**

Route types...

* `default` will match the default route.
* `connected` will match connected routes.
* `static` will match static routes. This will not match default routes.
* `kernel` will match kernel routes. This will not match default routes.
* `originated` will match originated routes. This will not match default routes.

Internal route types...

* `bgp` will match all BGP routes.
* `bgp_own` will match BGP routes that originated from our ASN.
* `bgp_customer` will match our customer routes.
* `bgp_peering` will match our peers routes.
* `bgp_transit` will match our transit providers routes.

An example of this is below...
```yaml
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prepend:
        static: 2
        bgp_customer: 2
```


## quarantine

Quarantine all the peer routes by filtering them out and blocking transversal into the bgp table.

An example of quarantining a peer can be found below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Bad peer
      quarantine: True
...
```


## redistribute

Types of routes to redistribute to the peer, valid options are detailed below...

* `default` will redistribute the default route, the type of route also needs to be redistributed. eg. `static`. Defaults to `False` except
for peer type `rrserver-rrserver` which defaults to `True`.
* `connected` will redistribute connected routes. Defaults to `False`.
* `static` will redistribute static routes in our global static configuration. Defaults to `False`.
* `kernel` will redistribute kernel routes. Defaults to `False`.
* `originated` will redistribute originated routes. Defaults to `False`.

In addition to setting these as a boolean value, one can also add the following items to a dictionary...
* `large_communities` will add additional large communities when exporting routes of this type

Internal redistribution options and how they are used... (do not use unless you know exactly you're doing)

* `bgp` will redistribute BGP routes. Automatically set to `True` for peer types of `rrclient`, `rrserver` and `rrserver-rrserver`.
* `bgp_own` will redistribute our own BGP routes based on an internal large community `OWN_ASN:3:1`. Automatically set to `True` for peer types of `customer`, `routecollector`, `routeserver`, `peer` and `upstream`.
* `bgp_customer` will redistribute our customers BGP routes based on an internal large community `OWN_ASN:3:2`. Automatically set to `True` for peer types of `customer`, `routecollector`, `routeserver`, `peer` and `upstream`.
* `bgp_peering` will redistribute peering session routes based on an internal large community `OWN_ASN:3:3`. Automatically set to `True` for peer types of `customer`.
* `bgp_transit` will redistribute transit routes based on an internal large community `OWN_ASN:3:4`. Automatically set to `True` for peer types of `customer`.

An example of using redistribute can be found below...
```yaml
...

bgp:
  originate:
    - '100.101.0.0/24 blackhole'
    - 'fc00:101::/48 blackhole'
  peers:
    peer1:
      asn: 65000
      description: Some peer
      redistribute:
        originated: True
...
```


## replace_aspath

Replace the advertised routes AS-PATH with our own ASN.

This is only valid for peer types of `customer` and `internal`.

This will result in a large community being added to the prefix, which will end up in the AS-PATH being replaced on all eBGP peers.

All private ASN's will be replaced up to a limit of 10, any AS-PATH longer than this will be truncated.

In addition to this functionality, the minimum and maximum prefix lengths we import and export are adjusted as follows. This allows a peer using this feature to advertise a /29 IPv4 and /64 IPv6 prefix to us.
```
prefix_import_minlen4 = 16
prefix_import_maxlen4 = 29
prefix_export_minlen4 = 16
prefix_export_maxlen4 = 29
prefix_import_maxlen6 = 64
prefix_import_minlen6 = 32
prefix_export_maxlen6 = 64
prefix_export_minlen6 = 32
```

An example is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      replace_aspath: True
...
```


## source_address4

The source IPv4 address we'll be using to connect to this peer.

You can specify the source address as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      source_address4: 192.168.0.2
...
```

## source_address6

The source IPv6 address we'll be using to connect to this peer.

You can specify the source address as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      source_address6: fc00::2
...
```


## type

The peer type, options are detailed below...

* `customer` this is a customer peering session.
* `internal` this is an internal peering session between routers.
* `peer` this is a peering partner peering session.
* `routecollector` this is a route collector session.
* `routeserver` this is a route server session.
* `rrclient` this is a route reflector client peering session.
* `rrserver` this is a route reflector server peering session.
* `rrserver-rrserver` this is a peering session between two route reflectors or route reflector mirrors.
* `transit` this is a transit provider peering session.
