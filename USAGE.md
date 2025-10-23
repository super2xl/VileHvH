# Usage Guide

Detailed usage guide for the CS:GO Legacy Server Setup Scripts.

## Table of Contents
- [Quick Start](#quick-start)
- [Step-by-Step Guide](#step-by-step-guide)
- [Command-Line Options](#command-line-options)
- [Common Scenarios](#common-scenarios)
- [Troubleshooting](#troubleshooting)

## Quick Start

The simplest way to get started:

```bash
# Test your system detection first (optional but recommended)
python3 test_system_detect.py

# Run the full setup
python3 setup.py
```

Follow the interactive prompts. You'll need:
- Your Steam username and password
- Steam Guard code (first login only)

## Step-by-Step Guide

### 1. Test System Detection (Optional)

Before running the full setup, verify your system is detected correctly:

```bash
python3 test_system_detect.py
```

This will show:
- Your OS and distribution
- Detected package managers
- Common package availability

### 2. Run the Setup Script

```bash
python3 setup.py
```

The script will guide you through:

#### Phase 1: System Detection
- Automatically detects your OS, distro, and package managers
- Shows what was detected
- No user input required

#### Phase 2: SteamCMD Installation
- Downloads and installs SteamCMD using the recommended method for your platform
- **Arch Linux**: Uses AUR (yay/paru) or manual makepkg
- **Ubuntu/Debian**: Enables multiverse and i386 support, installs via apt
- **Windows**: Downloads to C:\steamcmd
- **Other Linux**: Downloads tarball and extracts

#### Phase 3: Server Installation Path
You'll be asked:
```
Using default installation directory: /home/user/csgo-server
Would you like to use a custom directory? [y/N]:
```

- Press Enter for default
- Type `y` to specify a custom path

#### Phase 4: Steam Login
You'll need to provide:
```
Steam username: your_username
Is this your first time logging in on this machine? [Y/n]:
```

**First-time login:**
- Enter your password
- Wait for Steam Guard prompt
- Enter your Steam Guard code
- **IMPORTANT**: Type `exit` and press Enter after successful login
- This caches your credentials

**Subsequent logins:**
- No password needed
- Credentials are cached from first login

#### Phase 5: CS:GO Download
- Downloads CS:GO server files (app_update 740)
- Shows progress
- Validates files (can be disabled with --no-validate)
- Takes 10-30 minutes depending on connection

#### Phase 6: Metamod & SourceMod
- Automatically downloads and installs Metamod:Source
- Automatically downloads and installs SourceMod
- Verifies installation

## Command-Line Options

### Installation Directory

```bash
# Specify custom directory
python3 setup.py --install-dir /opt/csgo-server

# Windows example
python setup.py --install-dir D:\GameServers\csgo
```

### Skip Steps

```bash
# Skip SteamCMD installation (if already installed)
python3 setup.py --skip-steamcmd

# Skip CS:GO installation (only install mods on existing server)
python3 setup.py --skip-csgo --install-dir /path/to/existing/server

# Skip mod installation (only install CS:GO server)
python3 setup.py --skip-mods

# Combine flags
python3 setup.py --skip-steamcmd --skip-mods
```

### Validation

```bash
# Default: validate files (slower but safer)
python3 setup.py

# Skip validation (faster)
python3 setup.py --no-validate

# Explicitly enable validation
python3 setup.py --validate
```

## Common Scenarios

### Scenario 1: Fresh Installation (Everything)
```bash
python3 setup.py
```
- Installs SteamCMD
- Installs CS:GO server
- Installs Metamod & SourceMod
- Interactive prompts for Steam login

### Scenario 2: Custom Directory
```bash
python3 setup.py --install-dir /opt/csgo-hvh
```
- Same as fresh install but uses custom path

### Scenario 3: Add Mods to Existing Server
```bash
python3 setup.py --skip-steamcmd --skip-csgo --install-dir /path/to/server
```
- Only installs Metamod & SourceMod
- Use if you already have CS:GO installed

### Scenario 4: Update Existing Server
```bash
python3 setup.py --skip-steamcmd --skip-mods --install-dir /path/to/server
```
- Updates CS:GO server files
- Validates installation
- Does not reinstall mods

### Scenario 5: Quick Install (No Validation)
```bash
python3 setup.py --no-validate
```
- Faster installation
- Skips file validation
- Use if you trust your connection

### Scenario 6: Test System Only
```bash
python3 test_system_detect.py
```
- Only tests system detection
- No installation
- Safe to run anytime

## Platform-Specific Tips

### Arch Linux

The script will try to use your AUR helper:
1. First tries `yay` if available
2. Then tries `paru` if available
3. Falls back to manual `git clone` + `makepkg -si`

Make sure you have:
```bash
sudo pacman -S base-devel git
```

### Ubuntu/Debian

The script automatically:
- Enables multiverse repository (Ubuntu)
- Enables i386 architecture
- Installs required dependencies

You need sudo privileges.

### Windows

- Script must be run with permissions to create C:\steamcmd
- Default install: C:\csgo-server
- No special requirements beyond Python 3.8+

### Fedora/CentOS/Other Linux

Uses generic Linux installation method:
- Downloads SteamCMD tarball
- Extracts to ~/steamcmd
- Should work on most modern Linux distros

## Logs

Every run creates a log file:
```
logs/setup_YYYYMMDD_HHMMSS.log
```

Check logs for:
- Detailed error messages
- Download progress
- Debug information
- Troubleshooting

## After Installation

### Configure Server
Edit your server.cfg:
```bash
nano ~/csgo-server/csgo/cfg/server.cfg
```

Key settings:
- `hostname "Your Server Name"`
- `rcon_password "your_rcon_pass"`
- `sv_password "server_password"`

### Add SourceMod Admins
Edit admins_simple.ini:
```bash
nano ~/csgo-server/csgo/addons/sourcemod/configs/admins_simple.ini
```

Add your Steam ID:
```
"STEAM_1:0:12345678" "z" // Your Name
```

### Start Server

**Linux:**
```bash
cd ~/csgo-server
./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2
```

**Windows:**
```cmd
cd C:\csgo-server
srcds.exe -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2
```

## Troubleshooting

### "SteamCMD installation failed"
- **Arch**: Install base-devel and git
- **Ubuntu**: Ensure sudo privileges
- **Windows**: Check write permissions to C:\

### "Steam login failed"
- Verify username and password
- Check Steam Guard code
- Remember to type `exit` after first login
- Check logs/setup_*.log for details

### "CS:GO download stalled"
- Check internet connection
- Try --no-validate flag
- Check disk space (need ~25GB)
- Check logs for specific errors

### "Metamod/SourceMod download failed"
- URLs in script may be outdated
- Check [metamodsource.net](https://www.metamodsource.net/) for latest
- Check [sourcemod.net](https://www.sourcemod.net/) for latest
- Manually update URLs in metamod_sourcemod_installer.py

### Permission Errors (Linux)
```bash
# Make scripts executable
chmod +x setup.py test_system_detect.py

# If SteamCMD needs permissions
chmod +x ~/steamcmd/steamcmd.sh
```

### Module Import Errors
Ensure you're in the correct directory:
```bash
cd /path/to/VileHvH-wip
python3 setup.py
```

All Python files must be in the same directory.

## Getting Help

1. Check the log files in `logs/`
2. Read error messages carefully
3. Try the test script: `python3 test_system_detect.py`
4. Check if your OS/distro is supported
5. Verify Python version: `python3 --version` (need 3.8+)

---

**Happy CS:GO Legacy server hosting!** 🎮

