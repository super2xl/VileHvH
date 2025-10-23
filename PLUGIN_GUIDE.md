# VileHvH - Plugin Installation Guide

Guide for installing and managing SourceMod plugins on your CS:GO Legacy server.

## Quick Start

```bash
# Install a plugin from local directory
python3 install_plugins.py ~/csgo-server ./CSGO-Essentials-master

# Interactive mode (prompts for plugin paths)
python3 install_plugins.py ~/csgo-server
```

## Understanding Plugin Structure

Most CS:GO SourceMod plugins follow this directory structure:

```
plugin-name/
├── addons/
│   └── sourcemod/
│       ├── plugins/
│       │   └── plugin_name.smx      # Compiled plugin (required)
│       ├── scripting/
│       │   └── plugin_name.sp       # Source code (optional)
│       ├── configs/
│       │   └── plugin_config.cfg    # Plugin config (if needed)
│       ├── gamedata/
│       │   └── plugin_data.txt      # Game data (if needed)
│       └── translations/
│           └── plugin.phrases.txt   # Language files (if needed)
├── LICENSE
└── README.md
```

### Example: CSGO-Essentials

```
CSGO-Essentials-master/
└── addons/
    └── sourcemod/
        ├── plugins/
        │   └── hvhgg_csgo_essentials.smx
        └── scripting/
            └── hvhgg_csgo_essentials.sp
```

## Plugin Installation Methods

### 1. From Local Directory

If you have a plugin folder on your system:

```bash
python3 install_plugins.py ~/csgo-server ./plugin-folder
```

The script will:
1. Verify the plugin has an `addons` folder
2. Copy all files to the correct server directories
3. Preserve the directory structure
4. List installed plugins

### 2. Interactive Mode

For installing multiple plugins:

```bash
python3 install_plugins.py ~/csgo-server
```

Then enter plugin paths when prompted. Type `quit` to exit.

### 3. Manual Installation (Advanced)

Using Python directly:

```python
from pathlib import Path
from plugin_manager import PluginManager

# Initialize
pm = PluginManager(Path("~/csgo-server"))

# Install from directory
pm.install_plugin_from_directory(Path("./plugin-folder"))

# Install from URL
pm.install_plugin_from_url(
    "https://example.com/plugin.zip",
    "plugin-name"
)

# List plugins
plugins = pm.list_installed_plugins()
print(plugins)

# Disable a plugin
pm.disable_plugin("plugin_name.smx")

# Enable a plugin
pm.enable_plugin("plugin_name.smx")

# Remove a plugin
pm.remove_plugin("plugin_name.smx")
```

## Plugin Management

### List Installed Plugins

The script automatically shows installed plugins:

```bash
python3 install_plugins.py ~/csgo-server
```

### Disable a Plugin

Plugins can be disabled by renaming:

```bash
cd ~/csgo-server/csgo/addons/sourcemod/plugins
mv plugin_name.smx plugin_name.smx.disabled
```

Or using Python:

```python
from plugin_manager import PluginManager
pm = PluginManager(Path("~/csgo-server"))
pm.disable_plugin("plugin_name.smx")
```

### Enable a Disabled Plugin

```python
pm.enable_plugin("plugin_name.smx")
```

### Remove a Plugin

```python
pm.remove_plugin("plugin_name.smx")
```

## Common Plugin Sources

### HvH-gg Plugins

Many great HvH plugins are available on HvH-gg's GitHub:
- [HvH-gg GitHub](https://github.com/HvH-gg)

### AlliedModders

Official SourceMod plugin repository:
- [AlliedModders Forums](https://forums.alliedmods.net/)

### Custom Plugins

You can place any custom `.smx` files directly in:
```
~/csgo-server/csgo/addons/sourcemod/plugins/
```

## Plugin Installation Flow

```
1. Download/Clone Plugin
   ├─ From GitHub
   ├─ From website
   └─ From friends

2. Verify Structure
   └─ Must have 'addons/sourcemod/plugins/*.smx'

3. Install Using Script
   └─ python3 install_plugins.py ~/csgo-server ./plugin-folder

4. Plugin Files Copied
   ├─ .smx files → plugins/
   ├─ .sp files → scripting/
   ├─ configs → configs/
   └─ gamedata → gamedata/

5. Server Loads Plugin
   └─ Restart server or use 'sm plugins load plugin_name'
```

## Troubleshooting

### "SourceMod is not installed"

Install SourceMod first:
```bash
python3 setup.py
```

### "Plugin directory missing 'addons' folder"

The plugin must have this structure:
```
plugin-name/addons/sourcemod/plugins/*.smx
```

Check the plugin's README for correct structure.

### Plugin Not Loading

1. Check if .smx file is in plugins folder:
   ```bash
   ls ~/csgo-server/csgo/addons/sourcemod/plugins/
   ```

2. Check server console for errors:
   ```
   sm plugins list
   sm plugins load plugin_name
   ```

3. Check SourceMod error logs:
   ```bash
   cat ~/csgo-server/csgo/addons/sourcemod/logs/errors_*.log
   ```

### Plugin Conflicts

Some plugins may conflict. Disable one at a time to test:
```python
pm.disable_plugin("conflicting_plugin.smx")
```

## Advanced: GitHub Integration (Future)

Future versions will support direct GitHub installation:

```python
# Coming soon!
pm.install_github_release("HvH-gg/plugin-name")
```

This requires GitHub API integration (see TODO.md).

## Plugin Development

Want to create your own plugins?

### Requirements
- SourceMod include files
- AMXModX compiler (`spcomp`)
- Text editor

### Resources
- [SourceMod Scripting](https://wiki.alliedmods.net/Introduction_to_SourcePawn)
- [SourceMod API](https://sm.alliedmods.net/new-api/)
- [CS:GO Scripting](https://wiki.alliedmods.net/Category:CS:GO)

### Workflow
1. Write `.sp` source file
2. Compile to `.smx` using `spcomp`
3. Test on dev server
4. Package with addons structure
5. Distribute!

## Recommended Plugins

### Essential Plugins

- **SourceMod Admin**: Built-in admin management
- **SourceBans**: Ban management system
- **MapChooser Extended**: Advanced map voting

### HvH Plugins

- **HvH Essentials**: Core HvH features (example: CSGO-Essentials)
- **Rank System**: Player ranking with colors
- **Anti-Cheat**: Detection and prevention
- **Stats Tracker**: Player statistics

### Fun Plugins

- **Custom Models**: Player/weapon models
- **Sound Effects**: Custom sounds
- **Chat Colors**: Colored chat messages

## Tips

1. **Backup First**: Always backup before installing plugins
2. **Test Locally**: Test plugins on a dev server first
3. **Read Docs**: Check plugin README for requirements
4. **Update Regularly**: Keep plugins updated
5. **Monitor Logs**: Watch error logs for issues

## Next Steps

- Check TODO.md for planned plugin features
- Explore HvH-gg GitHub for community plugins
- Set up automated plugin updates
- Create your own plugins!

---

**Happy plugging! Build the ultimate HvH server! 🔌🎮**

