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

* `default` - Allows us to accept a default route from the BGP peer. The default is `False`.

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


## filters

Filtering of routes received from a peer. Options available are below...

* `prefixes` will filter on a list of allowed prefixes
* `asns` will filter on a list of allowed ASN's
* `as-sets` will filter on a list of as-sets, resolving them at the same time.

An example is however below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      filters:
        as-set: AS-EXAMPLE
        asns:
          - 65009
        prefixes:
          - "100.141.0.0/24"
          - "fc00:141::/64"
...
```


## incoming-large-communities

Large communites to add to incoming prefixes.

You can specify the large communities as a list as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      incoming-large-communities:
        - 65001:5000:1
        - 65001:5000:2
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


## outgoing-large-communities

Large communites to add to our outbound prefixes.

You can specify the large communities as a list as per below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      outgoing-large-communities:
        - 65000:5000:1
        - 65000:5000:2
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

IPv4 prefix limit for the peer.

An example of specifying a prefix limit is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prefix_limit4: "test123"
...
```


## prefix_limit6

IPv6 prefix limit for the peer.

An example of specifying a prefix limit is below...
```yaml
...

bgp:
  peers:
    peer1:
      asn: 65000
      description: Some peer
      prefix_limit6: "test123"
...
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

* `default` will redistribute the default route, the type of route also needs to be redistributed. eg. `static`. Defaults to `False`.
* `connected` will redistribute connected routes. Defaults to `False`.
* `static` will redistribute static routes in our global static configuration. Defaults to `False`.
* `kernel` will redistribute kernel routes. Defaults to `False`.
* `originated` will redistribute originated routes. Defaults to `False`.

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
* `peer` this is a peering partner peering session.
* `transit` this is a transit provider peering session.
* `rrclient` this is a route reflector client peering session.
* `rrserver` this is a route reflector server peering session.
* `rrserver-rrserver` this is a peering session between two route reflectors or route reflector mirrors.
* `routecollector` this is a route collector session.
* `routeserver` this is a route server session.
