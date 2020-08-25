# Configuration

Below are configuration options that do not apply to any specific protocol.

## router_id

This is the BIRD router ID, the main IP of the system is normally used.

```yaml
router_id: 0.0.0.2
```

## log_file

Set the log filename to use instead of systemd journal.

```yaml
log_file: /var/log/bird.log
```

## debug

Set BIRD into debug mode.

```yaml
debug: True
```

## export_kernel

The `export_kernel` key contains a dictionary of the routes to be exported to the kernel RIB. All items default to `True`.

* `static` routes are those setup in the static protocol.

* `rip` routes from the RIP protocol.

* `ospf` routes from the OSPF protocol.

* `bgp` routes from the BGP protocol.

An example of this configuration can be found below...
```yaml
router_id: 0.0.0.2
export_kernel:
  bgp: False
```