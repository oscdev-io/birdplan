# RIP Protocol Configuration

The following options are supported under `rip`.

# interfaces

The `interfaces` key contains a dictionary of the interfaces to use for RIP.

The following sub-properties are supported:

* `metric` - The metric value to add to the routes exported on this interface. The highest RIP route metric is 16, so be wary of
this.

* `update-time` - How often we should be sending updates.


A configuration example for interfaces is below...
```yaml
router_id: 0.0.0.2
rip:
  interfaces:
    'eth0': []
    'eth1':
      metric: 2
```

# accept

The `accept` key contains a dictionary of route types we will accept.  Namely...

* `default` - Allows us to accept a default route from RIP. The default is `False`.

```yaml
router_id: 0.0.0.5
rip:
  accept:
    default: True
```

# redistribute

The `redistribute` key contains a dictionary of the redistributable routes to be exported to RIP.

* `connected` routes are kernel device routes for the interfaces listed. A list of interfaces must be provided. This can be a pattern
like `eth*`.

* `kernel` routes are those added to the kernel. This excludes kernel default routes.

* `kernel_default` routes are default routes added to the kernel.

* `static` routes are those setup in the static protocol. This excludes static default routes.

* `static_default` routes are default routes setup in the static protocol.

* `rip` allows the disabling of redistributing of the RIP routes we receive. By default we redistribute RIP routes.

* `rip_default` allows the redistributing of RIP default routes we receive. By default we do not redistribute RIP default routes.

An example of this configuration can be found below...
```yaml
router_id: 0.0.0.2
rip:
  redistribute:
    connected:
      interfaces:
        - eth9
        - ppp*
    kernel: True
    static: True
```