# BGP filtering tests

Router r1 should be receiving routes from e1 test cases.


## Tests for BGP AS-PATH length filtering

In terms of test `test_bgp_filtering_as_path_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying AS-PATH lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_as_path_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying AS-PATH lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_as_path_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying AS-PATH lengths to test the peer min and max constraint values when overridden.


## Tests for BGP prefix length filtering

In terms of test `test_bgp_filtering_prefix_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_prefix_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_prefix_length_import_constraints`:
- ExaBGP e1 should export prefixes with varying lengths to test the peer min and max constraint values when overridden.


## Tests for BGP blackholing

In terms of test `test_bgp_filtering_blackhole_length_import_constraints`:
- ExaBGP e1 should export blackholes with varying lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_blackhole_length_import_constraints`:
- ExaBGP e1 should export blackholes with varying lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_blackhole_length_import_constraints`:
- ExaBGP e1 should export blackholes with varying lengths to test the peer min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_blackhole_not_in_prefix_list`:
- ExaBGP e1 should export blackholes with varying lengths within and outside of a prefix filter to test the peer min and max constraint values when overridden and filtering of blackholes that fall within the filter range.


## Tests for BGP community length filtering

In terms of test `test_bgp_filtering_community_length_import_constraints`:
- ExaBGP e1 should export communities with varying lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_community_length_import_constraints`:
- ExaBGP e1 should export communities with varying lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_community_length_import_constraints`:
- ExaBGP e1 should export communities with varying lengths to test the peer min and max constraint values when overridden.


In terms of test `test_bgp_filtering_extended_community_length_import_constraints`:
- ExaBGP e1 should export extended communities with varying lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_extended_community_length_import_constraints`:
- ExaBGP e1 should export extended communities with varying lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_extended_community_length_import_constraints`:
- ExaBGP e1 should export extended communities with varying lengths to test the peer min and max constraint values when overridden.


In terms of test `test_bgp_filtering_large_community_length_import_constraints`:
- ExaBGP e1 should export large communities with varying lengths to test the default min and max constraint values.

In terms of test `test_bgp_filtering_global_large_community_length_import_constraints`:
- ExaBGP e1 should export large communities with varying lengths to test the global min and max constraint values when overridden.

In terms of test `test_bgp_filtering_peer_large_community_length_import_constraints`:
- ExaBGP e1 should export large communities with varying lengths to test the peer min and max constraint values when overridden.


## Tests for BGP bogon filtering

In terms of test `test_bgp_filtering_bogon_asn`:
- ExaBGP e1 should export a prefix with a bogon ASN in the AS-PATH.

In terms of test `test_bgp_filtering_bogon`:
- ExaBGP e1 should export a bogon prefix.


## Tests for BGP transit free ASN filtering

In terms of test `test_bgp_filtering_transit_free_asn`:
- ExaBGP e1 should export a route where the route a transit free ASN in the AS-PATH.


## Tests for BGP default route filtering

In terms of test `test_bgp_filtering_default`:
- ExaBGP e1 and e2 should export default route(s) and depending on the peer type we filter them.

In terms of test `test_bgp_filtering_accept_bgp_own_default`:
- ExaBGP e1 and e2 should export default route(s) and depending on the peer type we filter them or accept only
our own default route.

In terms of test `test_bgp_filtering_accept_bgp_transit_default`:
- ExaBGP e1 and e2 should export default route(s) and depending on the peer type we filter them or accept only
our the transit default route.


## Tests for BGP first AS not peer AS filtering

In terms of test `test_bgp_filtering_first_as_not_peer_as`:
- ExaBGP e1 should export a route where the first AS is not the peer AS.


## Tests for BGP next hop not peer IP filtering

In terms of test `test_bgp_filtering_next_hop_not_peer_ip`:
- ExaBGP e1 should export a route where the next hop IP is not the peer IP.


## Tests for BGP AS-PATH ASN filtered

In terms of test `test_bgp_filtering_aspath_asn_filtered_with_match`:
- ExaBGP e1 should export a route where a specific set of ASN is listed in the filter.

In terms of test `test_bgp_filtering_aspath_asn_filtered_without_match`:
- ExaBGP e1 should export a route where a specific set of ASN is listed in the filter.


## Tests for BGP AS-PATH ASN deny

In terms of test `test_bgp_filtering_aspath_asn_deny_with_match`:
- ExaBGP e1 should export a route where a specific set of ASN is denied import.

In terms of test `test_bgp_filtering_aspath_asn_deny_without_match`:
- ExaBGP e1 should export a route where a specific set of ASN is denied import.


## Tests for BGP origin AS filtered

In terms of test `test_bgp_filtering_origin_asn_filtered_with_match`:
- ExaBGP e1 should export a route where the origin AS is listed in the filter.

In terms of test `test_bgp_filtering_origin_asn_filtered_without_match`:
- ExaBGP e1 should export a route where the origin AS is not listed in the filter.


## Tests for BGP origin AS deny

In terms of test `test_bgp_filtering_origin_asn_deny_with_match`:
- ExaBGP e1 should export a route where the origin AS is denied import.

In terms of test `test_bgp_filtering_origin_asn_deny_without_match`:
- ExaBGP e1 should export a route where the origin AS is not denied import.


## Tests for BGP peer AS filtered

In terms of test `test_bgp_filtering_peer_asn_filtered_with_match`:
- ExaBGP e1 should export a route where the first AS is listed in the filter.

In terms of test `test_bgp_filtering_peer_asn_filtered_without_match`:
- ExaBGP e1 should export a route where the first AS is not listed in the filter.


## Tests for BGP prefix filtered

In terms of test `test_bgp_filtering_prefix_filtered_with_match`:
- ExaBGP e1 should export a route where the prefix is listed in the filter.

In terms of test `test_bgp_filtering_prefix_filtered_without_match`:
- ExaBGP e1 should export a route where the prefix is not listed in the filter.


## Tests for BGP prefix deny

In terms of test `test_bgp_filtering_prefix_deny_with_match`:
- ExaBGP e1 should export a route where the prefix is denied import.

In terms of test `test_bgp_filtering_prefix_deny_without_match`:
- ExaBGP e1 should export a route where the prefix is not denied import.


## Tests for BGP quarantine filtering

In terms of test `test_bgp_filtering_quarantine`:
- ExaBGP e1 should export a route where the peer is set to quarantine.


## Tests for BGP replace_aspath community filtering

In terms of test `test_replace_aspath_nonprivate_asn`:
- ExaBGP e1 should export a route where the replace_aspath community is present and a non-private ASN and should be filtered.

In terms of test `test_replace_aspath_notallowed_aspath`:
- ExaBGP e1 should export a route where the replace_aspath community is present and a disallowed ASN and should be filtered.


## Tests for BGP relation large community filtering

In terms of test `test_bgp_filtering_quarantine`:
- ExaBGP e1 should export a route where the a relation large community is not present and should be filtered.


## Tests for BGP AS-SET filtering

In terms of test `test_bgp_filtering_as_sets`:
- ExaBGP e1 should be exporting various prefixes, depending on the test we'll be filtering some out.


## Diagram

```plantuml
@startuml
hide circle
title Test BGP filtering from e1 to r1


class "Router: r1" {
  .. Interface: eth0 ..
- 100.64.0.1/24
+ fc00:100::1/64
}


class "ExaBGP: e1" {
  .. Interface: eth0 ..
- 100.64.0.2/24
+ fc00:100::2/64
}


class "Switch: s1" {}

"ExaBGP: e1" -> "Switch: s1": e1 eth0
"Switch: s1" -> "Router: r1": r1 eth0

@enduml
```
