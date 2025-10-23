#!/usr/bin/env python3
"""
Plugin management module for CS:GO Legacy server
Handles downloading and installing plugins from GitHub and other sources

NOTE: This is a template/starter for future plugin management.
The user will need to expand this with specific plugin logic for HvH-gg plugins, etc.
"""

import urllib.request
import shutil
import zipfile
from pathlib import Path
from typing import Optional, List
from logger import get_logger


class PluginManager:
    """Manages SourceMod plugins installation and updates"""
    
    def __init__(self, csgo_install_dir: Path):
        self.csgo_install_dir = csgo_install_dir
        self.logger = get_logger()
        
        # SourceMod directories
        self.addons_dir = csgo_install_dir / "csgo" / "addons"
        self.sourcemod_dir = self.addons_dir / "sourcemod"
        self.plugins_dir = self.sourcemod_dir / "plugins"
        self.scripting_dir = self.sourcemod_dir / "scripting"
        self.gamedata_dir = self.sourcemod_dir / "gamedata"
        self.configs_dir = self.sourcemod_dir / "configs"
        self.translations_dir = self.sourcemod_dir / "translations"
    
    def check_sourcemod_installed(self) -> bool:
        """Check if SourceMod is installed"""
        if not self.sourcemod_dir.exists():
            self.logger.error("SourceMod is not installed")
            self.logger.error("Please install SourceMod first")
            return False
        return True
    
    def install_plugin_from_url(self, url: str, plugin_name: str) -> bool:
        """
        Download and install a plugin from a URL
        
        Args:
            url: URL to download plugin from (.smx file or .zip archive)
            plugin_name: Name of the plugin
        
        Returns:
            True if successful, False otherwise
        """
        if not self.check_sourcemod_installed():
            return False
        
        self.logger.info(f"Downloading plugin: {plugin_name}")
        
        # Determine file type from URL
        is_zip = url.endswith('.zip')
        temp_file = Path(f"/tmp/{plugin_name}{'zip' if is_zip else '.smx'}")
        
        try:
            # Download file
            urllib.request.urlretrieve(url, temp_file)
            self.logger.success(f"Downloaded: {plugin_name}")
            
            if is_zip:
                # Extract ZIP archive
                # Most plugins follow this structure:
                # addons/sourcemod/plugins/*.smx
                # addons/sourcemod/scripting/*.sp
                self.logger.info("Extracting plugin archive...")
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    # Extract to csgo directory (one level above addons)
                    zip_ref.extractall(self.addons_dir.parent)
                self.logger.success("Plugin extracted")
            else:
                # Copy .smx file to plugins directory
                dest_file = self.plugins_dir / temp_file.name
                shutil.copy(temp_file, dest_file)
                self.logger.success(f"Plugin installed: {dest_file}")
            
            # Clean up temp file
            temp_file.unlink()
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to install plugin: {e}")
            return False
    
    def install_plugin_from_directory(self, plugin_dir: Path) -> bool:
        """
        Install a plugin from a local directory
        
        Handles plugins with structure like:
        addons/sourcemod/plugins/*.smx
        addons/sourcemod/scripting/*.sp
        
        Args:
            plugin_dir: Path to the plugin directory (containing 'addons' folder)
        
        Returns:
            True if successful, False otherwise
        
        Example:
            install_plugin_from_directory(Path("./CSGO-Essentials-master"))
        """
        if not self.check_sourcemod_installed():
            return False
        
        plugin_addons = plugin_dir / "addons"
        if not plugin_addons.exists():
            self.logger.error(f"Plugin directory missing 'addons' folder: {plugin_dir}")
            return False
        
        self.logger.info(f"Installing plugin from: {plugin_dir}")
        
        try:
            # Copy the entire addons structure
            for item in plugin_addons.rglob("*"):
                if item.is_file():
                    # Calculate relative path from plugin_addons
                    rel_path = item.relative_to(plugin_addons)
                    dest_file = self.addons_dir / rel_path
                    
                    # Create destination directory if needed
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(item, dest_file)
                    self.logger.debug(f"Copied: {rel_path}")
            
            self.logger.success(f"Plugin installed from {plugin_dir.name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to install plugin: {e}")
            return False
    
    def install_github_release(self, repo: str, asset_name: Optional[str] = None) -> bool:
        """
        Install a plugin from a GitHub release
        
        Args:
            repo: GitHub repository (format: "owner/repo")
            asset_name: Name of the asset to download (if None, downloads first .zip)
        
        Returns:
            True if successful, False otherwise
        
        Example:
            install_github_release("HvH-gg/plugin-name")
        """
        if not self.check_sourcemod_installed():
            return False
        
        self.logger.info(f"Installing plugin from GitHub: {repo}")
        
        # This is a placeholder - needs GitHub API integration
        # For now, user should provide direct URLs
        self.logger.warning("GitHub API integration not yet implemented")
        self.logger.warning("Please use install_plugin_from_url() with direct download link")
        return False
    
    def list_installed_plugins(self) -> List[str]:
        """
        List all installed plugins
        
        Returns:
            List of plugin filenames
        """
        if not self.plugins_dir.exists():
            return []
        
        plugins = []
        for plugin_file in self.plugins_dir.glob("*.smx"):
            # Skip disabled plugins (*.smx.disabled)
            if plugin_file.suffix == ".smx":
                plugins.append(plugin_file.name)
        
        return plugins
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin by renaming it
        
        Args:
            plugin_name: Name of the plugin file (with or without .smx)
        
        Returns:
            True if successful, False otherwise
        """
        if not plugin_name.endswith('.smx'):
            plugin_name += '.smx'
        
        plugin_file = self.plugins_dir / plugin_name
        disabled_file = self.plugins_dir / f"{plugin_name}.disabled"
        
        if not plugin_file.exists():
            self.logger.error(f"Plugin not found: {plugin_name}")
            return False
        
        try:
            plugin_file.rename(disabled_file)
            self.logger.success(f"Disabled plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to disable plugin: {e}")
            return False
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a disabled plugin
        
        Args:
            plugin_name: Name of the plugin file (with or without .smx)
        
        Returns:
            True if successful, False otherwise
        """
        if not plugin_name.endswith('.smx'):
            plugin_name += '.smx'
        
        disabled_file = self.plugins_dir / f"{plugin_name}.disabled"
        plugin_file = self.plugins_dir / plugin_name
        
        if not disabled_file.exists():
            self.logger.error(f"Disabled plugin not found: {plugin_name}.disabled")
            return False
        
        try:
            disabled_file.rename(plugin_file)
            self.logger.success(f"Enabled plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enable plugin: {e}")
            return False
    
    def remove_plugin(self, plugin_name: str) -> bool:
        """
        Remove a plugin completely
        
        Args:
            plugin_name: Name of the plugin file (with or without .smx)
        
        Returns:
            True if successful, False otherwise
        """
        if not plugin_name.endswith('.smx'):
            plugin_name += '.smx'
        
        plugin_file = self.plugins_dir / plugin_name
        
        if not plugin_file.exists():
            self.logger.error(f"Plugin not found: {plugin_name}")
            return False
        
        try:
            plugin_file.unlink()
            self.logger.success(f"Removed plugin: {plugin_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove plugin: {e}")
            return False


# Example usage:
if __name__ == "__main__":
    """
    Example of how to use the PluginManager
    
    This would be expanded for actual HvH-gg plugin installation
    """
    from system_detect import detect_system
    
    # Example: Install plugins to an existing server
    server_path = Path.home() / "csgo-server"
    
    if server_path.exists():
        pm = PluginManager(server_path)
        
        # List installed plugins
        plugins = pm.list_installed_plugins()
        print(f"Installed plugins: {plugins}")
        
        # Example: Install a plugin from direct URL
        # pm.install_plugin_from_url(
        #     "https://example.com/plugin.smx",
        #     "example-plugin"
        # )
        
        # Example: Install HvH-gg plugin (would need actual URLs)
        # pm.install_github_release("HvH-gg/plugin-name")
    else:
        print(f"Server not found at {server_path}")
        print("Install the server first using setup.py")

