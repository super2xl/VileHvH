#!/usr/bin/env python3
"""
CS:GO Legacy Server Setup Script
Main orchestration script for installing and configuring CS:GO Legacy servers
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import get_logger
from system_detect import detect_system, OSType
from steamcmd_installer import SteamCMDInstaller
from csgo_installer import CSGOInstaller
from metamod_sourcemod_installer import MetamodSourcemodInstaller


def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     CS:GO Legacy Server Setup Script                        ║
║     Automated installation for Linux & Windows              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """
    Prompt user for yes/no answer
    
    Args:
        question: Question to ask
        default: Default answer if user just presses Enter
    
    Returns:
        True for yes, False for no
    """
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        response = input(f"{question} {suffix}: ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please answer 'y' or 'n'")


def get_steam_credentials():
    """
    Get Steam credentials from user
    
    Returns:
        Tuple of (username, password, is_first_login)
    """
    logger = get_logger()
    
    print("\n" + "="*60)
    print("Steam Login Information")
    print("="*60)
    
    username = input("Steam username: ").strip()
    
    is_first_login = prompt_yes_no(
        "Is this your first time logging in on this machine?",
        default=True
    )
    
    password = None
    if is_first_login:
        import getpass
        password = getpass.getpass("Steam password: ")
    
    return username, password, is_first_login


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CS:GO Legacy Server Setup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full automated setup (interactive)
  python setup.py
  
  # Custom installation directory
  python setup.py --install-dir /opt/csgo-server
  
  # Skip CS:GO installation (only install mods)
  python setup.py --skip-csgo
  
  # Skip metamod/sourcemod installation
  python setup.py --skip-mods
        """
    )
    
    parser.add_argument(
        '--install-dir',
        type=str,
        help='Custom installation directory for CS:GO server'
    )
    
    parser.add_argument(
        '--skip-steamcmd',
        action='store_true',
        help='Skip SteamCMD installation (assumes already installed)'
    )
    
    parser.add_argument(
        '--skip-csgo',
        action='store_true',
        help='Skip CS:GO server installation'
    )
    
    parser.add_argument(
        '--skip-mods',
        action='store_true',
        help='Skip Metamod:Source and SourceMod installation'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        default=True,
        help='Validate CS:GO server files (default: True)'
    )
    
    parser.add_argument(
        '--no-validate',
        action='store_false',
        dest='validate',
        help='Skip validation of CS:GO server files'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Initialize logger
    logger = get_logger()
    
    try:
        # Step 1: System Detection
        sys_info = detect_system()
        
        # Check if OS is supported
        if sys_info.os_type == OSType.UNKNOWN:
            logger.error("Unsupported operating system")
            logger.error("This script supports Windows and Linux only")
            return 1
        
        # Step 2: Install SteamCMD
        if not args.skip_steamcmd:
            steamcmd_installer = SteamCMDInstaller(sys_info)
            
            if not steamcmd_installer.install():
                logger.error("SteamCMD installation failed")
                return 1
            
            # Run initial update
            if not steamcmd_installer.is_installed():
                logger.error("SteamCMD installation verification failed")
                return 1
            
            logger.info("Running initial SteamCMD update...")
            steamcmd_installer.run_initial_update()
            
            steamcmd_path = steamcmd_installer.get_steamcmd_path()
        else:
            logger.info("Skipping SteamCMD installation")
            # Assume default paths
            if sys_info.os_type == OSType.WINDOWS:
                steamcmd_path = Path("C:/steamcmd/steamcmd.exe")
            else:
                steamcmd_path = Path.home() / "steamcmd" / "steamcmd.sh"
            
            if not steamcmd_path.exists():
                logger.error(f"SteamCMD not found at: {steamcmd_path}")
                return 1
        
        # Step 3: Install CS:GO Server
        if not args.skip_csgo:
            csgo_installer = CSGOInstaller(sys_info, steamcmd_path)
            
            # Set custom install directory if provided
            if args.install_dir:
                csgo_installer.set_install_directory(args.install_dir)
            else:
                # Use default and inform user
                default_dir = csgo_installer.get_install_dir()
                logger.info(f"Using default installation directory: {default_dir}")
                
                if prompt_yes_no("Would you like to use a custom directory?", default=False):
                    custom_dir = input("Enter custom installation path: ").strip()
                    csgo_installer.set_install_directory(custom_dir)
            
            # Configure force_install_dir (must be done before login)
            if not csgo_installer.configure_install_dir():
                logger.error("Failed to configure installation directory")
                return 1
            
            # Get Steam credentials
            username, password, is_first_login = get_steam_credentials()
            
            # Login to Steam
            if not csgo_installer.login(username, password, is_first_login):
                logger.error("Steam login failed")
                return 1
            
            # Install CS:GO server
            if not csgo_installer.install_server(username, validate=args.validate):
                logger.error("CS:GO server installation failed")
                return 1
            
            install_dir = csgo_installer.get_install_dir()
        else:
            logger.info("Skipping CS:GO server installation")
            
            # Need to get install directory
            if args.install_dir:
                install_dir = Path(args.install_dir)
            else:
                install_dir_input = input("Enter CS:GO server installation directory: ").strip()
                install_dir = Path(install_dir_input)
            
            if not install_dir.exists():
                logger.error(f"CS:GO server directory not found: {install_dir}")
                return 1
        
        # Step 4: Install Metamod:Source and SourceMod
        if not args.skip_mods:
            mod_installer = MetamodSourcemodInstaller(sys_info, install_dir)
            
            if not mod_installer.install_all():
                logger.error("Metamod/SourceMod installation failed")
                logger.warning("You may need to check the download URLs")
                return 1
        else:
            logger.info("Skipping Metamod:Source and SourceMod installation")
        
        # Success!
        logger.section("Setup Complete!")
        logger.success("CS:GO Legacy server setup completed successfully!")
        logger.info("")
        logger.info("Server installation directory:")
        logger.info(f"  {install_dir}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Configure server settings (server.cfg)")
        logger.info("  2. Add SourceMod admins if needed")
        logger.info("  3. Install additional plugins")
        logger.info("  4. Start your server!")
        logger.info("")
        
        if sys_info.os_type == OSType.WINDOWS:
            logger.info("To start the server (Windows):")
            logger.info(f"  cd {install_dir}")
            logger.info("  srcds.exe -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2")
        else:
            logger.info("To start the server (Linux):")
            logger.info(f"  cd {install_dir}")
            logger.info("  ./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2")
        
        return 0
    
    except KeyboardInterrupt:
        logger.warning("\nSetup interrupted by user")
        return 130
    
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        logger.critical("Please check the log file for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())

