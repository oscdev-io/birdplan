# OSPF Configuration

The following options are supported under `ospf`.

OSPF v3 is used for both IPv4 and IPv6.

## accept

The `accept` key contains a dictionary of routes we will accept.

* `default` allows us to accept a default route from OSPF.

Below is a configuration example...
```yaml
router_id: 0.0.0.2
ospf:
  accept:
    default: True
  areas:
    0:
      interfaces:
        'eth0': []
```

### redistribute

Tests: connected, kernel, static, default

The `redistribute` key contains a dictionary of the redistributable routes to be exported to OSPF.

* `connected` routes are kernel device routes for the interfaces listed. A list of interfaces must be provided. This can be a pattern
like `eth*`.

* `kernel` routes are those statically added to the kernel.

* `static` routes are those setup in the static protocol.

* `default` allows the redistribution of the default route, it must still come from somewhere, so this option alone is useless.


An example of this configuration can be found below...
```yaml
router_id: 0.0.0.2
ospf:
  redistribute:
    kernel: True
    static: True
    connected:
      interfaces:
        - eth9
  areas:
    0:
      interfaces:
        'eth0': []
```

### areas

Tests: hello, stub, wait

An OSPF area is defined using the `areas` key, which contains a dictionary of the area ID's.

Under the area ID is `interfaces`, which is a dictionary of interface matches, containing a list of supported options.

Supported interface options are listed below...

* `hello` - Interval in seconds between sending of Hello messages, all routers on the same network must have the same value.

* `stub` - When set to `True` will not communicate OSPF over this interface, but will add it to the automatically generated interface
routes injected into the OSPF routing table.

* `wait` - waits for the specified number of seconds between starting election and building adjacency. Default value is 4*hello.


```yaml
ospf:
  areas:
    0:
      interfaces:
        'eth0': []
        'eth1':
          stub: True
```