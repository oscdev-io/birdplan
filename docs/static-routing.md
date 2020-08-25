# Static Route Configuration

The following keys are supported under `static`.

## static

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