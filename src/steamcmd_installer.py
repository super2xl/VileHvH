#!/usr/bin/env python3
"""
SteamCMD installation module
Handles installing SteamCMD on different platforms with proper methods
"""

import os
import subprocess
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from typing import Optional
from logger import get_logger
from system_detect import SystemInfo, OSType, PackageManager, run_command, check_command_exists


class SteamCMDInstaller:
    """Handles SteamCMD installation across different platforms"""
    
    def __init__(self, sys_info: SystemInfo):
        self.sys_info = sys_info
        self.logger = get_logger()
        
        # Determine SteamCMD paths based on OS
        if sys_info.os_type == OSType.WINDOWS:
            self.steamcmd_dir = Path("C:/steamcmd")
            self.steamcmd_exe = self.steamcmd_dir / "steamcmd.exe"
        else:
            # Linux: use home directory
            self.steamcmd_dir = Path.home() / "steamcmd"
            self.steamcmd_exe = self.steamcmd_dir / "steamcmd.sh"
    
    def is_installed(self) -> bool:
        """Check if SteamCMD is already installed"""
        if self.steamcmd_exe.exists():
            self.logger.info(f"SteamCMD already installed at: {self.steamcmd_dir}")
            return True
        return False
    
    def install(self) -> bool:
        """
        Install SteamCMD using the appropriate method for the current OS
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.section("Installing SteamCMD")
        
        if self.is_installed():
            self.logger.success("SteamCMD is already installed")
            return True
        
        if self.sys_info.os_type == OSType.LINUX:
            return self._install_linux()
        elif self.sys_info.os_type == OSType.WINDOWS:
            return self._install_windows()
        else:
            self.logger.error(f"Unsupported OS: {self.sys_info.os_type}")
            return False
    
    def _install_linux(self) -> bool:
        """Install SteamCMD on Linux"""
        distro = self.sys_info.distro
        
        # Arch-based distros (use AUR)
        if distro in ["arch", "manjaro", "endeavouros"]:
            return self._install_arch()
        
        # Debian/Ubuntu-based distros
        elif distro in ["ubuntu", "debian", "linuxmint", "pop"]:
            return self._install_debian()
        
        # Fedora/RHEL-based distros
        elif distro in ["fedora", "rhel", "centos"]:
            return self._install_fedora()
        
        # Generic Linux fallback (manual download)
        else:
            self.logger.warning(f"Unknown distro '{distro}', using generic installation method")
            return self._install_linux_generic()
    
    def _install_arch(self) -> bool:
        """Install SteamCMD on Arch Linux using AUR"""
        self.logger.info("Installing SteamCMD via AUR (Arch Linux method)")
        
        # Check for AUR helper
        aur_helper = None
        if PackageManager.YAY in self.sys_info.package_managers:
            aur_helper = "yay"
        elif PackageManager.PARU in self.sys_info.package_managers:
            aur_helper = "paru"
        
        if aur_helper:
            self.logger.info(f"Using AUR helper: {aur_helper}")
            try:
                subprocess.run(
                    [aur_helper, "-S", "--noconfirm", "steamcmd"],
                    check=True
                )
                self.logger.success("SteamCMD installed via AUR helper")
                
                # Update paths for system-wide installation
                self.steamcmd_exe = Path("/usr/bin/steamcmd")
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install via {aur_helper}: {e}")
        
        # Fallback: Manual AUR installation
        self.logger.info("Installing SteamCMD manually from AUR")
        
        # Ensure base-devel is installed
        try:
            subprocess.run(
                ["sudo", "pacman", "-S", "--needed", "--noconfirm", "base-devel"],
                check=True
            )
        except subprocess.CalledProcessError:
            self.logger.warning("Could not ensure base-devel is installed")
        
        # Clone AUR package
        aur_dir = Path("/tmp/steamcmd-aur")
        if aur_dir.exists():
            subprocess.run(["rm", "-rf", str(aur_dir)])
        
        try:
            subprocess.run(
                ["git", "clone", "https://aur.archlinux.org/steamcmd.git", str(aur_dir)],
                check=True
            )
            
            # Build and install
            subprocess.run(
                ["makepkg", "-si", "--noconfirm"],
                cwd=aur_dir,
                check=True
            )
            
            self.logger.success("SteamCMD installed from AUR")
            self.steamcmd_exe = Path("/usr/bin/steamcmd")
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install from AUR: {e}")
            return False
    
    def _install_debian(self) -> bool:
        """Install SteamCMD on Debian/Ubuntu"""
        self.logger.info("Installing SteamCMD on Debian/Ubuntu")
        
        # Enable i386 architecture (32-bit support)
        self.logger.info("Enabling i386 architecture...")
        try:
            subprocess.run(["sudo", "dpkg", "--add-architecture", "i386"], check=True)
            self.logger.success("i386 architecture enabled")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to enable i386 architecture: {e}")
            return False
        
        # Add multiverse repository (Ubuntu)
        if self.sys_info.distro == "ubuntu":
            self.logger.info("Enabling multiverse repository...")
            try:
                subprocess.run(
                    ["sudo", "add-apt-repository", "-y", "multiverse"],
                    check=True
                )
                self.logger.success("Multiverse repository enabled")
            except subprocess.CalledProcessError:
                self.logger.warning("Could not enable multiverse repository")
        
        # Update package list
        self.logger.info("Updating package list...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to update package list: {e}")
            return False
        
        # Install SteamCMD
        self.logger.info("Installing steamcmd package...")
        try:
            subprocess.run(
                ["sudo", "apt", "install", "-y", "steamcmd"],
                check=True
            )
            self.logger.success("SteamCMD installed via apt")
            
            # SteamCMD is usually installed to /usr/games/steamcmd
            self.steamcmd_exe = Path("/usr/games/steamcmd")
            if not self.steamcmd_exe.exists():
                # Alternative location
                self.steamcmd_exe = Path("/usr/bin/steamcmd")
            
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install steamcmd: {e}")
            return False
    
    def _install_fedora(self) -> bool:
        """Install SteamCMD on Fedora/RHEL"""
        self.logger.info("Installing SteamCMD on Fedora/RHEL")
        
        # Fedora doesn't have a native package, use generic method
        return self._install_linux_generic()
    
    def _install_linux_generic(self) -> bool:
        """Generic Linux installation (manual download)"""
        self.logger.info("Installing SteamCMD using generic Linux method")
        
        # Create directory
        self.steamcmd_dir.mkdir(parents=True, exist_ok=True)
        
        # Download SteamCMD
        steamcmd_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
        tar_file = self.steamcmd_dir / "steamcmd_linux.tar.gz"
        
        self.logger.info(f"Downloading SteamCMD from {steamcmd_url}...")
        try:
            urllib.request.urlretrieve(steamcmd_url, tar_file)
            self.logger.success("Download complete")
        except Exception as e:
            self.logger.error(f"Failed to download SteamCMD: {e}")
            return False
        
        # Extract tarball
        self.logger.info("Extracting SteamCMD...")
        try:
            with tarfile.open(tar_file, "r:gz") as tar:
                tar.extractall(self.steamcmd_dir)
            self.logger.success("Extraction complete")
            
            # Make executable
            self.steamcmd_exe.chmod(0o755)
            
            # Clean up tarball
            tar_file.unlink()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to extract SteamCMD: {e}")
            return False
    
    def _install_windows(self) -> bool:
        """Install SteamCMD on Windows"""
        self.logger.info("Installing SteamCMD on Windows")
        
        # Create directory at C:\steamcmd
        self.steamcmd_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {self.steamcmd_dir}")
        
        # Download SteamCMD
        steamcmd_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        zip_file = self.steamcmd_dir / "steamcmd.zip"
        
        self.logger.info(f"Downloading SteamCMD from {steamcmd_url}...")
        try:
            urllib.request.urlretrieve(steamcmd_url, zip_file)
            self.logger.success("Download complete")
        except Exception as e:
            self.logger.error(f"Failed to download SteamCMD: {e}")
            return False
        
        # Extract ZIP
        self.logger.info("Extracting SteamCMD...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.steamcmd_dir)
            self.logger.success("Extraction complete")
            
            # Clean up ZIP file
            zip_file.unlink()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to extract SteamCMD: {e}")
            return False
    
    def get_steamcmd_path(self) -> Path:
        """Get the path to the SteamCMD executable"""
        return self.steamcmd_exe
    
    def run_initial_update(self) -> bool:
        """
        Run SteamCMD once to perform initial update
        This ensures SteamCMD is fully installed and updated
        """
        self.logger.info("Running initial SteamCMD update...")
        
        try:
            subprocess.run(
                [str(self.steamcmd_exe), "+quit"],
                check=True,
                cwd=self.steamcmd_dir
            )
            self.logger.success("SteamCMD initial update complete")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to run initial update: {e}")
            return False

