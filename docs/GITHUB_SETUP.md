# Pushing VileHvH to GitHub - Complete Guide

Quick guide to create a new GitHub repo and push VileHvH from the command line.

## Step 1: Create Personal Access Token (PAT)

GitHub requires a PAT instead of password for command-line operations.

### Generate PAT

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `VileHvH-CLI` or `Git-CLI-Access`
4. Set expiration: Choose what you prefer (or "No expiration")
5. Select scopes (permissions):
   - ✅ **repo** (all sub-options) - Required for pushing
   - That's it! (Don't need anything else for basic push/pull)
6. Click **"Generate token"**
7. **COPY THE TOKEN NOW** (you won't see it again!)
   - Save it somewhere safe (password manager, text file, etc.)

### Example Token
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 2: Create GitHub Repo (Web Method)

Quick method - create repo on GitHub website:

1. Go to: https://github.com/new
2. Repository name: `VileHvH` (or whatever you want)
3. Description: `CS:GO Legacy Server Setup & Management Scripts`
4. Visibility: **Public** or **Private** (your choice)
5. **DON'T** initialize with README (we have one already)
6. Click **"Create repository"**

GitHub will show you the quick setup page - ignore it, we'll do it from CLI.

## Step 3: Create GitHub Repo (CLI Method)

Or create it entirely from command line using GitHub CLI:

### Install GitHub CLI (if not installed)

**Arch Linux:**
```bash
sudo pacman -S github-cli
```

**Other systems:** https://cli.github.com/

### Login and Create Repo
```bash
# Login (one-time setup)
gh auth login
# Follow prompts, paste your PAT when asked

# Create repo from current directory
cd /home/vile/Documents/VileHvH-wip
gh repo create VileHvH --public --source=. --remote=origin --push
```

This creates the repo and pushes in one command! 🚀

## Step 4: Push Using Git (Traditional Method)

If you created repo via web or want to do it manually:

```bash
cd /home/vile/Documents/VileHvH-wip

# Initialize git (if not already)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - VileHvH CS:GO Legacy Server Setup"

# Rename branch to main (if needed)
git branch -M main

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/VileHvH.git

# Push to GitHub
git push -u origin main
```

### When Prompted for Credentials:
- **Username:** Your GitHub username
- **Password:** **PASTE YOUR PAT HERE** (not your GitHub password!)

## Step 5: Save PAT in Git Config (Optional)

To avoid entering PAT every time:

### Option A: Git Credential Helper (Recommended)
```bash
# Cache credentials for 1 hour
git config --global credential.helper 'cache --timeout=3600'

# Or store permanently (less secure)
git config --global credential.helper store
```

After this, enter PAT once and it's remembered.

### Option B: Use SSH Keys (More Secure)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/keys
# Then use SSH URL instead:
git remote set-url origin git@github.com:USERNAME/VileHvH.git
```

## Quick Reference Commands

### Create Repo + Push (GitHub CLI - Easiest!)
```bash
cd /home/vile/Documents/VileHvH-wip
gh auth login
gh repo create VileHvH --public --source=. --remote=origin --push
```

### Create Repo + Push (Traditional Git)
```bash
cd /home/vile/Documents/VileHvH-wip
git init
git add .
git commit -m "Initial commit - VileHvH CS:GO Legacy Server Setup"
git branch -M main
git remote add origin https://github.com/USERNAME/VileHvH.git
git push -u origin main
# Enter username and PAT when prompted
```

### Update Existing Repo
```bash
git add .
git commit -m "Update: description of changes"
git push
```

## Full Example Workflow

```bash
# 1. Navigate to project
cd /home/vile/Documents/VileHvH-wip

# 2. Initialize git
git init

# 3. Check status
git status

# 4. Add all files
git add .

# 5. Verify what will be committed
git status

# 6. Create first commit
git commit -m "Initial commit - VileHvH

- Complete CS:GO Legacy server setup scripts
- Cross-platform support (Windows + Linux)
- Automated SteamCMD, CS:GO, Metamod, SourceMod installation
- Plugin management system
- Comprehensive documentation"

# 7. Rename branch to main
git branch -M main

# 8. Add remote (replace USERNAME!)
git remote add origin https://github.com/USERNAME/VileHvH.git

# 9. Push to GitHub
git push -u origin main
# When prompted:
#   Username: your-github-username
#   Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (your PAT)

# 10. Done! 🎉
```

## Troubleshooting

### "remote: Support for password authentication was removed"
**Solution:** Use your PAT (starts with `ghp_`), not your GitHub password

### "Permission denied (publickey)"
**Solution:** Using SSH but key not added to GitHub
- Generate SSH key: `ssh-keygen -t ed25519 -C "email@example.com"`
- Add to GitHub: https://github.com/settings/keys

### "failed to push some refs"
**Solution:** Remote has changes you don't have locally
```bash
git pull origin main --rebase
git push origin main
```

### "fatal: not a git repository"
**Solution:** Not in project directory or not initialized
```bash
cd /home/vile/Documents/VileHvH-wip
git init
```

### Token Permission Issues
**Solution:** Regenerate token with correct scopes:
- Need **repo** scope for private repos
- Need **public_repo** scope for public repos

## Recommended: GitHub CLI Method

The GitHub CLI (`gh`) is the easiest method:

```bash
# Install
sudo pacman -S github-cli

# Login once
gh auth login
# Choose: GitHub.com → HTTPS → Paste PAT → Done

# Create and push repo
cd /home/vile/Documents/VileHvH-wip
gh repo create VileHvH --public --source=. --remote=origin --push

# That's it! Repo created and pushed!
```

## Adding a README Badge

After pushing, add badges to your README:

```markdown
# VileHvH

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

## .gitignore Already Configured

Your `.gitignore` already excludes:
- `__pycache__/`
- `*.pyc`
- `logs/`
- `steamcmd/`
- `csgo-server/`
- `CSGO-Essentials-master/`
- Credentials files

So you're good to go! ✅

## Common Git Commands

```bash
# Check status
git status

# Add specific files
git add file1.py file2.md

# Add all changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# View remote URL
git remote -v

# Change remote URL
git remote set-url origin https://github.com/USERNAME/VileHvH.git
```

## Next Steps After Pushing

1. **Add Topics** on GitHub:
   - csgo, sourcemod, metamod, hvh, counter-strike

2. **Enable GitHub Pages** (optional):
   - For hosting documentation

3. **Add License**:
   - MIT, GPL, or whatever you prefer

4. **Create Releases**:
   - Tag versions: `v1.0.0`, `v1.1.0`, etc.

5. **Add Contributing Guidelines**:
   - `CONTRIBUTING.md` for others who want to help

---

**You're ready to push VileHvH to the world! 🚀**

Need help? Commands not working? Let me know!

