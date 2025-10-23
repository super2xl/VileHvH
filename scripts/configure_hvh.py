#!/usr/bin/env python3
"""
HvH Server Configuration Script
Configures a CS:GO Legacy server specifically for Hack vs Hack gameplay
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import get_logger
from server_config import ServerConfigurator


def print_banner():
    """Print HvH configuration banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║          VileHvH - HvH Server Configuration                  ║
║          Configure your CS:GO Legacy HvH server              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Configure CS:GO Legacy server for HvH gameplay"
    )
    
    parser.add_argument(
        'server_dir',
        type=str,
        help='Path to CS:GO server installation directory'
    )
    
    parser.add_argument(
        '--hostname',
        type=str,
        default='VileHvH Server',
        help='Server hostname (default: VileHvH Server)'
    )
    
    parser.add_argument(
        '--rcon-password',
        type=str,
        default='change_me_now',
        help='RCON password (default: change_me_now)'
    )
    
    parser.add_argument(
        '--password',
        type=str,
        default='',
        help='Server password (default: none/public)'
    )
    
    parser.add_argument(
        '--tickrate',
        type=int,
        choices=[64, 128],
        default=128,
        help='Server tickrate (default: 128)'
    )
    
    parser.add_argument(
        '--map',
        type=str,
        default='de_mirage',
        help='Starting map (default: de_mirage)'
    )
    
    parser.add_argument(
        '--maxplayers',
        type=int,
        default=10,
        help='Max players (default: 10)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=27015,
        help='Server port (default: 27015)'
    )
    
    parser.add_argument(
        '--skip-steam-inf',
        action='store_true',
        help='Skip steam.inf modification (not recommended)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Initialize logger
    logger = get_logger()
    
    # Validate server directory
    server_dir = Path(args.server_dir)
    if not server_dir.exists():
        logger.error(f"Server directory not found: {server_dir}")
        logger.error("Please install the server first using scripts/setup.py")
        return 1
    
    csgo_dir = server_dir / "csgo"
    if not csgo_dir.exists():
        logger.error(f"CS:GO directory not found: {csgo_dir}")
        logger.error("This doesn't appear to be a valid CS:GO server installation")
        return 1
    
    # Initialize configurator
    configurator = ServerConfigurator(server_dir)
    
    # Create HvH configuration
    logger.info("Configuring HvH server settings...")
    if not configurator.create_hvh_config(
        hostname=args.hostname,
        rcon_password=args.rcon_password,
        sv_password=args.password,
        tickrate=args.tickrate
    ):
        logger.error("Failed to create HvH configuration")
        return 1
    
    # Set CS:GO Legacy version
    if not args.skip_steam_inf:
        if not configurator.set_legacy_version():
            logger.warning("Failed to set legacy version in steam.inf")
            logger.warning("Server may not work correctly without this!")
    else:
        logger.info("Skipped steam.inf modification (as requested)")
    
    # Generate launch command
    launch_cmd = configurator.get_hvh_launch_command(
        map_name=args.map,
        tickrate=args.tickrate,
        maxplayers=args.maxplayers,
        port=args.port
    )
    
    # Success summary
    logger.section("HvH Configuration Complete!")
    logger.success("Server configured for HvH gameplay")
    logger.info("")
    logger.info("Configuration Summary:")
    logger.info(f"  Hostname: {args.hostname}")
    logger.info(f"  Tickrate: {args.tickrate}")
    logger.info(f"  Max Players: {args.maxplayers}")
    logger.info(f"  Starting Map: {args.map}")
    logger.info(f"  Port: {args.port}")
    logger.info(f"  Password: {'Yes' if args.password else 'No (Public)'}")
    logger.info(f"  RCON Password: {args.rcon_password}")
    logger.info("")
    logger.warning("=" * 60)
    logger.warning("IMPORTANT: HvH servers MUST run with -insecure flag!")
    logger.warning("This disables VAC to allow cheaters to play")
    logger.warning("=" * 60)
    logger.info("")
    logger.info("To start your HvH server:")
    logger.info("")
    logger.info(f"  cd {server_dir}")
    logger.info(f"  {launch_cmd}")
    logger.info("")
    logger.info("Additional Notes:")
    logger.info("  • Server has max money ($16000) enabled")
    logger.info("  • Tickrate 128 for optimal performance")
    logger.info("  • steam.inf set to Legacy version (2000258)")
    logger.info("  • You need a Game Server Token from:")
    logger.info("    https://steamcommunity.com/dev/managegameservers")
    logger.info("    Replace YOUR_GAME_SERVER_TOKEN in launch command")
    logger.info("")
    logger.info("Config file location:")
    logger.info(f"  {server_dir}/csgo/cfg/server.cfg")
    logger.info("")
    logger.success("Ready to host HvH! 🔥")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)

