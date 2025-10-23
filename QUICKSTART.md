# VileHvH - Quick Start Guide

Get your CS:GO Legacy server running in minutes!

## Prerequisites

- Python 3.8 or higher
- Internet connection
- Steam account
- ~25GB free disk space

## Installation (30 seconds)

### Linux (Arch/Ubuntu/etc.)
```bash
cd /home/vile/Documents/VileHvH-wip
python3 setup.py
```

### Windows
```cmd
cd C:\path\to\VileHvH-wip
python setup.py
```

## What the Script Does

1. ✓ Detects your OS and package managers
2. ✓ Installs SteamCMD (correct method for your platform)
3. ✓ Downloads CS:GO Legacy server (~20GB)
4. ✓ Installs Metamod:Source and SourceMod
5. ✓ Logs everything to `logs/` directory

## During Installation

### You'll be prompted for:
- **Installation directory** (press Enter for default)
- **Steam username**
- **First-time login?** (yes if first time on this machine)
- **Steam password** (if first time)
- **Steam Guard code** (if first time)

### ⚠️ IMPORTANT: First-Time Login
After entering your Steam Guard code successfully:
1. **Type `exit`** 
2. **Press Enter**

This caches your credentials. Next time you won't need your password!

## Command Examples

```bash
# Full installation (interactive)
python3 setup.py

# Custom directory
python3 setup.py --install-dir /opt/csgo-server

# Fast install (skip validation)
python3 setup.py --no-validate

# Add mods to existing server
python3 setup.py --skip-steamcmd --skip-csgo --install-dir /path/to/server

# Test your system first
python3 test_system_detect.py
```

## Installing Plugins

After server setup, you can install plugins easily:

```bash
# Install a plugin from a local directory
python3 install_plugins.py ~/csgo-server ./CSGO-Essentials-master

# Interactive mode
python3 install_plugins.py ~/csgo-server
```

The script handles plugins with this structure:
```
plugin-name/
└── addons/
    └── sourcemod/
        ├── plugins/*.smx
        └── scripting/*.sp
```

## After Installation

### Start Your Server

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

### Configure Server
```bash
# Edit server settings
nano ~/csgo-server/csgo/cfg/server.cfg

# Add yourself as admin
nano ~/csgo-server/csgo/addons/sourcemod/configs/admins_simple.ini
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "SteamCMD installation failed" | Install `base-devel git` (Arch) or check sudo access (Ubuntu) |
| "Steam login failed" | Verify credentials, check Steam Guard code |
| "Download stalled" | Check internet connection, try `--no-validate` |
| Permission errors | Run `chmod +x setup.py` (Linux) |
| Import errors | Make sure you're in the correct directory |

Check `logs/setup_*.log` for detailed error messages.

## Files Created

```
Your system:
├── steamcmd/              # SteamCMD installation
│   └── steamcmd.sh/.exe
│
└── csgo-server/           # Your CS:GO server
    ├── srcds_run / srcds.exe
    └── csgo/
        ├── cfg/           # Server configs
        └── addons/        # Metamod & SourceMod
            ├── metamod/
            └── sourcemod/
```

## Default Locations

| Platform | SteamCMD | CS:GO Server |
|----------|----------|--------------|
| **Arch Linux** | `/usr/bin/steamcmd` (system-wide) | `~/csgo-server` |
| **Ubuntu** | `/usr/games/steamcmd` | `~/csgo-server` |
| **Other Linux** | `~/steamcmd` | `~/csgo-server` |
| **Windows** | `C:\steamcmd` | `C:\csgo-server` |

## Need More Help?

- Read [USAGE.md](USAGE.md) for detailed guide
- Read [README.md](README.md) for full documentation
- Check log files in `logs/` directory
- Verify system detection: `python3 test_system_detect.py`

---

**Welcome back to CS:GO Legacy! The old servers are alive!** 🎮🔥

