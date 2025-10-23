"""
VileHvH - CS:GO Legacy Server Setup & Management
Core package for automated server installation
"""

__version__ = "1.0.0"
__author__ = "VileHvH"
__description__ = "CS:GO Legacy Server Setup Scripts"

# Make key components easily importable
from .logger import get_logger, SetupLogger
from .system_detect import detect_system, SystemInfo, OSType, PackageManager
from .steamcmd_installer import SteamCMDInstaller
from .csgo_installer import CSGOInstaller
from .metamod_sourcemod_installer import MetamodSourcemodInstaller
from .plugin_manager import PluginManager

__all__ = [
    'get_logger',
    'SetupLogger',
    'detect_system',
    'SystemInfo',
    'OSType',
    'PackageManager',
    'SteamCMDInstaller',
    'CSGOInstaller',
    'MetamodSourcemodInstaller',
    'PluginManager',
]

