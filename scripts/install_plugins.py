#!/usr/bin/env python3
"""
Plugin installation utility script
Demonstrates how to install plugins using plugin_manager.py

This script can be extended to install all your favorite HvH plugins!
"""

import sys
import re
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import get_logger
from plugin_manager import PluginManager


def print_usage():
    """Print usage information"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           VileHvH - Plugin Installation Utility              ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  python3 install_plugins.py <server_directory> [plugin_source]

Examples:
  # Install from GitHub URL (with or without .git)
  python3 install_plugins.py ~/csgo-server https://github.com/hvhgg/CSGO-Essentials
  python3 install_plugins.py ~/csgo-server https://github.com/hvhgg/CSGO-Essentials.git
  
  # Install from local directory
  python3 install_plugins.py ~/csgo-server ./CSGO-Essentials-master
  
  # Interactive mode (prompts for GitHub URL or path)
  python3 install_plugins.py ~/csgo-server

Options:
  server_directory    Path to CS:GO server installation
  plugin_source       GitHub URL or local path to plugin (must contain 'addons' folder)
    """)


def is_github_url(source: str) -> bool:
    """Check if the source is a GitHub URL"""
    github_patterns = [
        r'https?://github\.com/[\w-]+/[\w.-]+/?',
        r'git@github\.com:[\w-]+/[\w.-]+\.git',
        r'github\.com/[\w-]+/[\w.-]+',
    ]
    return any(re.match(pattern, source) for pattern in github_patterns)


def normalize_github_url(url: str) -> str:
    """Normalize GitHub URL (add https:// if missing, handle .git)"""
    # Remove trailing .git if present
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    
    # Add https:// if not present
    if not url.startswith(('http://', 'https://', 'git@')):
        url = 'https://' + url
    
    return url


def clone_from_github(url: str) -> Path:
    """
    Clone a GitHub repository to a temporary directory
    
    Returns:
        Path to cloned directory, or None if failed
    """
    logger = get_logger()
    
    # Normalize URL
    url = normalize_github_url(url)
    
    logger.info(f"Cloning from GitHub: {url}")
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="vilehvh_plugin_"))
    
    try:
        # Clone the repository
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', url, str(temp_dir)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"Git clone failed: {result.stderr}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None
        
        logger.success(f"Cloned successfully to: {temp_dir}")
        return temp_dir
    
    except subprocess.TimeoutExpired:
        logger.error("Git clone timed out after 60 seconds")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None
    except FileNotFoundError:
        logger.error("Git is not installed. Please install git first.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None
    except Exception as e:
        logger.error(f"Clone failed: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None


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


def install_plugin(pm: PluginManager, source: str) -> bool:
    """
    Install a plugin from GitHub URL or local directory
    
    Args:
        pm: PluginManager instance
        source: GitHub URL or local directory path
    
    Returns:
        True if successful
    """
    logger = get_logger()
    temp_dir = None
    
    try:
        # Check if it's a GitHub URL
        if is_github_url(source):
            logger.info("Detected GitHub URL")
            temp_dir = clone_from_github(source)
            
            if temp_dir is None:
                return False
            
            # Install from the cloned directory
            success = install_from_directory(pm, temp_dir)
            
        else:
            # Treat as local directory
            plugin_dir = Path(source).expanduser()
            success = install_from_directory(pm, plugin_dir)
        
        return success
    
    finally:
        # Clean up temporary directory
        if temp_dir and temp_dir.exists():
            logger.debug(f"Cleaning up temp directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)


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
    
    # If plugin source provided, install it
    if len(sys.argv) >= 3:
        plugin_source = sys.argv[2]
        
        if install_plugin(pm, plugin_source):
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
    logger.info("")
    logger.info("You can install plugins from:")
    logger.info("  • GitHub URL (with or without .git)")
    logger.info("  • Local directory path")
    logger.info("")
    logger.info("Examples:")
    logger.info("  https://github.com/hvhgg/CSGO-Essentials")
    logger.info("  https://github.com/hvhgg/CSGO-Essentials.git")
    logger.info("  ./CSGO-Essentials-master")
    logger.info("  ~/Downloads/my-plugin")
    
    while True:
        print()
        plugin_source = input("Enter GitHub URL or directory path (or 'quit' to exit): ").strip()
        
        if plugin_source.lower() in ['quit', 'exit', 'q']:
            break
        
        if not plugin_source:
            continue
        
        if install_plugin(pm, plugin_source):
            logger.success("Plugin installed!")
            logger.info("")
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

