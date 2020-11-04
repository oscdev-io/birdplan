# BGP Appendix

# Local Preferences

Peer costs are minus'd from the below preference values.

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
| PREFIX_IMPORT_MAXLEN4 | 24 | Maximum IPv4 CIDR length to import |
| PREFIX_IMPORT_MINLEN4 | 8 | Minimum IPv4 CIDR length to import |
| PREFIX_EXPORT_MAXLEN4 | 24 | Maximum IPv4 CIDR length to export |
| PREFIX_EXPORT_MINLEN4 | 8 | Minimum IPv4 CIDR length to export |
| PREFIX_IMPORT_MAXLEN6 | 48 | Maximum IPv6 CIDR length to import |
| PREFIX_IMPORT_MINLEN6 | 16 | Minimum IPv6 CIDR length to import |
| PREFIX_EXPORT_MAXLEN6 | 48 | Maximum IPv6 CIDR length to export |
| PREFIX_EXPORT_MINLEN6 | 16 | Minimum IPv6 CIDR length to export |

# Large Communities

Large communities are in the form of (OWN_ASN, FUNCTION, XXX) and are described below.

Brief overview of FUNCTION assignments...
  * `OWN_ASN:0-999:*` - Operational, some action is taken
  * `OWN_ASN:1000-1999:*` - Informational, give some information about the route

## Functions

| Function Number | Description |
| --- | --- |
| 1 | Route learned [^lc-function-1] in (https://www.iso.org/iso-3166-country-codes.html) - ISO 3166-1 numeric country identifier |
| 2 | Route learned [^lc-function-2] in (https://unstats.un.org/unsd/methodology/m49/) - UN M.49 Region |
| 3 | Relation [^lc-function-3] |
| 4 | ASN-based selective NOEXPORT [^lc-function-4] |
| 5 | Location-based selective NOEXPORT [^lc-function-5] |
| 6 | ASN-Based Selective AS Path Prepending (one) [^lc-function-6] |
| 62 | ASN-Based Selective AS Path Prepending (two) - ENHANCED [^lc-function-6] |
| 63 | ASN-Based Selective AS Path Prepending (three) - ENHANCED [^lc-function-6] |
| 7 | Location-Based Selective AS Path Prepending (one) [^lc-function-7] |
| 72 | Location-Based Selective AS Path Prepending (two) - ENHANCED [^lc-function-7] |
| 73 | Location-Based Selective AS Path Prepending (three) - ENHANCED [^lc-function-7] |
| 8 | Manipulation of the LOCAL_PREF Attribute - ENHANCED [^lc-function-8] |
| 1000 | Route information |
| 1101 | Route filtered |
| 1200 | Actions |

[^lc-function-1]: Route learned in ISO-3166-1 country. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 3.1.1 pg. 6

[^lc-function-2]: Route learned in UN M.49 region. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 3.1.2 pg. 6

[^lc-function-3]: Relation. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 3.2 pg 7.

[^lc-function-4]: ASN-based selective NOEXPORT. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 4.1.1 pg 8.

[^lc-function-5]: Location-based selective NOEXPORT. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 4.1.2 pg 8.

[^lc-function-6]: ASN-Based Selective AS Path Prepending. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 4.2.1 pg 9.

[^lc-function-7]: Location-Based Selective AS Path Prepending. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 4.2.2 pg 10.

[^lc-function-8]: Manipulation of the LOCAL_PREF Attribute. ref [RFC 8195](https://tools.ietf.org/html/rfc8195) section 4.3 pg 10/11.

## Relation Communities

Internally set, not allowable from any BGP peer type.

| Community | Description |
| --- | --- |
| (OWN_ASN, 3, 1) | Originated (OWN) |
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

## Location-based selective NOEXPORT Communities

Location based selective NOEXPORT using an ISO-3166-1 country identifier.

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 5, COUNTRY) | Do not export to peer in ISO-3166-1 country (https://www.iso.org/iso-3166-country-codes.html) |


## Prepending Communities

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 6, PEER_ASN) | Prepend 1x to PEER_ASN |
| (OWN_ASN, 62, PEER_ASN) | Prepend 2x to PEER_ASN |
| (OWN_ASN, 63, PEER_ASN) | Prepend 3x to PEER_ASN |


## Location-Based Selective AS Path Prepending Communities

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 7, COUNTRY) | Prepend 1x to ISO-3166-1 country (https://www.iso.org/iso-3166-country-codes.html) |
| (OWN_ASN, 72, COUNTRY) | Prepend 2x to ISO-3166-1 country (https://www.iso.org/iso-3166-country-codes.html) |
| (OWN_ASN, 73, COUNTRY) | Prepend 3x to ISO-3166-1 country (https://www.iso.org/iso-3166-country-codes.html) |


## LOCAL_PREF Attribute Manipulation Communities

Allowable internally and by `customer`.

| Community | Description |
| --- | --- |
| (OWN_ASN, 8, 1) | Decrease local_pref by 1 |
| (OWN_ASN, 8, 2) | Decrease local_pref by 2 |
| (OWN_ASN, 8, 3) | Decrease local_pref by 3 |


## Route Information Communities

Internally set, not allowable from any BGP peer type.

| Community | Description |
| --- | --- |
| (OWN_ASN, 1000, 1) | Communities were stripped |
| (OWN_ASN, 1000, 3) | Large communities were stripped |
| (OWN_ASN, 1000, 4) | Private large communities were stripped |

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
| (OWN_ASN, 1101, 10) | Origin AS filtered (not in filter list) |
| (OWN_ASN, 1101, 12) | Default route not allowed |
| (OWN_ASN, 1101, 13) | RPKI unknown |
| (OWN_ASN, 1101, 14) | RPKI invalid |
| (OWN_ASN, 1101, 15) | Transit free ASN |
| (OWN_ASN, 1101, 16) | Too many communities |
| (OWN_ASN, 1101, 17) | Route collector |
| (OWN_ASN, 1101, 18) | Quarantined |
| (OWN_ASN, 1101, 19) | Too many extended communities |
| (OWN_ASN, 1101, 20) | Too many large communities |
| (OWN_ASN, 1101, 21) | Peer AS filtered (not in filter list) |
| (OWN_ASN, 1101, 22) | AS path not allowed |
| (OWN_ASN, 1101, 23) | No relation large community set |

## Action Communities

Internally set, not allowable from any BGP peer type.

| Community | Description |
| --- | --- |
| (OWN_ASN, 1200, 1) | Replace AS-PATH with our own ASN |
