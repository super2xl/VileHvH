# TODO List - Future Enhancements

## Completed ✓
- [x] Core logging system with colored output
- [x] OS and package manager detection
- [x] SteamCMD installation (Arch AUR, Ubuntu apt, Windows, generic Linux)
- [x] CS:GO Legacy server installation with proper force_install_dir handling
- [x] Steam Guard support for first-time login
- [x] Metamod:Source and SourceMod installation
- [x] Main orchestration script with CLI arguments
- [x] Comprehensive documentation (README, USAGE, QUICKSTART)

## High Priority 🔥

### Plugin Management
- [ ] GitHub API integration for plugin downloads
- [ ] HvH-gg plugin installation from GitHub
  - Research available plugins on HvH-gg's GitHub
  - Determine installation requirements for each
  - Create plugin profiles (dependencies, configs, etc.)
- [ ] Plugin dependency resolution
- [ ] Plugin configuration file management
- [ ] Automated plugin updates

### Server Configuration
- [ ] Server configuration templates
  - Competitive mode
  - HvH mode
  - Casual mode
- [ ] RCON configuration helper
- [ ] Network settings optimization
- [ ] Tickrate configuration

### Custom Ranks System
- [ ] Database setup (SQLite/MySQL)
  - Schema design
  - Migration scripts
  - Connection handling
- [ ] Rank plugin installation
- [ ] Custom rank colors configuration
- [ ] Rank progression system
- [ ] Rank statistics tracking

## Medium Priority 📋

### Installation Improvements
- [ ] Verify Metamod/SourceMod URLs are current
- [ ] Add retry logic for downloads
- [ ] Parallel download support
- [ ] Resume interrupted downloads
- [ ] Bandwidth throttling option
- [ ] Checksum verification for downloads

### Server Management
- [ ] Server startup script generation
- [ ] Server monitoring (is server running?)
- [ ] Auto-restart on crash
- [ ] Server update checker
- [ ] Backup and restore functionality
- [ ] Multiple server instance support

### Plugin System
- [ ] Plugin marketplace/repository
- [ ] Plugin version management
- [ ] Plugin conflict detection
- [ ] Plugin configuration wizard
- [ ] Plugin hot-reload support

### User Experience
- [ ] Interactive TUI (Text User Interface) using curses or rich
- [ ] Progress bars for downloads
- [ ] Better error messages with suggestions
- [ ] Automatic troubleshooting suggestions
- [ ] Setup wizard with step-by-step guide

## Low Priority 💡

### Documentation
- [ ] Video tutorial
- [ ] Common plugin configurations
- [ ] Server optimization guide
- [ ] HvH server best practices
- [ ] FAQ section
- [ ] Troubleshooting flowcharts

### Advanced Features
- [ ] Web-based control panel
- [ ] Discord bot integration for server management
- [ ] Automated backup to cloud storage
- [ ] Performance monitoring and metrics
- [ ] Player statistics dashboard
- [ ] Map workshop downloader
- [ ] Custom map management

### Platform Support
- [ ] macOS support (low priority per user preference)
- [ ] Docker container option
- [ ] More Linux distro testing
  - Fedora
  - CentOS
  - Gentoo
  - OpenSUSE

### Testing
- [ ] Unit tests for core modules
- [ ] Integration tests for full workflow
- [ ] Test on different platforms
- [ ] Mock SteamCMD for testing
- [ ] CI/CD pipeline

## Research Needed 🔍

### HvH-gg Plugins
- [ ] Research available plugins on HvH-gg GitHub
- [ ] Document installation procedures for each plugin
- [ ] Check for dependencies between plugins
- [ ] Verify compatibility with latest CS:GO Legacy
- [ ] Test plugin combinations

### Database Systems
- [ ] Research best DB for rank system
  - SQLite (simple, no server needed)
  - MySQL (more powerful, needs server)
  - PostgreSQL (alternative to MySQL)
- [ ] Connection pooling
- [ ] ORM vs raw SQL

### Performance
- [ ] SteamCMD performance optimization
- [ ] Download speed optimization
- [ ] Server startup time optimization
- [ ] Memory usage optimization

## Known Issues 🐛

### To Investigate
- [ ] Test first-time Steam login flow thoroughly
- [ ] Verify force_install_dir behavior on all platforms
- [ ] Check if multiverse repo command works on all Ubuntu versions
- [ ] Test AUR installation on different Arch variants
- [ ] Verify Windows paths handle spaces correctly

### To Fix
- [ ] Add better error handling for network timeouts
- [ ] Handle partial downloads gracefully
- [ ] Improve permission error messages on Linux
- [ ] Handle disk space checks before downloads

## User Feedback Needed 💬

- [ ] Test on Arch Linux system
- [ ] Test on Ubuntu system
- [ ] Test on Windows system
- [ ] Verify Metamod/SourceMod URLs are current
- [ ] Confirm HvH-gg plugin requirements
- [ ] Database preferences for rank system
- [ ] Desired plugin features

## Notes

### Architecture Decisions
- **Python Standard Library Only**: Keep dependencies minimal for easier deployment
- **Modular Design**: Each component is self-contained and reusable
- **Cross-Platform**: Support Windows and Linux equally (macOS later if needed)
- **Logging First**: Everything important should be logged

### Plugin Management Considerations
- Plugins can have complex dependencies
- Some plugins need gamedata files
- Some plugins need config files
- Version compatibility is crucial
- Need to handle both .smx and .sp files

### Database for Ranks
- Need to decide: SQLite (easier) vs MySQL (more powerful)
- Consider using an ORM for easier database operations
- Need migration system for schema updates
- Consider connection pooling for performance

### Future Architecture
- Consider adding a web UI using Flask or FastAPI
- Could use React/Vue for frontend
- Could add REST API for remote management
- Could add WebSocket for real-time server monitoring

---

**Last Updated**: October 23, 2025  
**Status**: Core functionality complete, ready for expansion

