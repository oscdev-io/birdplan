#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2021, AllWorldIT.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Plugin handler."""

import inspect
import logging
import os
import pkgutil
from typing import Any, Dict, List, Optional


class PluginMethodException(RuntimeError):
    """Plugin method exception raised when a method is called that does not exist."""


class PluginNotFoundException(RuntimeError):
    """Plugin not found exception raised when a plugin is referenced by name and not found."""


class Plugin:  # pylint: disable=too-few-public-methods
    """Base plugin class, used as the parent for all plugins we define."""

    plugin_description: str
    plugin_order: int

    def __init__(self) -> None:
        """Plugin __init__ method."""

        # Set defaults
        self.plugin_description = type(self).__name__
        self.plugin_order = 10


class PluginCollection:
    """
    Initialize PluginCollection using a plugin base package.

    Apon loading each plugin will be instantiated as an object.

    Parameters
    ----------
    plugin_package : str
        Source plan file to generate configuration from.

    """

    # The package name we will be loading plugins from
    _plugin_packages: List[str]
    # List of plugins we've loaded
    _plugins: Dict[str, Plugin]
    # List of paths we've seen during processing
    _seen_paths: List[str]
    # Plugin statuses
    _plugin_status: Dict[str, str]

    def __init__(self, plugin_packages: List[str]):
        """
        Initialize Plugincollection using a plugin base package.

        Classes with a name ending in 'Base' will not be loaded.

        Parameters
        ----------
        plugin_packages : List[str]
            Package names to load plugins from.

        """

        # Setup object
        self._plugin_packages = plugin_packages
        self._plugins = {}
        self._seen_paths = []
        self._plugin_status = {}

        # Load plugins
        self._load_plugins()

    def call_if_exists(self, method_name: str, args: Any = None) -> Dict[str, Any]:
        """
        Call a plugin method, but do not raise an exception if it does not exist.

        Parameters
        ----------
        method_name : str
            Method name to call.

        args : Any
            Method argument(s).

        Returns
        -------
        Dict containing the module name and its result.

        """

        logging.debug("Calling method '%s' if exists", method_name)

        return self.call(method_name, args, skip_not_found=True)

    def call(self, method_name: str, args: Any = None, skip_not_found: bool = False) -> Dict[str, Any]:
        """
        Call a plugin method.

        Parameters
        ----------
        method_name : str
            Method name to call.

        kwargs : Any
            Method arguments.

        args : Any
            Method argument(s).

        skip_not_found :
            If the method is not found return None.

        Returns
        -------
        Dict containing the module name and its result.

        """

        # Loop with plugins, if they have overridden the method, then call it
        results = {}
        # Loop through plugins sorted
        for plugin_name, plugin in sorted(self.plugins.items(), key=lambda kv: kv[1].plugin_order):
            # Check if we're going to raise an exception or just skip
            if not hasattr(plugin, method_name):
                if skip_not_found:
                    logging.debug("Method '%s' does not exist in plugin '%s'", method_name, plugin_name)
                    continue
                raise PluginMethodException(f'Plugin "{plugin_name}" has no method "{method_name}"')
            # Save the result
            results[plugin_name] = self.call_plugin(plugin_name, method_name, args)

        return results

    def get_first(self, method_name: str) -> Optional[str]:
        """
        Get the first plugin method found that matches a specific method name.

        Parameters
        ----------
        method_name : str
            Method name to call.

        Returns
        -------
        Any containing the result.

        """

        # Loop through plugins sorted
        for plugin_name, plugin in sorted(self.plugins.items(), key=lambda kv: kv[1].plugin_order):
            # Check if we're skipping this one if the method is not found
            if not hasattr(plugin, method_name):
                continue
            # Return the first result we get
            return plugin_name

        return None

    def call_first(self, method_name: str, args: Any = None) -> Any:
        """
        Call the first plugin method found.

        Parameters
        ----------
        method_name : str
            Method name to call.

        kwargs : Any
            Method arguments.

        args : Any
            Method argument(s).

        Returns
        -------
        Any containing the result.

        """

        # Get first plugin which has our method
        plugin_name = self.get_first(method_name)

        # Make sure we got a plugin back
        if not plugin_name:
            raise PluginNotFoundException(f"No plugin found for method name '{method_name}'")

        # Return the result of the method call on the first plugin
        return self.call_plugin(plugin_name, method_name, args)

    def call_plugin(self, plugin_name: str, method_name: str, args: Any = None) -> Any:
        """
        Call a specific plugin and its method.

        Parameters
        ----------
        plugin_name : str
            Plugin to call the method in.

        method_name : str
            Method name to call.

        args : Any
            Method argument(s).

        Returns
        -------
        Any containing the plugin call result.

        """

        # Check if plugin exists
        if plugin_name not in self.plugins:
            raise PluginNotFoundException(f'Plugin "{plugin_name}"" not found')
        # If it does then grab it
        plugin = self.plugins[plugin_name]

        # Check if we're going to raise an exception or just skip
        if not hasattr(plugin, method_name):
            raise PluginMethodException(f'Plugin "{plugin_name}" has no method "{method_name}"')

        # Grab the method
        method = getattr(plugin, method_name)

        # Call it
        logging.debug("Calling method '%s' from plugin '%s'", method_name, plugin_name)
        return method(args)

    def get(self, plugin_name: str) -> Plugin:
        """
        Get a specific plugin object.

        Parameters
        ----------
        plugin_name : str
            Plugin to call the method in.

        Returns
        -------
        Plugin object.

        """

        if plugin_name not in self.plugins:
            raise PluginNotFoundException(f'Plugin "{plugin_name}" not found')

        return self.plugins[plugin_name]

    #
    # Internals
    #

    def _load_plugins(self) -> None:
        """Load plugins from the plugin_package we were provided."""

        # Load plugin packages
        for plugin_package in self._plugin_packages:
            self._find_plugins(plugin_package)

    def _find_plugins(self, package_name: str) -> None:  # pylint: disable=too-many-branches
        """
        Recursively search the plugin_package and retrieve all plugins.

        Parameters
        ----------
        package_name : str
            Package to load plugins from.

        """

        logging.debug("Finding plugins from '%s'", package_name)

        imported_package = __import__(package_name, fromlist=["__VERSION__"])

        # Iterate through the modules
        for _, plugin_name, _ in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + "."):

            # Try import
            try:
                plugin_module = __import__(plugin_name, fromlist=["__VERSION__"])
            except ModuleNotFoundError as err:
                self._plugin_status[plugin_name] = f"cannot load module: {err}"
                continue

            # Grab object members
            object_members = inspect.getmembers(plugin_module, inspect.isclass)

            # Loop with class names
            for (_, class_name) in object_members:
                # Only add classes that are a sub class of Plugin
                if not issubclass(class_name, Plugin) or (class_name is Plugin) or class_name.__name__.endswith("Base"):
                    continue
                # Save plugin and record that it was loaded
                self._plugins[plugin_name] = class_name()
                self._plugin_status[plugin_name] = "loaded"
                logging.debug("Plugin loaded '%s' [class=%s]", plugin_name, class_name)

        # Look for modules in sub packages
        all_current_paths: List[str] = []

        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend(imported_package.__path__)

        # Loop with package path
        for pkg_path in all_current_paths:
            # Make sure its not seen in our seen_paths
            if pkg_path in self._seen_paths:
                continue
            # If not add it so we don't process it again
            self._seen_paths.append(pkg_path)

            # Grab all the sub directories of the current package path directory
            sub_dirs = []
            for sub_dir in os.listdir(pkg_path):
                # If the subdir starts with a ., ignore it
                if sub_dir.startswith("."):
                    continue
                # If the subdir is __pycache__, ignore it
                if sub_dir == "__pycache__":
                    continue
                # If this is not a sub dir, then move onto the next one
                if not os.path.isdir(os.path.join(pkg_path, sub_dir)):
                    continue
                # Add sub-directory
                sub_dirs.append(sub_dir)

            # Find packages in sub directory
            for sub_dir in sub_dirs:
                module = f"{package_name}.{sub_dir}"
                self._find_plugins(module)

    @property
    def plugins(self) -> Dict[str, Plugin]:
        """
        Property containing the dictionary of plugins loaded.

        Returns
        -------
        Dict[str, Plugin], keyed by plugin name.

        """

        return self._plugins

    @property
    def plugin_status(self) -> Dict[str, str]:
        """
        Property containing the plugin load status.

        Returns
        -------
        Dict[str, str], keyed by plugin name.

        """

        return self._plugin_status
