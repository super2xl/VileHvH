#!/usr/bin/env python3
"""
Server configuration module for CS:GO Legacy HvH servers
Handles server.cfg generation and steam.inf modification
"""

import shutil
from pathlib import Path
from typing import Optional
from logger import get_logger


class ServerConfigurator:
    """Manages CS:GO server configuration for HvH"""
    
    # CS:GO Legacy version for HvH (pre-CS2)
    CSGO_LEGACY_VERSION = "2000258"
    
    def __init__(self, csgo_install_dir: Path):
        self.csgo_install_dir = csgo_install_dir
        self.logger = get_logger()
        
        self.csgo_dir = csgo_install_dir / "csgo"
        self.cfg_dir = self.csgo_dir / "cfg"
        self.steam_inf = self.csgo_dir / "steam.inf"
    
    def create_hvh_config(self, 
                          hostname: str = "VileHvH Server",
                          rcon_password: str = "change_me",
                          sv_password: str = "",
                          tickrate: int = 128) -> bool:
        """
        Create optimized HvH server configuration
        
        Args:
            hostname: Server name
            rcon_password: RCON password
            sv_password: Server password (empty = public)
            tickrate: Server tickrate (64 or 128)
        
        Returns:
            True if successful
        """
        self.logger.section("Creating HvH Server Configuration")
        
        # Ensure cfg directory exists
        self.cfg_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate server.cfg
        config = self._generate_hvh_config(hostname, rcon_password, sv_password, tickrate)
        
        server_cfg = self.cfg_dir / "server.cfg"
        
        try:
            # Backup existing config if present
            if server_cfg.exists():
                backup = self.cfg_dir / "server.cfg.backup"
                shutil.copy(server_cfg, backup)
                self.logger.info(f"Backed up existing config to: {backup}")
            
            # Write new config
            with open(server_cfg, 'w') as f:
                f.write(config)
            
            self.logger.success(f"HvH config created: {server_cfg}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to create config: {e}")
            return False
    
    def _generate_hvh_config(self, hostname: str, rcon_password: str, 
                            sv_password: str, tickrate: int) -> str:
        """Generate HvH-optimized server.cfg content"""
        
        return f"""// VileHvH CS:GO Legacy Server Configuration
// Optimized for Hack vs Hack gameplay
// Generated automatically - edit as needed

// ============================================================
// SERVER IDENTITY
// ============================================================
hostname "{hostname}"
sv_password "{sv_password}"
rcon_password "{rcon_password}"

// ============================================================
// HvH SETTINGS (IMPORTANT!)
// ============================================================
// Server runs in -insecure mode (VAC disabled)
// This is required for HvH gameplay
sv_lan 0
sv_cheats 0              // Keep off even in insecure mode
sv_pure 1                // Prevent client-side file modifications

// ============================================================
// GAME MODE & RULES (DEATHMATCH FOR HvH)
// ============================================================
game_type 1              // Gun Game (required for DM)
game_mode 2              // Deathmatch
mp_dm_bonus_percent 0    // No bonus weapons

// Deathmatch Settings
mp_respawn_on_death_ct 1 // Instant respawn CT
mp_respawn_on_death_t 1  // Instant respawn T
mp_respawn_immunitytime 0  // No spawn protection
mp_dm_time_between_bonus_min 99999  // No bonus time
mp_dm_time_between_bonus_max 99999

// Round Settings
mp_roundtime 60          // Long rounds for DM
mp_timelimit 0           // No time limit
mp_maxrounds 0           // Continuous play
mp_round_restart_delay 5

// Buy Settings (Buy anytime, anywhere)
mp_buytime 9999          // Always able to buy
mp_buy_anywhere 1        // Buy anywhere on map
mp_buy_during_immunity 0
mp_death_drop_gun 0      // Don't drop guns on death

// ============================================================
// MONEY SETTINGS (HvH = MAX MONEY)
// ============================================================
mp_startmoney 16000      // Start with max money
mp_maxmoney 16000        // Max money cap
mp_afterroundmoney 16000 // Max money after round
cash_team_terrorist_win_bomb 0
cash_team_elimination_bomb_map 0
cash_team_win_by_defusing_bomb 0
cash_team_win_by_time_running_out_bomb 0
cash_player_killed_enemy_default 0
cash_player_bomb_planted 0
cash_player_bomb_defused 0

// ============================================================
// TICKRATE & NETWORK SETTINGS
// ============================================================
// Server tickrate: {tickrate} (set via launch options)
sv_minrate 128000
sv_maxrate 0             // Unlimited
sv_minupdaterate {tickrate}
sv_maxupdaterate {tickrate}
sv_mincmdrate {tickrate}
sv_maxcmdrate {tickrate}
fps_max 0                // Unlimited server FPS

// Network Optimization
sv_client_min_interp_ratio 1
sv_client_max_interp_ratio 1
net_maxcleartime 0.001

// ============================================================
// PERFORMANCE & OPTIMIZATION
// ============================================================
host_workshop_collection 0
host_threaded_sound 0
sv_parallel_sendsnapshot 1
sv_parallel_packentities 1

// Stability
sv_clockcorrection_msecs 15
sv_timeout 60
sv_forcepreload 1

// ============================================================
// MOVEMENT & GAMEPLAY
// ============================================================
// Default CS:GO movement (cheats handle movement)
// Don't modify these - let the cheats do their thing
sv_accelerate 5.5        // Default
sv_airaccelerate 12      // Default  
sv_friction 5.2          // Default
sv_stopspeed 80          // Default

// ============================================================
// WEAPON & DAMAGE SETTINGS
// ============================================================
mp_damage_headshot_only 0
mp_friendlyfire 0        // Friendly fire OFF (will add utility plugin later)
mp_autokick 0            // Don't auto-kick
mp_tkpunish 0            // No punishment

// Weapon restrictions (none for HvH)
mp_weapons_allow_zeus 1
mp_weapons_allow_typecount -1
mp_weapons_allow_map_placed 1

// Deathmatch weapon settings
mp_weapons_glow_on_ground 0
mp_display_kill_assists 1
mp_dm_bonus_length_min 0
mp_dm_bonus_length_max 0

// ============================================================
// BOT SETTINGS
// ============================================================
bot_quota 0              // No bots
bot_quota_mode "normal"
bot_join_after_player 0
bot_chatter "off"

// ============================================================
// SPECTATOR SETTINGS
// ============================================================
mp_forcecamera 0         // Free spectate
mp_allowspectators 1
tv_enable 0              // GOTV disabled (enable if needed)

// ============================================================
// MAP & VOTING
// ============================================================
mp_endmatch_votenextmap 1
mp_endmatch_votenextleveltime 20

// ============================================================
// LOGGING
// ============================================================
log on
sv_logfile 1
sv_log_onefile 0
sv_logbans 1
sv_logecho 0
sv_logflush 0

// ============================================================
// MISC SETTINGS
// ============================================================
sv_alltalk 0             // Team-only voice
sv_deadtalk 1            // Dead can talk to living
sv_full_alltalk 0
sv_pausable 0            // Can't pause
sv_allow_votes 1         // Allow voting
sv_vote_allow_spectators 0

// Player settings
mp_join_grace_time 30
mp_playerid 0
mp_playerid_delay 0.5
mp_playerid_hold 0.25

// Molotov settings
molotov_throw_detonate_time 2.0
inferno_max_flames 16

// Grenade trajectory
sv_grenade_trajectory 0
sv_showimpacts 0

// ============================================================
// EXECUTION
// ============================================================
exec banned_user.cfg
exec banned_ip.cfg

echo ""
echo "============================================================"
echo "  VileHvH Server Configuration Loaded"
echo "  Mode: Deathmatch | Tickrate: {tickrate}"
echo "  Max Money: $16000 | Buy Anytime/Anywhere"
echo "  Instant Respawn | Friendly Fire: OFF"
echo "  HvH Mode: Enabled (-insecure required)"
echo "============================================================"
echo ""
"""
    
    def set_legacy_version(self) -> bool:
        """
        Set CS:GO Legacy version in steam.inf
        This locks the server to pre-CS2 version
        
        Modifies TWO critical values:
        1. ClientVersion - Client game version
        2. ServerVersion - Server game version
        Both must be set to 2000258 for CS:GO Legacy
        
        Returns:
            True if successful
        """
        self.logger.info("Setting CS:GO Legacy version in steam.inf")
        
        if not self.steam_inf.exists():
            self.logger.error(f"steam.inf not found: {self.steam_inf}")
            return False
        
        try:
            # Read current steam.inf
            with open(self.steam_inf, 'r') as f:
                lines = f.readlines()
            
            # Backup
            backup = self.steam_inf.parent / "steam.inf.backup"
            shutil.copy(self.steam_inf, backup)
            self.logger.debug(f"Backed up steam.inf to: {backup}")
            
            # Track modifications
            client_version_modified = False
            server_version_modified = False
            
            # Modify both ClientVersion and ServerVersion
            for i, line in enumerate(lines):
                # Modify ClientVersion
                if line.startswith('ClientVersion='):
                    old_version = line.strip().split('=')[1]
                    lines[i] = f'ClientVersion={self.CSGO_LEGACY_VERSION}\n'
                    client_version_modified = True
                    self.logger.info(f"Changed ClientVersion: {old_version} → {self.CSGO_LEGACY_VERSION}")
                
                # Modify ServerVersion
                elif line.startswith('ServerVersion='):
                    old_version = line.strip().split('=')[1]
                    lines[i] = f'ServerVersion={self.CSGO_LEGACY_VERSION}\n'
                    server_version_modified = True
                    self.logger.info(f"Changed ServerVersion: {old_version} → {self.CSGO_LEGACY_VERSION}")
            
            # Add missing lines if needed
            if not client_version_modified:
                self.logger.warning("ClientVersion not found, appending...")
                lines.append(f'ClientVersion={self.CSGO_LEGACY_VERSION}\n')
            
            if not server_version_modified:
                self.logger.warning("ServerVersion not found, appending...")
                lines.append(f'ServerVersion={self.CSGO_LEGACY_VERSION}\n')
            
            # Write modified steam.inf
            with open(self.steam_inf, 'w') as f:
                f.writelines(lines)
            
            self.logger.success(f"steam.inf configured for CS:GO Legacy")
            self.logger.info(f"  ClientVersion: {self.CSGO_LEGACY_VERSION}")
            self.logger.info(f"  ServerVersion: {self.CSGO_LEGACY_VERSION}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to modify steam.inf: {e}")
            return False
    
    def get_hvh_launch_command(self, 
                              map_name: str = "de_mirage",
                              tickrate: int = 128,
                              maxplayers: int = 10,
                              port: int = 27015,
                              gslt: str = "") -> str:
        """
        Generate HvH server launch command
        
        Args:
            map_name: Starting map (default: de_mirage)
            tickrate: Server tickrate
            maxplayers: Max players
            port: Server port
            gslt: Game Server Login Token (GSLT)
        
        Returns:
            Launch command string
        """
        if self.csgo_install_dir.exists():
            server_exe = self.csgo_install_dir / "srcds_run"
            if not server_exe.exists():
                server_exe = self.csgo_install_dir / "srcds.exe"
        else:
            server_exe = Path("./srcds_run")
        
        # HvH MUST use -insecure flag to disable VAC
        cmd = (
            f"{server_exe} "
            f"-game csgo "
            f"-console "
            f"-usercon "
            f"-insecure "  # CRITICAL for HvH!
            f"-tickrate {tickrate} "
            f"-port {port} "
            f"-maxplayers_override {maxplayers} "
            f"+game_type 1 "  # Gun Game (for DM)
            f"+game_mode 2 "  # Deathmatch
            f"+map {map_name}"
        )
        
        # Add GSLT if provided
        if gslt:
            cmd += f" +sv_setsteamaccount {gslt}"
        
        return cmd
    
    def save_gslt(self, gslt: str) -> bool:
        """
        Save GSLT to a file for easy reference
        
        Args:
            gslt: Game Server Login Token
        
        Returns:
            True if successful
        """
        try:
            gslt_file = self.csgo_dir / "gslt.txt"
            with open(gslt_file, 'w') as f:
                f.write(gslt)
            self.logger.success(f"GSLT saved to: {gslt_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save GSLT: {e}")
            return False


# Example usage
if __name__ == "__main__":
    from pathlib import Path
    
    # Example: Configure HvH server
    server_path = Path.home() / "csgo-server"
    
    if server_path.exists():
        configurator = ServerConfigurator(server_path)
        
        # Create HvH config
        configurator.create_hvh_config(
            hostname="VileHvH Test Server",
            rcon_password="secure_rcon_123",
            sv_password="",  # Public
            tickrate=128
        )
        
        # Set legacy version
        configurator.set_legacy_version()
        
        # Get launch command
        launch_cmd = configurator.get_hvh_launch_command(
            map_name="de_mirage",
            tickrate=128
        )
        print("\nLaunch command:")
        print(launch_cmd)
    else:
        print(f"Server not found at {server_path}")

