# VileHvH - CS:GO Legacy Server Setup Scripts

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗   ██╗██╗██╗     ███████╗    ██╗  ██╗██╗   ██╗██╗  ██╗                 ║
║  ██║   ██║██║██║     ██╔════╝    ██║  ██║██║   ██║██║  ██║                 ║
║  ██║   ██║██║██║     █████╗      ███████║██║   ██║███████║                 ║
║  ██║   ██║██║██║     ██╔══╝      ██╔══██║╚██╗ ██╔╝██╔══██║                 ║
║  ╚██████╔╝██║███████╗███████╗    ██║  ██║ ╚████╔╝ ██║  ██║                 ║
║   ╚═════╝ ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝                 ║
║                                                                              ║
║              CS:GO Legacy Server Setup & Management Scripts                  ║
║                Automated Installation for Windows & Linux                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

Automated installation and configuration scripts for CS:GO Legacy (pre-CS2) servers on Linux and Windows.

## Features

- **Cross-Platform Support**: Windows and Linux (Arch, Ubuntu/Debian, Fedora)
- **Intelligent OS Detection**: Automatically detects your OS, distribution, and package managers
- **Automated SteamCMD Installation**: Uses the recommended installation method for each platform
  - Arch Linux: AUR package via yay/paru or manual `makepkg -si`
  - Ubuntu/Debian: Enables multiverse repo and i386 architecture
  - Windows: Downloads to `C:\steamcmd`
- **Proper CS:GO Installation**: Handles `force_install_dir` correctly (before login)
- **Steam Guard Support**: Interactive first-login with cached credentials for subsequent runs
- **Metamod:Source & SourceMod**: Automated installation of essential server mods
- **Comprehensive Logging**: Colored console output + detailed log files

## Requirements

- **Python 3.8+**
- **Operating System**: Windows 10/11 or Linux (tested on Arch, Ubuntu)
- **Steam Account**: Required for downloading CS:GO server files
- **Disk Space**: ~25GB for CS:GO server files
- **Internet Connection**: Required for downloading

### Linux Additional Requirements
- `git` (for AUR installation on Arch)
- `base-devel` (Arch) or `build-essential` (Ubuntu) for building packages
- `sudo` privileges for package installation

## Installation

1. **Clone or download this repository**:
   ```bash
   git clone <your-repo-url>
   cd VileHvH-wip
   ```

2. **Ensure Python 3.8+ is installed**:
   ```bash
   python3 --version
   ```

3. **No external dependencies needed!** (Uses Python standard library only)

## Usage

### Quick Start (Interactive Mode)

```bash
python3 setup.py
```

This will guide you through:
1. System detection
2. SteamCMD installation
3. CS:GO server installation (with Steam login)
4. Metamod:Source and SourceMod installation

### Custom Installation Directory

```bash
python3 setup.py --install-dir /opt/csgo-server
```

### Skip Specific Steps

```bash
# Skip SteamCMD installation (if already installed)
python3 setup.py --skip-steamcmd

# Skip CS:GO installation (only install mods)
python3 setup.py --skip-csgo

# Skip mod installation
python3 setup.py --skip-mods
```

### Disable File Validation

```bash
# Skip validation to speed up installation
python3 setup.py --no-validate
```

## First-Time Steam Login

On your first run, you'll need to:
1. Enter your Steam username and password
2. Enter your Steam Guard code when prompted
3. **Type `exit` and press Enter** after successful authentication
4. Subsequent runs will use cached credentials (no password needed)

## Project Structure

```
VileHvH-wip/
├── setup.py                          # Main orchestration script
├── logger.py                         # Logging system (colored output + files)
├── system_detect.py                  # OS/distro/package manager detection
├── steamcmd_installer.py             # SteamCMD installation per platform
├── csgo_installer.py                 # CS:GO server installation & management
├── metamod_sourcemod_installer.py    # Metamod & SourceMod installation
├── requirements.txt                  # Python dependencies (none required)
├── README.md                         # This file
└── logs/                             # Log files (created automatically)
    └── setup_YYYYMMDD_HHMMSS.log
```

## Platform-Specific Notes

### Arch Linux
- Installs SteamCMD from AUR using `yay` or `paru` if available
- Falls back to manual `git clone` + `makepkg -si` if no AUR helper found
- SteamCMD installed system-wide to `/usr/bin/steamcmd`

### Ubuntu/Debian
- Automatically enables `multiverse` repository (Ubuntu)
- Enables `i386` architecture for 32-bit support
- Installs via `apt install steamcmd`

### Windows
- Downloads SteamCMD to `C:\steamcmd`
- No Steam user permission management needed (simpler than Linux)
- Default CS:GO install: `C:\csgo-server`

### Linux (Generic/Other Distros)
- Downloads SteamCMD tarball directly
- Extracts to `~/steamcmd`
- Works on Fedora, CentOS, and other distros

## Starting Your Server

### Windows
```cmd
cd C:\csgo-server
srcds.exe -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2
```

### Linux
```bash
cd ~/csgo-server
./srcds_run -game csgo -console -usercon +game_type 0 +game_mode 1 +mapgroup mg_active +map de_dust2
```

## Configuration

### Server Configuration
Edit `csgo-server/csgo/cfg/server.cfg` for your server settings:
- Hostname, password, rcon password
- Tickrate, rates, cvars
- Game modes and settings

### SourceMod Admins
Add admins to `csgo-server/csgo/addons/sourcemod/configs/admins_simple.ini`:
```
"STEAM_1:0:12345678" "z" // Admin Name
```

## Troubleshooting

### SteamCMD Installation Fails
- **Arch**: Ensure `base-devel` and `git` are installed
- **Ubuntu**: Check that you have sudo privileges
- **Windows**: Ensure you have write permissions to `C:\`

### Steam Login Fails
- Verify your username and password are correct
- Make sure you have Steam Guard enabled
- Check your internet connection
- For first login, ensure you type `exit` after entering Steam Guard code

### CS:GO Download Stalls
- Check your internet connection
- Try running with `--no-validate` first, then validate later
- Ensure you have enough disk space (~25GB)

### Metamod/SourceMod Download Fails
- The download URLs may be outdated
- Check [Metamod:Source](https://www.metamodsource.net/) for latest builds
- Check [SourceMod](https://www.sourcemod.net/) for latest builds
- Update URLs in `metamod_sourcemod_installer.py`

## Logs

All operations are logged to:
- **Console**: Colored output with INFO level and above
- **Log File**: `logs/setup_YYYYMMDD_HHMMSS.log` with DEBUG level

Check log files for detailed troubleshooting information.

## Future Features

- [ ] HvH-gg plugin installation from GitHub
- [ ] Custom ranks with colors
- [ ] Database setup for rank storage
- [ ] Server configuration templates
- [ ] Automated plugin management
- [ ] Update checker for installed components

## Contributing

Feel free to submit issues or pull requests. This is an active development project for CS:GO Legacy HvH servers.

## License

This project is provided as-is for the CS:GO community. Use at your own discretion.

## Credits

- Built for CS:GO Legacy server enthusiasts
- Supports the CS:GO Legacy community as official servers see more action than CS2 HvH

---

**Welcome to new beginnings!** 🎮

*CS:GO Legacy is back - Legacy servers > CS2 for HvH any day! 💯*

