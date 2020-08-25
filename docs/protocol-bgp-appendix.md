# BGP Appendix

# Local Preferences

| Constant | Preference | Description |
| --- | --- | --- |
| BGP_PREF_OWN | 950 | Originated routes (originated = -20, static = -10, direct = -10, kernel = -5) |
| BGP_PREF_CUSTOMER | 750 | Customer peer routes |
| BGP_PREF_PEER | 470 | Peer routes |
| BGP_PREF_ROUTESERVER | 450 | Route server routes |
| BGP_PREF_TRANSIT | 150 | Transit routes |


# Prefix Sizes

These are globals which can be overridden in configuration.

| Constant | Size | Description |
| --- | --- | --- |
| BGP_PREFIX_MAXLEN4_IMPORT | 24 | Maximum IPv4 CIDR length to import |
| BGP_PREFIX_MAXLEN4_EXPORT | 24 | Maximum IPv4 CIDR length to export |
| BGP_PREFIX_MINLEN4_IMPORT | 8 | Minimum IPv4 CIDR length to import |
| BGP_PREFIX_MINLEN4_EXPORT | 8 | Minimum IPv4 CIDR length to export |
| BGP_PREFIX_MAXLEN6_IMPORT | 48 | Maximum IPv6 CIDR length to import |
| BGP_PREFIX_MAXLEN6_EXPORT | 48 | Maximum IPv6 CIDR length to export |
| BGP_PREFIX_MINLEN6_IMPORT | 16 | Minimum IPv6 CIDR length to import |
| BGP_PREFIX_MINLEN6_EXPORT | 16 | Minimum IPv6 CIDR length to export |

# Large Communities

Large communities are in the form of (OWN_ASN, FUNCTION, XXX) and are described below.

## Functions
| Function Number | Description |
| --- | --- |
| 3 | Relation |
| 4 | No Export |
| 61 | Prepend one |
| 62 | Prepend two |
| 63 | Prepend three |
| 1101 | Filtered |

## Relation Communities

Internally set, not allowable from any BGP peer type.

| Community | Description |
| --- | --- |
| (OWN_ASN, 3, 1) | Originated |
| (OWN_ASN, 3, 2) | Customer |
| (OWN_ASN, 3, 3) | Peer |
| (OWN_ASN, 3, 4) | Transit |
| (OWN_ASN, 3, 5) | Route server |

## NoExport Communities

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 4, PEER_ASN) | Do not export to PEER_ASN |
| (OWN_ASN, 4, 65412) | Do not export to transit peers |
| (OWN_ASN, 4, 65413) | Do not export to peers |
| (OWN_ASN, 4, 65414) | Do not export to customers |

## Prepending Communities

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 61, PEER_ASN) | Prepend 1x to PEER_ASN |
| (OWN_ASN, 62, PEER_ASN) | Prepend 2x to PEER_ASN |
| (OWN_ASN, 63, PEER_ASN) | Prepend 3x to PEER_ASN |

## Filtered Communities

Internally set, not allowable from any BGP peer type.

| Community | Description |
| --- | --- |
| (OWN_ASN, 1101, 1) | Prefix length too long |
| (OWN_ASN, 1101, 2) | Prefix length too short |
| (OWN_ASN, 1101, 3) | Bogon |
| (OWN_ASN, 1101, 4) | Bogon ASN |
| (OWN_ASN, 1101, 5) | AS path too long |
| (OWN_ASN, 1101, 6) | AS path too short |
| (OWN_ASN, 1101, 7) | First AS not peer AS |
| (OWN_ASN, 1101, 8) | Next hop not peer IP |
| (OWN_ASN, 1101, 9) | Prefix filtered |
| (OWN_ASN, 1101, 10) | Origin AS filtered |
| (OWN_ASN, 1101, 12) | Default route not allowed |
| (OWN_ASN, 1101, 13) | RPKI unknown |
| (OWN_ASN, 1101, 14) | RPKI invalid |
| (OWN_ASN, 1101, 15) | Transit free ASN |
| (OWN_ASN, 1101, 16) | Too many communities |
| (OWN_ASN, 1101, 17) | Route collector |
| (OWN_ASN, 1101, 18) | Quarantined |

