#!/usr/bin/env python3
"""
System detection module for OS, distro, and package manager detection
"""

import platform
import subprocess
import shutil
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from logger import get_logger


class OSType(Enum):
    """Supported operating systems"""
    LINUX = "linux"
    WINDOWS = "windows"
    UNKNOWN = "unknown"


class PackageManager(Enum):
    """Supported package managers"""
    PACMAN = "pacman"
    YAY = "yay"
    PARU = "paru"
    APT = "apt"
    DNF = "dnf"
    WINGET = "winget"
    CHOCO = "choco"
    UNKNOWN = "unknown"


@dataclass
class SystemInfo:
    """System information container"""
    os_type: OSType
    os_name: str
    os_version: str
    distro: Optional[str]
    distro_version: Optional[str]
    package_managers: List[PackageManager]
    architecture: str
    
    def __str__(self):
        pm_list = ", ".join([pm.value for pm in self.package_managers])
        result = [
            f"OS: {self.os_name} ({self.os_type.value})",
            f"Version: {self.os_version}",
            f"Architecture: {self.architecture}",
        ]
        if self.distro:
            result.append(f"Distribution: {self.distro} {self.distro_version or ''}")
        result.append(f"Package Managers: {pm_list}")
        return "\n".join(result)


def run_command(cmd: List[str], capture_output: bool = True) -> tuple[bool, str]:
    """
    Run a command and return success status and output
    
    Args:
        cmd: Command and arguments as list
        capture_output: Whether to capture output
    
    Returns:
        Tuple of (success, output)
    """
    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout.strip()
        else:
            result = subprocess.run(cmd, timeout=10)
            return result.returncode == 0, ""
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False, ""


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH"""
    return shutil.which(cmd) is not None


def detect_linux_distro() -> tuple[Optional[str], Optional[str]]:
    """
    Detect Linux distribution and version
    
    Returns:
        Tuple of (distro_name, distro_version)
    """
    logger = get_logger()
    
    # Try /etc/os-release first (most modern distros)
    try:
        with open("/etc/os-release", "r") as f:
            os_release = {}
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    os_release[key] = value.strip('"')
            
            distro_name = os_release.get("ID", "unknown")
            distro_version = os_release.get("VERSION_ID", "")
            
            logger.debug(f"Detected distro from /etc/os-release: {distro_name} {distro_version}")
            return distro_name, distro_version
    except FileNotFoundError:
        logger.debug("/etc/os-release not found")
    
    # Fallback: Try lsb_release command
    success, output = run_command(["lsb_release", "-is"])
    if success:
        distro_name = output.lower()
        success_v, version = run_command(["lsb_release", "-rs"])
        distro_version = version if success_v else ""
        logger.debug(f"Detected distro from lsb_release: {distro_name} {distro_version}")
        return distro_name, distro_version
    
    return None, None


def detect_package_managers() -> List[PackageManager]:
    """
    Detect available package managers on the system
    
    Returns:
        List of detected package managers
    """
    logger = get_logger()
    managers = []
    
    # Check for each package manager
    if check_command_exists("yay"):
        managers.append(PackageManager.YAY)
        logger.debug("Found package manager: yay")
    
    if check_command_exists("paru"):
        managers.append(PackageManager.PARU)
        logger.debug("Found package manager: paru")
    
    if check_command_exists("pacman"):
        managers.append(PackageManager.PACMAN)
        logger.debug("Found package manager: pacman")
    
    if check_command_exists("apt"):
        managers.append(PackageManager.APT)
        logger.debug("Found package manager: apt")
    
    if check_command_exists("dnf"):
        managers.append(PackageManager.DNF)
        logger.debug("Found package manager: dnf")
    
    if check_command_exists("winget"):
        managers.append(PackageManager.WINGET)
        logger.debug("Found package manager: winget")
    
    if check_command_exists("choco"):
        managers.append(PackageManager.CHOCO)
        logger.debug("Found package manager: choco")
    
    if not managers:
        managers.append(PackageManager.UNKNOWN)
        logger.warning("No known package managers detected")
    
    return managers


def detect_system() -> SystemInfo:
    """
    Detect system information including OS, distro, and package managers
    
    Returns:
        SystemInfo object with detected information
    """
    logger = get_logger()
    logger.section("System Detection")
    
    # Detect OS type
    system = platform.system().lower()
    
    if system == "linux":
        os_type = OSType.LINUX
        os_name = "Linux"
        os_version = platform.release()
        distro, distro_version = detect_linux_distro()
    elif system == "windows":
        os_type = OSType.WINDOWS
        os_name = "Windows"
        os_version = platform.version()
        distro = None
        distro_version = None
    else:
        os_type = OSType.UNKNOWN
        os_name = system
        os_version = platform.release()
        distro = None
        distro_version = None
    
    # Detect architecture
    architecture = platform.machine()
    
    # Detect package managers
    package_managers = detect_package_managers()
    
    # Create system info object
    sys_info = SystemInfo(
        os_type=os_type,
        os_name=os_name,
        os_version=os_version,
        distro=distro,
        distro_version=distro_version,
        package_managers=package_managers,
        architecture=architecture
    )
    
    logger.info("System information detected:")
    for line in str(sys_info).split("\n"):
        logger.info(f"  {line}")
    
    return sys_info


def check_package_installed(package_name: str, sys_info: SystemInfo) -> bool:
    """
    Check if a package is installed using available package managers
    
    Args:
        package_name: Name of the package to check
        sys_info: System information
    
    Returns:
        True if package is installed, False otherwise
    """
    logger = get_logger()
    
    for pm in sys_info.package_managers:
        if pm == PackageManager.PACMAN:
            success, _ = run_command(["pacman", "-Q", package_name])
            if success:
                logger.debug(f"Package {package_name} is installed (pacman)")
                return True
        
        elif pm == PackageManager.APT:
            success, output = run_command(["dpkg", "-l", package_name])
            if success and package_name in output:
                logger.debug(f"Package {package_name} is installed (apt/dpkg)")
                return True
        
        elif pm == PackageManager.DNF:
            success, _ = run_command(["dnf", "list", "installed", package_name])
            if success:
                logger.debug(f"Package {package_name} is installed (dnf)")
                return True
        
        elif pm == PackageManager.WINGET:
            success, output = run_command(["winget", "list", "--id", package_name])
            if success and package_name in output:
                logger.debug(f"Package {package_name} is installed (winget)")
                return True
        
        elif pm == PackageManager.CHOCO:
            success, output = run_command(["choco", "list", "--local-only", package_name])
            if success and package_name in output:
                logger.debug(f"Package {package_name} is installed (choco)")
                return True
    
    logger.debug(f"Package {package_name} is not installed")
    return False

