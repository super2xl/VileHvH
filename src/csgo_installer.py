#!/usr/bin/env python3
"""
CS:GO Legacy server installation module
Handles server installation, login, and configuration
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from logger import get_logger
from system_detect import SystemInfo, OSType


class CSGOInstaller:
    """Handles CS:GO Legacy server installation and management"""
    
    CSGO_APP_ID = "740"
    
    def __init__(self, sys_info: SystemInfo, steamcmd_path: Path):
        self.sys_info = sys_info
        self.steamcmd_path = steamcmd_path
        self.logger = get_logger()
        
        # Determine install path based on OS
        if sys_info.os_type == OSType.WINDOWS:
            self.install_dir = Path("C:/csgo-server")
        else:
            self.install_dir = Path.home() / "csgo-server"
        
        self.first_login = False
    
    def set_install_directory(self, custom_path: Optional[str] = None):
        """
        Set the CS:GO server installation directory
        
        Args:
            custom_path: Optional custom path for installation
        """
        if custom_path:
            self.install_dir = Path(custom_path)
        
        self.logger.info(f"CS:GO server will be installed to: {self.install_dir}")
        self.install_dir.mkdir(parents=True, exist_ok=True)
    
    def configure_install_dir(self) -> bool:
        """
        Configure the force_install_dir in SteamCMD
        This MUST be done while logged out, before first login
        """
        self.logger.info("Configuring installation directory (must be done before login)...")
        
        try:
            # Run SteamCMD with force_install_dir and quit
            # This sets the install directory for subsequent commands
            cmd = [
                str(self.steamcmd_path),
                f"+force_install_dir {self.install_dir}",
                "+quit"
            ]
            
            subprocess.run(
                cmd,
                check=True,
                cwd=self.steamcmd_path.parent
            )
            
            self.logger.success(f"Installation directory configured: {self.install_dir}")
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to configure installation directory: {e}")
            return False
    
    def login(self, username: str, password: Optional[str] = None, is_first_login: bool = False) -> bool:
        """
        Login to Steam via SteamCMD
        
        Args:
            username: Steam username
            password: Steam password (only needed for first login)
            is_first_login: Whether this is the first login (requires Steam Guard)
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.section(f"Logging in to Steam as '{username}'")
        
        if is_first_login:
            if not password:
                self.logger.error("Password is required for first login")
                return False
            
            self.logger.warning("=" * 60)
            self.logger.warning("IMPORTANT: First-time login requires Steam Guard code")
            self.logger.warning("After entering your Steam Guard code, type 'exit' and press Enter")
            self.logger.warning("This will cache your credentials for future logins")
            self.logger.warning("=" * 60)
            
            # First login with password - interactive mode
            try:
                cmd = [
                    str(self.steamcmd_path),
                    f"+force_install_dir {self.install_dir}",
                    f"+login {username} {password}"
                ]
                
                self.logger.info("Starting SteamCMD for first-time login...")
                self.logger.info("You will need to enter your Steam Guard code when prompted")
                
                # Run interactively so user can enter Steam Guard code
                process = subprocess.Popen(
                    cmd,
                    cwd=self.steamcmd_path.parent,
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr
                )
                
                # Wait for user to complete login and type 'exit'
                process.wait()
                
                if process.returncode == 0:
                    self.logger.success("First-time login successful! Credentials cached")
                    self.first_login = True
                    return True
                else:
                    self.logger.error("Login failed")
                    return False
            
            except Exception as e:
                self.logger.error(f"Login error: {e}")
                return False
        
        else:
            # Subsequent logins - credentials are cached, no password needed
            self.logger.info("Using cached credentials...")
            try:
                cmd = [
                    str(self.steamcmd_path),
                    f"+force_install_dir {self.install_dir}",
                    f"+login {username}",
                    "+quit"
                ]
                
                subprocess.run(
                    cmd,
                    check=True,
                    cwd=self.steamcmd_path.parent
                )
                
                self.logger.success("Login successful (cached credentials)")
                return True
            
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Login failed: {e}")
                return False
    
    def install_server(self, username: str, validate: bool = True) -> bool:
        """
        Download/update CS:GO Legacy server
        
        Args:
            username: Steam username (must be logged in)
            validate: Whether to validate game files
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.section("Installing/Updating CS:GO Legacy Server")
        
        # Build command
        validate_flag = "validate" if validate else ""
        
        cmd = [
            str(self.steamcmd_path),
            f"+force_install_dir {self.install_dir}",
            f"+login {username}",
            f"+app_update {self.CSGO_APP_ID} {validate_flag}",
            "+quit"
        ]
        
        self.logger.info(f"Downloading CS:GO (App ID: {self.CSGO_APP_ID})...")
        if validate:
            self.logger.info("Validation enabled - this may take longer")
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=self.steamcmd_path.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Stream output
            if process.stdout:
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        # Show progress updates
                        if "Update state" in line or "progress:" in line.lower():
                            self.logger.info(line)
                        elif "Success!" in line:
                            self.logger.success(line)
            
            process.wait()
            
            if process.returncode == 0:
                self.logger.success("CS:GO server installation complete!")
                
                # Fix bundled library issues on Linux
                if self.sys_info.os_type == OSType.LINUX:
                    self._fix_bundled_libraries()
                
                return True
            else:
                self.logger.error(f"Installation failed with code {process.returncode}")
                return False
        
        except Exception as e:
            self.logger.error(f"Installation error: {e}")
            return False
    
    def _fix_bundled_libraries(self) -> bool:
        """
        Fix bundled library conflicts on Linux
        
        CS:GO ships with old bundled libraries that conflict with system libs.
        This renames them so the server uses system libraries instead.
        
        Returns:
            True if successful or not needed
        """
        self.logger.info("Fixing bundled library conflicts...")
        
        bin_dir = self.install_dir / "bin"
        if not bin_dir.exists():
            self.logger.debug("bin directory not found, skipping library fix")
            return True
        
        # Libraries to rename (force use of system versions)
        libs_to_fix = [
            "libgcc_s.so.1",
            "libstdc++.so.6"
        ]
        
        fixed_count = 0
        for lib in libs_to_fix:
            lib_path = bin_dir / lib
            if lib_path.exists():
                backup_path = bin_dir / f"{lib}.bak"
                try:
                    lib_path.rename(backup_path)
                    self.logger.debug(f"Renamed {lib} -> {lib}.bak")
                    fixed_count += 1
                except Exception as e:
                    self.logger.warning(f"Could not rename {lib}: {e}")
            else:
                self.logger.debug(f"{lib} not found, no fix needed")
        
        if fixed_count > 0:
            self.logger.success(f"Fixed {fixed_count} bundled library conflict(s)")
        else:
            self.logger.debug("No bundled library fixes needed")
        
        return True
    
    def is_installed(self) -> bool:
        """Check if CS:GO server is installed"""
        # Check for essential game files
        if self.sys_info.os_type == OSType.WINDOWS:
            server_exe = self.install_dir / "srcds.exe"
        else:
            server_exe = self.install_dir / "srcds_run"
        
        return server_exe.exists()
    
    def get_install_dir(self) -> Path:
        """Get the server installation directory"""
        return self.install_dir

