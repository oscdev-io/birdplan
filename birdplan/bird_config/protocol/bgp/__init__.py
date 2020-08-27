#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""BIRD BGP protocol configuration."""

from ...base import BirdConfigBase
from ..pipe import BirdConfigProtocolPipe
from ..direct import BirdConfigProtocolDirect
from .peer import BirdConfigProtocolBGPPeer
from ....exceptions import BirdPlanError


class BirdConfigProtocolBGP(BirdConfigBase):
    """BIRD BGP protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # BGP
        self._bgp_asn = None
        self._bgp_peers = {}
        # Route reflector cluster ID
        self._bgp_rr_cluster_id = None
        # Routes originated from BGP
        self._bgp_originate_routes = {}
        # Some tunables...
        self._bgp_accept = {
            "default": False,
        }
        # BGP route redistribution
        self._bgp_import = {
            "connected": {},
            "static": False,
            "kernel": False,
        }

    def _configure_originate(self):
        # Work out static v4 and v6 routes
        routes_ipv4 = []
        routes_ipv6 = []
        for prefix in sorted(self._bgp_originate_routes.keys()):
            info = self._bgp_originate_routes[prefix]
            if "." in prefix:
                routes_ipv4.append("%s %s" % (prefix, info))
            elif ":" in prefix:
                routes_ipv6.append("%s %s" % (prefix, info))
            else:
                raise BirdPlanError(f"The BGP originate route '{prefix}' is odd")

        self._addline("# BGP Origination")
        self._addline("ipv4 table t_bgp_originate4;")
        self._addline("ipv6 table t_bgp_originate6;")
        self._addline("")

        #
        # Setup BGP Origination
        #

        self._addline("filter f_bgp_originate4_import {")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(20);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")
        self._addline("filter f_bgp_originate6_import {")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(20);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

        self._addline("protocol static bgp_originate4 {")
        self._addline('\tdescription "BGP route origination for IPv4";')
        self._addline("")
        self._addline("\tipv4 {")
        self._addline("\t\ttable t_bgp_originate4;")
        self._addline("\t\texport none;")
        self._addline("\t\timport filter f_bgp_originate4_import;")
        self._addline("\t};")
        # If we have IPv4 routes
        if routes_ipv4:
            self._addline("")
            # Output the routes
            for route in routes_ipv4:
                self._addline(f"\troute {route};")
        self._addline("};")
        self._addline("")
        self._addline("protocol static bgp_originate6 {")
        self._addline('\tdescription "BGP route origination for IPv6";')
        self._addline("")
        self._addline("\tipv6 {")
        self._addline("\t\ttable t_bgp_originate6;")
        self._addline("\t\texport none;")
        self._addline("\t\timport filter f_bgp_originate6_import;")
        self._addline("\t};")
        # If we have IPv6 routes
        if routes_ipv6:
            self._addline("")
            # Output the routes
            for route in routes_ipv6:
                self._addline(f"\troute {route};")
        self._addline("};")
        self._addline("")

        # Configure BGP origination route pipe to the bgp table
        originate_pipe = BirdConfigProtocolPipe(
            self, table_from="bgp_originate", table_to="bgp", table_export="all", table_import="none"
        )
        originate_pipe.configure()

    def _bgp_to_master_export_filter(self, ipv):
        """BGP to master filter."""

        # Configure export filter to master
        self._addline("# Export filter FROM BGP table TO master table")
        self._addline(f"filter f_bgp_master{ipv}_export {{")
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self._addline("\t# Do not export default routes to the master")
            self._addline(f"\tif (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self._addline("\t\treject;")
            self._addline("\t}")
        # Else accept
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _bgp_to_master_import_filter(self, ipv):
        # Configure import filter to master
        self._addline("# Import filter FROM master table TO BGP table")
        self._addline(f"filter f_bgp_master{ipv}_import")
        self._addline("{")
        # Redistribute kernel routes
        if self.import_kernel:
            self._addline("\t# Import kernel routes into BGP")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\tbgp_import_own(5);")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.import_static:
            self._addline("\t# Import static routes into BGP")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\tbgp_import_own(10);")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else accept
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _bgp_to_direct_import_filter(self, ipv):
        # Configure import filter to direct
        self._addline(f"filter f_bgp_direct{ipv}_import {{")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(10);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _setup_bgp_to_master_export_filters(self):
        """BGP main table to master export filters setup."""
        self._bgp_to_master_export_filter(4)
        self._bgp_to_master_export_filter(6)

    def _setup_bgp_to_master_import_filters(self):
        """BGP main table to master import filters setup."""
        self._bgp_to_master_import_filter(4)
        self._bgp_to_master_import_filter(6)

    def _setup_bgp_to_direct_import_filters(self):
        """BGP main table to direct import filters setup."""
        self._bgp_to_direct_import_filter(4)
        self._bgp_to_direct_import_filter(6)

    def configure(self):
        """Configure the BGP protocol."""

        self._addline("# BGP Tables")
        self._addline("ipv4 table t_bgp4;")
        self._addline("ipv6 table t_bgp6;")
        self._addline("")

        # Setup BGP origination
        self._configure_originate()

        # BGP to master export filters
        self._setup_bgp_to_master_export_filters()

        # BGP to master import filters
        self._setup_bgp_to_master_import_filters()

        # Configure pipe from BGP to the master routing table
        bgp_master_pipe = BirdConfigProtocolPipe(
            self, table_from="bgp", table_to="master", table_export_filtered=True, table_import_filtered=True
        )
        bgp_master_pipe.configure()

        # Check if we're importing connected routes, if we are, create the protocol and pipe
        if self.import_connected:
            if "interfaces" not in self.import_connected:
                raise BirdPlanError("BGP import connected requires a list in item 'interfaces' to match interface names")
            # Add direct protocol for redistribution of connected routes
            bgp_direct_protocol = BirdConfigProtocolDirect(self, name="bgp", interfaces=self.import_connected["interfaces"])
            bgp_direct_protocol.configure()
            # Add pipe
            self._setup_bgp_to_direct_import_filters()
            bgp_direct_pipe = BirdConfigProtocolPipe(
                self,
                name="bgp",
                description="BGP",
                table_from="bgp",
                table_to="direct",
                table_export="none",
                table_import_filtered=True,
            )
            bgp_direct_pipe.configure()

        # Loop with BGP peers and configure them
        for peer_name in sorted(self._bgp_peers.keys()):
            peer = BirdConfigProtocolBGPPeer(self, peer_name=peer_name, peer_config=self._bgp_peers[peer_name])
            peer.configure()

    def set_asn(self, asn):
        """Set our ASN."""
        self._bgp_asn = asn

        # Turn on bogons and functions output in our constants block
        self.parent.constants.need_bogons = True
        self.parent.constants.bgp_asn = self._bgp_asn
        self.parent.constants.need_functions = True

    def add_originate_route(self, route):
        """Add static route."""
        (prefix, route_info) = route.split(" ", 1)
        self._bgp_originate_routes[prefix] = route_info

    def add_peer(self, peer_name, peer_config=None):
        """Add peer to BGP."""
        if peer_name not in self._bgp_peers:
            self._bgp_peers[peer_name] = peer_config

    # PREFIX_MAXLEN4

    @property
    def prefix_maxlen4_import(self):
        """Return the current value of prefix_maxlen4_import."""
        return self.parent.constants.bgp_prefix_maxlen4_import

    @prefix_maxlen4_import.setter
    def prefix_maxlen4_import(self, value):
        """Setter for prefix_maxlen4_import."""
        self.parent.constants.bgp_prefix_maxlen4_import = value

    @property
    def prefix_maxlen4_export(self):
        """Return the current value of prefix_maxlen4_export."""
        return self.parent.constants.bgp_prefix_maxlen4_export

    @prefix_maxlen4_export.setter
    def prefix_maxlen4_export(self, value):
        """Setter for prefix_maxlen4_export."""
        self.parent.constants.bgp_prefix_maxlen4_export = value

    # PREFIX_MINLEN4

    @property
    def prefix_minlen4_import(self):
        """Return the current value of prefix_minlen4_import."""
        return self.parent.constants.bgp_prefix_minlen4_import

    @prefix_minlen4_import.setter
    def prefix_minlen4_import(self, value):
        """Setter for prefix_minlen4_import."""
        self.parent.constants.bgp_prefix_minlen4_import = value

    @property
    def prefix_minlen4_export(self):
        """Return the current value of prefix_minlen4_export."""
        return self.parent.constants.bgp_prefix_minlen4_export

    @prefix_minlen4_export.setter
    def prefix_minlen4_export(self, value):
        """Setter for prefix_minlen4_export."""
        self.parent.constants.bgp_prefix_minlen4_export = value

    # PREFIX_MAXLEN6

    @property
    def prefix_maxlen6_import(self):
        """Return the current value of prefix_maxlen6_import."""
        return self.parent.constants.bgp_prefix_maxlen6_import

    @prefix_maxlen6_import.setter
    def prefix_maxlen6_import(self, value):
        """Setter for prefix_maxlen6_import."""
        self.parent.constants.bgp_prefix_maxlen6_import = value

    @property
    def prefix_maxlen6_export(self):
        """Return the current value of prefix_maxlen6_export."""
        return self.parent.constants.bgp_prefix_maxlen6_export

    @prefix_maxlen6_export.setter
    def prefix_maxlen6_export(self, value):
        """Setter for prefix_maxlen6_export."""
        self.parent.constants.bgp_prefix_maxlen6_export = value

    # PREFIX_MINLEN6

    @property
    def prefix_minlen6_import(self):
        """Return the current value of prefix_minlen6_import."""
        return self.parent.constants.bgp_prefix_minlen6_import

    @prefix_minlen6_import.setter
    def prefix_minlen6_import(self, value):
        """Setter for prefix_minlen6_import."""
        self.parent.constants.bgp_prefix_minlen6_import = value

    @property
    def prefix_minlen6_export(self):
        """Return the current value of prefix_minlen6_export."""
        return self.parent.constants.bgp_prefix_minlen6_export

    @prefix_minlen6_export.setter
    def prefix_minlen6_export(self, value):
        """Setter for prefix_minlen6_export."""
        self.parent.constants.bgp_prefix_minlen6_export = value

    # OTHER SETTINGS

    @property
    def accept_default(self):
        """Accept the default route if we get it via BGP."""
        return self._bgp_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Setter for accept_default."""
        self._bgp_accept["default"] = value

    @property
    def import_connected(self):
        """Import connected routes into the main BGP table."""
        return self._bgp_import["connected"]

    @import_connected.setter
    def import_connected(self, value):
        """Setter for import_connected."""
        self._bgp_import["connected"] = value

    @property
    def import_static(self):
        """Import static routes into the main BGP table."""
        return self._bgp_import["static"]

    @import_static.setter
    def import_static(self, value):
        """Setter for import_static."""
        self._bgp_import["static"] = value

    @property
    def import_kernel(self):
        """Import kernel routes into the main BGP table."""
        return self._bgp_import["kernel"]

    @import_kernel.setter
    def import_kernel(self, value):
        """Setter for import_kernel."""
        self._bgp_import["kernel"] = value

    @property
    def peers(self):
        """Return BGP peers."""
        return self._bgp_peers

    @property
    def rr_cluster_id(self):
        """Return route reflector cluster ID."""
        return self._bgp_rr_cluster_id

    @rr_cluster_id.setter
    def rr_cluster_id(self, value):
        """Set our route reflector cluster ID."""
        self._bgp_rr_cluster_id = value
