#!/usr/bin/env python3
"""
Metamod:Source and SourceMod installation module
Handles downloading and installing metamod and sourcemod to CS:GO server
"""

import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import Optional
from logger import get_logger
from system_detect import SystemInfo, OSType


class MetamodSourcemodInstaller:
    """Handles installation of Metamod:Source and SourceMod"""
    
    # Latest stable versions as of implementation
    # These URLs point to the latest builds
    METAMOD_URL = "https://mms.alliedmods.net/mmsdrop/1.11/mmsource-1.11.0-git1148-linux.tar.gz"
    METAMOD_URL_WIN = "https://mms.alliedmods.net/mmsdrop/1.11/mmsource-1.11.0-git1148-windows.zip"
    
    SOURCEMOD_URL = "https://sm.alliedmods.net/smdrop/1.11/sourcemod-1.11.0-git6968-linux.tar.gz"
    SOURCEMOD_URL_WIN = "https://sm.alliedmods.net/smdrop/1.11/sourcemod-1.11.0-git6968-windows.zip"
    
    def __init__(self, sys_info: SystemInfo, csgo_install_dir: Path):
        self.sys_info = sys_info
        self.csgo_install_dir = csgo_install_dir
        self.logger = get_logger()
        
        # CS:GO server directories
        self.csgo_dir = csgo_install_dir / "csgo"
        self.addons_dir = self.csgo_dir / "addons"
        self.cfg_dir = self.csgo_dir / "cfg"
        
        # Determine which URLs to use based on OS
        if sys_info.os_type == OSType.WINDOWS:
            self.metamod_url = self.METAMOD_URL_WIN
            self.sourcemod_url = self.SOURCEMOD_URL_WIN
            self.archive_ext = ".zip"
        else:
            self.metamod_url = self.METAMOD_URL
            self.sourcemod_url = self.SOURCEMOD_URL
            self.archive_ext = ".tar.gz"
    
    def check_prerequisites(self) -> bool:
        """Check if CS:GO server is installed"""
        if not self.csgo_dir.exists():
            self.logger.error(f"CS:GO server directory not found: {self.csgo_dir}")
            self.logger.error("Please install CS:GO server first")
            return False
        return True
    
    def is_metamod_installed(self) -> bool:
        """Check if Metamod:Source is installed"""
        metamod_vdf = self.addons_dir / "metamod.vdf"
        metamod_bin = self.addons_dir / "metamod"
        return metamod_vdf.exists() or metamod_bin.exists()
    
    def is_sourcemod_installed(self) -> bool:
        """Check if SourceMod is installed"""
        sourcemod_dir = self.addons_dir / "sourcemod"
        return sourcemod_dir.exists()
    
    def install_metamod(self, force: bool = False) -> bool:
        """
        Install Metamod:Source
        
        Args:
            force: Force reinstall even if already installed
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.section("Installing Metamod:Source")
        
        if not self.check_prerequisites():
            return False
        
        if self.is_metamod_installed() and not force:
            self.logger.info("Metamod:Source is already installed")
            return True
        
        # Create addons directory
        self.addons_dir.mkdir(parents=True, exist_ok=True)
        
        # Download Metamod
        temp_file = Path(f"/tmp/metamod{self.archive_ext}")
        
        self.logger.info(f"Downloading Metamod:Source from {self.metamod_url}...")
        try:
            urllib.request.urlretrieve(self.metamod_url, temp_file)
            self.logger.success("Download complete")
        except Exception as e:
            self.logger.error(f"Failed to download Metamod:Source: {e}")
            self.logger.warning("Please check if the URL is still valid")
            return False
        
        # Extract archive
        self.logger.info("Extracting Metamod:Source...")
        try:
            if self.archive_ext == ".zip":
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(self.csgo_dir)
            else:
                import tarfile
                with tarfile.open(temp_file, 'r:gz') as tar:
                    tar.extractall(self.csgo_dir)
            
            self.logger.success("Metamod:Source extracted successfully")
            
            # Clean up temp file
            temp_file.unlink()
            
            # Verify installation
            if self.is_metamod_installed():
                self.logger.success("Metamod:Source installation verified")
                return True
            else:
                self.logger.error("Metamod:Source installation verification failed")
                return False
        
        except Exception as e:
            self.logger.error(f"Failed to extract Metamod:Source: {e}")
            return False
    
    def install_sourcemod(self, force: bool = False) -> bool:
        """
        Install SourceMod
        
        Args:
            force: Force reinstall even if already installed
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.section("Installing SourceMod")
        
        if not self.check_prerequisites():
            return False
        
        if not self.is_metamod_installed():
            self.logger.error("Metamod:Source must be installed before SourceMod")
            return False
        
        if self.is_sourcemod_installed() and not force:
            self.logger.info("SourceMod is already installed")
            return True
        
        # Download SourceMod
        temp_file = Path(f"/tmp/sourcemod{self.archive_ext}")
        
        self.logger.info(f"Downloading SourceMod from {self.sourcemod_url}...")
        try:
            urllib.request.urlretrieve(self.sourcemod_url, temp_file)
            self.logger.success("Download complete")
        except Exception as e:
            self.logger.error(f"Failed to download SourceMod: {e}")
            self.logger.warning("Please check if the URL is still valid")
            return False
        
        # Extract archive
        self.logger.info("Extracting SourceMod...")
        try:
            if self.archive_ext == ".zip":
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(self.csgo_dir)
            else:
                import tarfile
                with tarfile.open(temp_file, 'r:gz') as tar:
                    tar.extractall(self.csgo_dir)
            
            self.logger.success("SourceMod extracted successfully")
            
            # Clean up temp file
            temp_file.unlink()
            
            # Verify installation
            if self.is_sourcemod_installed():
                self.logger.success("SourceMod installation verified")
                return True
            else:
                self.logger.error("SourceMod installation verification failed")
                return False
        
        except Exception as e:
            self.logger.error(f"Failed to extract SourceMod: {e}")
            return False
    
    def install_all(self, force: bool = False) -> bool:
        """
        Install both Metamod:Source and SourceMod
        
        Args:
            force: Force reinstall even if already installed
        
        Returns:
            True if both installed successfully, False otherwise
        """
        self.logger.section("Installing Metamod:Source and SourceMod")
        
        # Install Metamod first
        if not self.install_metamod(force):
            return False
        
        # Then install SourceMod
        if not self.install_sourcemod(force):
            return False
        
        self.logger.success("Metamod:Source and SourceMod installation complete!")
        return True
    
    def add_admin(self, steam_id: str, admin_name: str = "Admin", flags: str = "z") -> bool:
        """
        Add an admin to SourceMod admins_simple.ini
        
        Args:
            steam_id: Steam ID (STEAM_X:X:XXXXXX format)
            admin_name: Display name for the admin
            flags: Admin flags (default "z" = root)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_sourcemod_installed():
            self.logger.error("SourceMod must be installed first")
            return False
        
        admins_file = self.addons_dir / "sourcemod" / "configs" / "admins_simple.ini"
        
        if not admins_file.exists():
            self.logger.error(f"admins_simple.ini not found: {admins_file}")
            return False
        
        # Add admin to file
        admin_line = f'"{steam_id}" "{flags}" // {admin_name}\n'
        
        try:
            with open(admins_file, 'a') as f:
                f.write(admin_line)
            
            self.logger.success(f"Added admin: {admin_name} ({steam_id}) with flags '{flags}'")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to add admin: {e}")
            return False

