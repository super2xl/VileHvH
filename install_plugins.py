#!/usr/bin/env python3
"""
Plugin installation utility script
Demonstrates how to install plugins using plugin_manager.py

This script can be extended to install all your favorite HvH plugins!
"""

import sys
from pathlib import Path
from logger import get_logger
from plugin_manager import PluginManager


def print_usage():
    """Print usage information"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           VileHvH - Plugin Installation Utility              ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  python3 install_plugins.py <server_directory> [plugin_directory]

Examples:
  # Install from local directory
  python3 install_plugins.py ~/csgo-server ./CSGO-Essentials-master
  
  # Interactive mode (prompts for paths)
  python3 install_plugins.py ~/csgo-server

Options:
  server_directory    Path to CS:GO server installation
  plugin_directory    Path to plugin directory (must contain 'addons' folder)
    """)


def install_from_directory(pm: PluginManager, plugin_dir: Path):
    """Install a plugin from a local directory"""
    logger = get_logger()
    
    logger.section(f"Installing Plugin from Directory")
    logger.info(f"Plugin directory: {plugin_dir}")
    
    if not plugin_dir.exists():
        logger.error(f"Plugin directory not found: {plugin_dir}")
        return False
    
    # Check if it has the expected structure
    addons_dir = plugin_dir / "addons"
    if not addons_dir.exists():
        logger.error("Plugin directory must contain an 'addons' folder")
        logger.info("Expected structure:")
        logger.info("  plugin-name/")
        logger.info("    └── addons/")
        logger.info("        └── sourcemod/")
        logger.info("            ├── plugins/*.smx")
        logger.info("            └── scripting/*.sp")
        return False
    
    # Install the plugin
    return pm.install_plugin_from_directory(plugin_dir)


def list_plugins(pm: PluginManager):
    """List all installed plugins"""
    logger = get_logger()
    
    logger.section("Installed Plugins")
    plugins = pm.list_installed_plugins()
    
    if not plugins:
        logger.info("No plugins installed yet")
    else:
        logger.info(f"Found {len(plugins)} plugin(s):")
        for plugin in plugins:
            logger.info(f"  • {plugin}")


def main():
    """Main entry point"""
    logger = get_logger()
    
    # Check arguments
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_usage()
        return 0
    
    # Get server directory
    server_dir = Path(sys.argv[1])
    
    if not server_dir.exists():
        logger.error(f"Server directory not found: {server_dir}")
        return 1
    
    # Initialize plugin manager
    pm = PluginManager(server_dir)
    
    # Check if SourceMod is installed
    if not pm.check_sourcemod_installed():
        logger.error("Please install SourceMod first using setup.py")
        return 1
    
    # List currently installed plugins
    list_plugins(pm)
    
    # If plugin directory provided, install it
    if len(sys.argv) >= 3:
        plugin_dir = Path(sys.argv[2])
        
        if install_from_directory(pm, plugin_dir):
            logger.success("Plugin installation complete!")
            logger.info("")
            list_plugins(pm)
            return 0
        else:
            logger.error("Plugin installation failed")
            return 1
    
    # Interactive mode
    logger.info("")
    logger.info("=" * 60)
    logger.info("Interactive Plugin Installation")
    logger.info("=" * 60)
    
    while True:
        print()
        plugin_path = input("Enter plugin directory path (or 'quit' to exit): ").strip()
        
        if plugin_path.lower() in ['quit', 'exit', 'q']:
            break
        
        if not plugin_path:
            continue
        
        plugin_dir = Path(plugin_path)
        
        if install_from_directory(pm, plugin_dir):
            logger.success("Plugin installed!")
            list_plugins(pm)
        else:
            logger.error("Installation failed, try again")
    
    logger.info("Done!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)

