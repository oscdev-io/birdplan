# BGP Configuration

Below are configuration options that apply to the BGP protocol.

Remember to set the `router_id`, see [Configuration](configuration.md).



## type

The peer type, options are detailed below... this option is mandatory.

* `customer` this is a customer peering session.
* `internal` this is an internal peering session between routers.
* `peer` this is a peering partner peering session.
* `routecollector` this is a route collector session.
* `routeserver` this is a route server session.
* `rrclient` this is a route reflector client peering session.
* `rrserver` this is a route reflector server peering session.
* `rrserver-rrserver` this is a peering session between two route reflectors or route reflector mirrors.
* `transit` this is a transit provider peering session.

Below is a configuration example...
```yaml
...

bgp:
  asn: 65000
  peers:
    peer1:
      asn: 65000
      type: internal
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



# accept

The `accept` key contains a dictionary of routes we will accept into the master table from our BGP table. Namely...

* `originated` - Allows us to accept originated routes from the BGP table. The default is `True`.
* `originated_default` - Allows us to accept locally originated routes from the BGP table. The default is `False`.

* `bgp_customer_blackhole` - Allows us to accept a blackhole route that originated from a customer. The default is `True`.
* `bgp_own_blackhole` - Allows us to accept a blackhole route that originated from our own federation. The default is `True`.

* `bgp_own_default` - Allows us to accept a default route that originated from within our own federation from the BGP peer.
  The default is `False` for all peer types except a `rrserver-rrserver` peer.
* `bgp_transit_default` - Allows us to accept a default route that originated from a transit peer.
  The default is `False` for all peer types except a `rrserver-rrserver` peer.


Below is a configuration example...
```yaml
...

bgp:
  asn: 65000
  peers:
    peer1:
      asn: 65000
      type: internal
      accept:
        default: True
...
```



# graceful_shutdown

Add the graceful_shutdown community to all outgoing prefixes for all peers.

This in essence should result in all peers setting their local_pref to 0 for routes we advertise.

We will also ensure that all received routes have a local_pref of 0.

This will result hopefully in traffic being drained from this router.

This is also a peer-specific option (below), which will activate global_shutdown on a single peer.

An example is however below...

```yaml
...

bgp:
  asn: 65000
  graceful_shutdown: True
  peers:
    peer1:
      asn: 65000
      type: internal
...
```



# import

The `import` key contains a dictionary of the routes to import into the main BGP table.

* `connected` routes are kernel device routes for the interfaces listed. A list of interfaces must be provided. This can be a pattern
like `eth*`. Connected routes are not imported by default..

* `kernel` routes are those added to the kernel, excluding blackhole and default routes. The default for this option is `False`.

* `kernel_blackhole` routes are those statically added to the kernel which are blackhole routes. This option is independant of the `kernel` option above and will only import blackhole routes. The default for this option is `False`.

* `kernel_default` routes are those added to the kernel. This option is independant of the `kernel` option above and will only import kernel default routes. The default for this option is `False`.

* `static` routes are those setup in the static protocol, excluding blackhole and default routes. The default for this option is `False`.

* `static_blackhole` routes are those setup in the static protocol which are blackhole routes. This option is independant of the `static` option above and will only import blackhole routes. The default for this option is `False`.

* `static_default` routes are those setup in the static protocol. This option is independant of the `static` option above and will only import static default routes. The default for this option is `False`.


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

When the destination is set as a `blackhole`, an additional large community (OWN_ASN, 1200, 2) will be added. This will result
in all iBGP peers blackholing the originated range.

Origination can be specified as per below example...
```yaml
...

bgp:
  originate:
    - '100.101.0.0/24 blackhole'
    - 'fc00:101::/48 blackhole'
  ...
```

Attributes can also be added to originated routes for instance...
```yaml
bird:
  originate:
    - '100.101.0.0/24 blackhole { bgp_large_community.add(65000, 111, 222) }'
  ...
```



# peertype_constraints

This configuration key can be used to override the global constraints in place for each of the peer types.

## Valid peer types
* `customer`
* `customer.private` - This is a special peer type used when a `customer` peer type has a private ASN which is translated to our
own ASN on eBGP export (ie. the `replace_aspath` is specified).
* `internal`
* `peer`
* `routecollector`
* `routeserver`
* `rrclient`
* `rrserver`
* `rrserver-rrserver`
* `transit`


## Prefix size limits

* `import_maxlen4`

Maximum IPv4 import prefix length, defaults to `24`
except for `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` which defaults to `32`
and `customer.private` which defaults to `29`.

* `import_minlen4`

Minimum IPv4 import prefix length, defaults to `8`
except for `customer.private` which defaults to `16`.

* `export_maxlen4`

Maximum IPv4 export prefix length, defaults to `24`
except for `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` which defaults to `32`
and `customer.private` which defaults to `29`.

* `export_minlen4`

Minimum IPv4 export prefix length, defaults to `8`
except for `customer.private` which defaults to `16`.

* `import_maxlen6`

Maximum IPv6 import prefix length, defaults to `48`
except for `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` which defaults to `128`
and `customer.private` which defaults to `64`.

* `import_minlen6`

Minimum IPv6 import prefix length, defaults to `16`
and `customer.private` which defaults to `32`.

* `export_maxlen6`

Maximum IPv6 export prefix length, defaults to `48`
except for `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` which defaults to `128`
and `customer.private` which defaults to `64`.

* `export_minlen6`

Minimum IPv6 export prefix length, defaults to `16`
and `customer.private` which defaults to `32`.


## Blackhole size limits

* `blackhole_import_maxlen4`

Blackhole maximum IPv4 import prefix length, defaults to `32`.

* `blackhole_import_minlen4`

Blackhole minimum IPv4 import prefix length, defaults to `24`.

* `blackhole_export_maxlen4`

Blackhole maximum IPv4 export prefix length, defaults to `32`.

* `blackhole_export_minlen4`

Blackhole minimum IPv4 export prefix length, defaults to `24`.

* `blackhole_import_maxlen6`

Blackhole maximum IPv6 import prefix length, defaults to `128`.

* `blackhole_import_minlen6`

Blackhole minimum IPv6 import prefix length, defaults to `64`.

* `blackhole_export_maxlen6`

Blackhole maximum IPv6 export prefix length, defaults to `128`.

* `blackhole_export_minlen6`

Blackhole minimum IPv6 export prefix length, defaults to `64`.


## AS-PATH length limits

* `aspath_import_maxlen` - AS-PATH import maximum length, defaults to `100`.

* `aspath_import_minlen` - AS-PATH import minimum length, defaults to `1`
except for `internal`, `rrclient`, `rrserver`, `rrserver-rrserver` which defaults to `0`.


## Community length limits

* `community_import_maxlen` - Community import maximum length, defaults to `100`.

* `extended_community_import_maxlen` - Extended community import maximum length, defaults to `100`.

* `large_community_import_maxlen` - Large community import maximum length, defaults to `100`.


An example of setting the global defaults for a specific peer type can be found below...
```yaml
...

bgp:
  peertype_constraints:
    customer:
      import_maxlen4: 25
...
```



# rr_cluster_id

Route reflector cluster ID, this must be specified if we have peers of type `rrclient` or `rrserver-rrserver`.

One can specify the route reflector cluster ID as per below...
```yaml
router_id: 0.0.0.1

bgp:
  rr_cluster_id: 0.0.0.1
  ...
```



# peers

The `peers` key contains a dictionary of our peers, with the below options.


## asn

The peer ASN. This is mandatory.

An example is below...
```yaml
...

bgp:
  ...
  peers:
    peer1:
      asn: 65000
      type: internal
  ...
```



## accept

The `accept` key contains a dictionary of routes we will accept. Namely...

* `bgp_customer_blackhole` - Allows us to accept a blackhole route that originated from a customer.
  This is only valid for peer types `customer`, `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.
  The default is `True` for peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.
  The default is `True` for peer type `customer` when `filter:prefixes` is set.

* `bgp_own_blackhole` - Allows us to accept a blackhole route that originated from our own federation.
  This is only valid for peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.
  The default is `True` for peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.

* `bgp_own_default` - Allows us to accept a default route that originated from our own federation.
  This is only valid for peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.
  The default is `True` for peer type `rrserver-rrserver`.

* `bgp_transit_default` - Allows us to accept a default route that originated from a transit peer.
  The is `True` for peer type `rrserver-rrserver`.

Below is a configuration example...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      accept:
        default: True
  ...
```


## blackhole_community

Set the peers blackhole community. When this option is specified blackhole routes with the large community action
`(OWN_ASN, 666, XXX)` will result in the blackhole route being propagated to the specified peer(s).

The only peer type supported for this option is `transit`, `routeserver` and `routecollector`.

This value of this option can either be:
  - a normal community in the format of 'XXXX:YYYY'; or
  - a large community in the format of 'XXXX:YYYY:ZZZZ'; or
  - boolean of `True` or `False`, in this case the well-known community `(65535, 666)` will be propagated if `True`.

Below is a configuration example using a normal community...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      blackhole_community: 65000:100
  ...
...
```

Below is a configuration example using a large community...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      blackhole_community: 65000:100:100
  ...
```

Below is a configuration example using a boolean...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      blackhole_community: True
  ...
```


## connect_delay_time

Delay in seconds between protocol startup and the first attempt to connect. Default: 5 seconds.

You probably don't want to change this, it is primarily used for testing.

An example is however below...

```yaml
...

bgp:
  ...
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
  ...
  peers:
    peer1:
      asn: 65000
      connect_retry_time: 60
  ...
```


## constraints

This configuration key can be used to override the global peer type constraints.
All values default to the global setting for the specific peer type (above).


### Normal prefix size limits

* `import_maxlen4` - maximum IPv4 import prefix length.
* `import_minlen4` - minimum IPv4 import prefix length.
* `export_maxlen4` - maximum IPv4 export prefix length.
* `export_minlen4` - minimum IPv4 export prefix length.
* `import_maxlen6` - maximum IPv6 import prefix length.
* `import_minlen6` - minimum IPv6 import prefix length.
* `export_maxlen6` - maximum IPv6 export prefix length.
* `export_minlen6` - minimum IPv6 export prefix length.


### Blackhole prefix size limits

* `blackhole_import_maxlen4` - blackhole maximum IPv4 import prefix length.
* `blackhole_import_minlen4` - blackhole minimum IPv4 import prefix length.
* `blackhole_export_maxlen4` - blackhole maximum IPv4 export prefix length.
* `blackhole_export_minlen4` - blackhole minimum IPv4 export prefix length.
* `blackhole_import_maxlen6` - blackhole maximum IPv6 import prefix length.
* `blackhole_import_minlen6` - blackhole minimum IPv6 import prefix length.
* `blackhole_export_maxlen6` - blackhole maximum IPv6 export prefix length.
* `blackhole_export_minlen6` - blackhole minimum IPv6 export prefix length.


### AS-PATH length limits

* `aspath_import_maxlen` - AS-PATH import maximum length.
* `aspath_import_minlen` - AS-PATH import minimum length.


### Community length limits

* `community_import_maxlen` - Community import maximum length.
* `extended_community_import_maxlen` - Extended community import maximum length.
* `large_community_import_maxlen` - Large community import maximum length.


An example of overriding a constraint can be found below...
```yaml
..

bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      constraints:
        import_maxlen4: 25
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
  ...
  peers:
    peer1:
      asn: 65000
      cost: 5
  ...
```


## add_paths

Supported in: 0.0.3

ADD-PATH is the BGP capability described in RFC5492 which enables the sending/receiving (or both) of multiple paths for the same
prefix.

Valid values are `tx`, `rx` and `on`.

This is only supported for peer types of `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`.

An example is however below...

```yaml
...

bgp:
  ...
  peers:
    peer1:
      asn: 65000
      add_paths: on
  ...
```


## description

Description of this peer. This is mandatory.

You can specify the description as per below...
```yaml
...

bgp:
  ...
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
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      error_wait_time: 120, 900
  ...
```


## import_filter (alias: filter)

(The 'import_filter' key is supported from version v0.0.20)

Filtering of routes received from a peer. Options available are below...

* `prefixes` will filter on a list of allowed prefixes.
* `aspath_asns` will filter on a list of ASNs in the AS-PATH.
* `origin_asns` will filter on a list of allowed origin ASN's.
* `peer_asns` will filter on the first ASN in the AS-PATH, but only really makes sense for `routeserver`.
* `as_sets` will filter on a list of as-sets, resolving them at the same time. This only makes sense for `customer` and `peer`.

In the context of peer types `customer` and `peer`...

* The above forms the ALLOW list. Everything other than what is specified will be filtered.
* When specifing `as_sets`, the `origin_asns` and `aspath_asns` will be populated with the IRR ASN list.
* When specifying `origin_asns`, the `aspath_asns` filter will be populated with `origin_asns` and the peer ASN.

In the context of peer types `transit` and `routeserver`:

* The above forms the DENY list. Everything specified will be filtered.
* When specifing `as_sets`, the `origin_asns` will be populated with the IRR ASN list.
* When specifying `aspath_asns` if any of the ASNs are within the path, the prefix will be filtered.

In the context of peer types `internal`, `rrclient`, `rrserver`, `rrserver-rrserver`:

* The above forms the DENY list. Everything specified will be filtered.
* When specifing `as_sets`, the `origin_asns` will be populated with the IRR ASN list.
* When specifying `aspath_asns` if any of the ASNs are within the path, the prefix will be filtered.

Examples of `prefixes` filter:
* `192.168.0.0/22+` - Matches /22 or any subset of the /22
* `192.168.0.0/24` - Matches exactly /24

Currently only the above two methods of specifying IP ranges are accepted.

The prefix sizes are controlled by the prefix and blackhole length constraints, so one does not need to specify the min and max sizes here.

An example is however below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      import_filter:
        as_sets: AS-EXAMPLE
        origin_asns:
          - 65009
        peer_asns:
          - 65000
        prefixes:
          - "100.141.0.0/24"
          - "fc00:141::/64"
  ...
```


## export_filter

Supported in: v0.0.20+

Filtering of routes advertised to a peer. Options available are below...

* `prefixes` will filter out the list of specified prefixes from being advertised.
* `origin_asns` will filter out the list of origin ASN's from being advertised.

Examples of `prefixes` filter:
* `192.168.0.0/22+` - Matches /22 or any subset of the /22
* `192.168.0.0/24` - Matches exactly /24

Currently only the above two methods of specifying IP ranges are accepted.

An example is however below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      export_filter:
        origin_asns:
          - 65009
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
  ...
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
  ...
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
  ...
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
  ...
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
bgp:
  ...
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
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      neighbor6: fc00::1
  ...
```


## outgoing_large_communities

This option allows us to set outgoing large communites in two methods listed below.

**The first method we can use to specify outbound large communites is just list of communites:**

This will result in `65000:99:98` and `65000:99:99` being added to all outgoing prefixes.

An example of this is below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      outgoing_large_communites:
        - 65000:99:98
        - 65000:99:99
  ...
```

**The second method is we can use a dict to do fine grained adding of communites based on route type:**

Route types...

* `blackhole` will set the default value for all *_blackhole options.
* `default` will set the default value for all *_default options.
* `connected` will match connected routes.
* `kernel` will match kernel routes. This will also set the default for all kernel_* options.
* `kernel_blackhole` will match kernel blackhole routes.
* `kernel_default` will match kernel default routes.
* `static` will match static routes. This will also set the default for all static_* options.
* `static_blackhole` will match static blackhole routes.
* `static_default` will match static default routes.
* `originated` will match originated routes. This will also set the default for all originated_* options.
* `originated_default` will match originated routes default routes.

Internal route types...

* `bgp` will set the default value for all bgp_* options.
* `bgp_blackhole` will set the default value for all bgp_*_blackhole options.
* `bgp_default` will set the default value for all bgp_*_default options.
* `bgp_own` will match BGP routes that originated from our ASN. This will also set the default for all bgp_own_* options.
* `bgp_own_blackhole` will match BGP blackhole routes that originated from our ASN.
* `bgp_own_default` will match BGP default routes that originated from our ASN.
* `bgp_customer` will match our customer routes. This will set the default for all bgp_customer_* options.
* `bgp_customer_blackhole` will match BGP blackhole routes received from customers.
* `bgp_peering` will match our peers routes.
* `bgp_transit` will match our transit providers routes. This will set the default for all bgp_transit_* options.
* `bgp_transit_default` will match BGP default routes received from transit providers.


An example of this is below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      outgoing_large_communities:
        static:
          - 65000:99:98
        bgp_customer:
          - 65000:99:99
  ...
```


# passive

Set the BGP session to passive or non-passive.

This defaults to `True` for `customer` and `rrclient` peer types and `False` for all other peer types.

```yaml
...

bgp:
  ...
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
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      password: "test123"
  ...
```


## ttl_security

Supported in version: 0.0.17+

Enable TTL security on the BGP session.

An example of enabling TTL security is below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      ttl_security: true
  ...
```


## prefix_limit4

IPv4 prefix limit for the peer. This is only supported for peer types `customer` and `peer`.

An example of specifying a prefix limit is below...
```yaml
bgp:
  ...
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
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prefix_limit6: 100
  ...
```


## prepend

This option controls AS-PATH prepending in various ways. The prepending count must be between 1 and 10.

NOTE: Currently our own ASN will be prepended. Support for the first AS is not yet added.

**The first method we can use to specify outbound prepending is just with a number:**

This will result in our own ASN being prepended for the number of times specified.

An example of this is below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prepend: 2
  ...
```

**The second method is we can use a dict to do fine grained prepending based on route type:**

Route types...

* `blackhole` will set the default value for all *_blackhole options.
* `default` will set the default value for all *_default options.
* `connected` will match connected routes.
* `kernel` will match kernel routes. This will also set the default for all kernel_* options.
* `kernel_blackhole` will match kernel blackhole routes.
* `kernel_default` will match kernel default routes.
* `static` will match static routes. This will also set the default for all static_* options.
* `static_blackhole` will match static blackhole routes.
* `static_default` will match static default routes.
* `originated` will match originated routes. This will also set the default for all originated_* options.
* `originated_default` will match originated routes default routes.

Internal route types...

* `bgp` will set the default value for all bgp_* options.
* `bgp_blackhole` will set the default value for all bgp_*_blackhole options.
* `bgp_default` will set the default value for all bgp_*_default options.
* `bgp_own` will match BGP routes that originated from our ASN. This will also set the default for all bgp_own_* options.
* `bgp_own_blackhole` will match BGP blackhole routes that originated from our ASN.
* `bgp_own_default` will match BGP default routes that originated from our ASN.
* `bgp_customer` will match our customer routes. This will set the default for all bgp_customer_* options.
* `bgp_customer_blackhole` will match BGP blackhole routes received from customers.
* `bgp_peering` will match our peers routes.
* `bgp_transit` will match our transit providers routes. This will set the default for all bgp_transit_* options.
* `bgp_transit_default` will match BGP default routes received from transit providers.

An example of this is below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prepend:
        static: 2
        bgp_customer: 2
  ...
```


## quarantine

Quarantine all the peer routes by filtering them out and blocking transversal into the bgp table.

An example of quarantining a peer can be found below...
```yaml
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Bad peer
      quarantine: True
  ...
```


## redistribute

Types of routes to redistribute to the peer, valid options are detailed below...

Locally originated route redistribution...

* `connected` will redistribute connected routes. Defaults to `False`.
* `kernel` will redistribute kernel routes. Defaults to `False`.
* `kernel_blackhole` will redistribute kernel blackhole routes. Defaults to `False`. If set to True, kernel blackhole routes will
  be redistributed regardless of the blackhole large community function value.
* `kernel_default` will redistribute kernel default routes. Defaults to `False`.
* `static` will redistribute static routes in our global static configuration. Defaults to `False`.
* `static_blackhole` will redistribute static blackhole routes in our global static configuration. Defaults to `False`. If set to
  True, static blackhole routes will be redistributed regardless of the blackhole large community function value.
* `static_default` will redistribute static default routes. Defaults to `False`.
* `originated` will redistribute originated routes. Defaults to `False`.
* `originated_default` will redistribute originated default routes. Defaults to `False`.

BGP "all" route redistribution...

* `bgp` will set the default option for all bgp_* options if specified. If set to `False`, one can then individually enable redistribution of various types of BGP routes using the options below. Setting this option to `True` will be pointless as
it will just result in the defaults being used.

BGP route source redistribution...

* `bgp_own` will redistribute our own BGP routes based on an internal large community `OWN_ASN:3:1`. This will set the default value for `bgp_own_blackhole` and `bgp_own_default` to `False` if explicitly set to `False`.
Defaults to `True` for peer types of `customer`, `routecollector`, `routeserver`, `peer` and `upstream`.
* `bgp_customer` will redistribute our customers BGP routes based on an internal large community `OWN_ASN:3:2`. This will set the default value
for `bgp_customer_blackhole` to `False` if explicitly set to `False`.
Defaults to `True` for peer types of `customer`, `routecollector`, `routeserver`, `peer` and `upstream`.
* `bgp_peering` will redistribute peering session routes based on an internal large community `OWN_ASN:3:3`.
Defaults to `True` for peer types of `customer`.
* `bgp_transit` will redistribute transit routes based on an internal large community `OWN_ASN:3:4`. This will set the default value
for `bgp_transit_default` to `False` if explicitly set to `False`.
Defaults to `True` for peer types of `customer`.

BGP blackhole redistribution...

* `bgp_customer_blackhole` will redistribute BGP default routes. Defaults to `True` for peer types `internal`, `routecollector`, `routeserver`, `rrclient`, `rrserver`, `rrserver-rrserver`, `transit`.
* `bgp_own_blackhole` will redistribute BGP default routes. Defaults to `True` for peer types `internal`, `routecollector`, `routeserver`, `rrclient`, `rrserver`, `rrserver-rrserver`, `transit`.

BGP default route redistribution...

* `bgp_own_default` will redistribute BGP default routes. Defaults to `True` for peer types of `rrserver-rrserver`.
* `bgp_transit_default` will redistribute BGP default routes. Defaults to `True` for peer types of `rrserver-rrserver`.


An example of using redistribute can be found below...
```yaml
bgp:
  ...
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

Using this option will set the `constraints` profile to `customer.private` and apply the relevant adjusted limits.


An example is below...
```yaml
bgp:
  ...
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
bgp:
  ...
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
bgp:
  ...
  peers:
    peer1:
      asn: 65000
      description: Some peer
      source_address6: fc00::2
  ...
```
