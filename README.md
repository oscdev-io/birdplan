# BIRD Configuraiton

This document is broken up into sections for the configuration of each routing protocol.

## Main Configuration

The following YAML configuration keys are supported..

### router_id

This is the BIRD router ID, the main IP of the system is normally used.

```yaml
router_id: 0.0.0.2
```

### log_file

Set the log filename to use instead of systemd journal.

```yaml
log_file: /var/log/bird.log
```

### debug

Set BIRD into debug mode.

```yaml
debug: True
```

### export_kernel

The `export_kernel` key contains a dictionary of the routes to be exported to the kernel RIB. All items default to `True`.

`static` routes are those setup in the static protocol.

`static_device` routes are those setup in the static protocol which point to a device and not a gateway.

`rip` routes from the RIP protocol.

`ospf` routes from the OSPF protocol.

`bgp` routes from the BGP protocol.

An example of this configuration can be found below...
```yaml
router_id: 0.0.0.2
export_kernel:
  bgp: False
```

## Static Route Configuration

The following keys are supported under the `static` key.

### static

The `static` key contains a list of routes to be added in the static routing table.

These static routes will be exported to the kernel.

A configuration example for static routes is below...
```yaml
bird:
  router_id: 0.0.0.2
  static:
    - '10.0.1.0/24 via 192.168.0.4'
    - '10.0.2.0/24 via 192.168.0.5'
```

## RIP Configuration

The following keys are supported under the `rip` key.

### interfaces

The `interfaces` key contains a dictionary of the interfaces to use for RIP.

The following sub-properties are supported:

`metric` - The metric value to add to the routes exported on this interface. The highest RIP route metric is 16, so be wary of
this.

`update-time` - How often we should be sending updates.


A configuration example for interfaces is below...
```yaml
router_id: 0.0.0.2
rip:
  interfaces:
    'eth0': []
    'eth1':
      metric: 2
```

### accept

The `accept` key contains a dictionary of route types we will accept:

`default` - Allows us to accept a default route from RIP. The default is `False`.

```yaml
router_id: 0.0.0.5
rip:
  accept:
    default: True
```

### redistribute

The `redistribute` key contains a dictionary of the redistributable routes to be exported to RIP.

`connected` routes are kernel device routes for the interfaces listed. A list of interfaces must be provided. This can be a pattern
like `eth*`.

`kernel` routes are those statically added to the kernel.

`static` routes are those setup in the static protocol.

`static_device` routes are those setup in the static protocol which point to a device and not a gateway. FIXME: NK: UNKNOWN WHERE THESE COME FROM

`default` allows the redistribution of the default route, it must still come from somewhere, so this option alone is useless.

`rip` allows the disabling of redistributing of the RIP routes we receive. By default we redistribute RIP routes.


An example of this configuration can be found below...
```yaml
bird:
  router_id: 0.0.0.2
  rip:
    redistribute:
      connected:
        interfaces:
          - eth9
      kernel: True
      static: True
      static_device: True
```

## OSPF Configuration

The following pillar keys are supported under the `ospf` key under the top level `bird` key.

OSPF v3 is used for both IPv4 and IPv6.

### accept

The `accept` key contains a dictionary of routes we will accept.

`default` allows us to accept a default route from OSPF.


### redistribute

The `redistribute` key contains a dictionary of the redistributable routes to be exported to OSPF.

`connected` routes are kernel device routes for the interfaces. OSPF stub routes are used to add interfaces not part of the OSPF
communication network. OSPF by default exports all connected routes as OSPF internal routes. So this option makes no sense.

`kernel` routes are those statically added to the kernel.

`static` routes are those setup in the static protocol.

`static_device` routes are those setup in the static protocol which point to a device and not a gateway.

`default` allows the redistribution of the default route, it must still come from somewhere, so this option alone is useless.


An example of this configuration can be found below...
```yaml
bird:
  router_id: 0.0.0.2
  ospf:
    redistribute:
      kernel: True
      static: True
      static_device: True
    areas:
      0:
        interfaces:
          'eth0': []
```

### areas

An OSPF area is defined using the `areas` key, which contains a dictionary of the area ID's.

Under the area ID is `interfaces`, which is a dictionary of interface matches, containing a list of supported options.

Supported interface options are listed below.

* `stub` - When set to `True` will not communicate OSPF over this interface, but will add it to the automatically generated interface
routes injected into the OSPF routing table.

```yaml
  ospf:
    areas:
      0:
        interfaces:
          'eth0': []
          'eth1':
            - stub: True
```
