# Installation Guide

## Overview

The Domain Plugin Builder is a standalone marketplace that provides tools for building Claude Code plugins across ANY codebase or marketplace.

## Prerequisites

- Claude Code installed and configured
- Git installed
- GitHub account (for pushing created plugins)

## Installation Methods

### Method 1: Clone from GitHub (Recommended)

```bash
# Navigate to Claude marketplaces directory
cd ~/.claude/plugins/marketplaces

# Clone the repository
git clone https://github.com/vanman2024/domain-plugin-builder.git

# Verify installation
ls -la domain-plugin-builder/plugins/domain-plugin-builder
```

### Method 2: Manual Download

1. Download the repository as ZIP from GitHub
2. Extract to `~/.claude/plugins/marketplaces/domain-plugin-builder/`
3. Verify the structure matches the expected layout

## Post-Installation Configuration

### 1. Register Commands in Claude Code

The domain-plugin-builder commands need to be registered in your Claude Code settings:

**Location**: `~/.claude/settings.json` or `~/.claude/settings.local.json`

Add the following to the `permissions.allow` array:

```json
{
  "permissions": {
    "allow": [
      "SlashCommand(/domain-plugin-builder:*)",
      "SlashCommand(/domain-plugin-builder:plugin-create)",
      "SlashCommand(/domain-plugin-builder:slash-commands-create)",
      "SlashCommand(/domain-plugin-builder:agents-create)",
      "SlashCommand(/domain-plugin-builder:skills-create)",
      "SlashCommand(/domain-plugin-builder:build-plugin)"
    ]
  }
}
```

### 2. Verify Installation

Test that the commands are available:

```bash
# In Claude Code, try running:
/domain-plugin-builder:
# (Tab to see available commands)
```

You should see:
- `/domain-plugin-builder:plugin-create`
- `/domain-plugin-builder:slash-commands-create`
- `/domain-plugin-builder:agents-create`
- `/domain-plugin-builder:skills-create`
- `/domain-plugin-builder:build-plugin`

## Directory Structure

After installation, you should have:

```
~/.claude/plugins/marketplaces/domain-plugin-builder/
├── .claude-plugin/
│   └── marketplace.json
├── README.md
├── INSTALLATION.md
└── plugins/domain-plugin-builder/
    ├── commands/
    │   ├── plugin-create.md
    │   ├── slash-commands-create.md
    │   ├── agents-create.md
    │   ├── skills-create.md
    │   └── build-plugin.md
    ├── agents/
    │   ├── plugin-validator.md
    │   └── skills-builder.md
    ├── skills/
    │   └── build-assistant/
    │       ├── templates/
    │       ├── scripts/
    │       └── examples.md
    └── docs/
        └── frameworks/
```

## Usage

### Building Your First Plugin

```bash
# Navigate to the marketplace where you want to create a plugin
cd ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace

# Run the plugin builder
/domain-plugin-builder:plugin-create my-first-plugin
```

### Adding Components to Existing Plugins

```bash
# Add a slash command
/domain-plugin-builder:slash-commands-create my-command "Description" --plugin=my-plugin

# Add an agent
/domain-plugin-builder:agents-create my-agent "Description" "Bash, Read, Write"

# Add a skill
/domain-plugin-builder:skills-create my-skill "Description"
```

## Troubleshooting

### Commands Not Found

**Problem**: Slash commands don't appear or aren't recognized

**Solution**:
1. Check that the repository is in `~/.claude/plugins/marketplaces/domain-plugin-builder/`
2. Verify commands are registered in `~/.claude/settings.json`
3. Restart Claude Code

### Path Errors

**Problem**: "File not found" errors when running commands

**Solution**:
1. Verify installation path: `ls ~/.claude/plugins/marketplaces/domain-plugin-builder/`
2. Check that all files were copied correctly
3. Ensure paths in commands use absolute paths (`~/.claude/plugins/marketplaces/domain-plugin-builder/...`)

### Script Permission Errors

**Problem**: "Permission denied" when running validation scripts

**Solution**:
```bash
# Make scripts executable
chmod +x ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/*.sh
```

## Cross-Repository Usage

The beauty of this marketplace is that it works **everywhere**:

```bash
# Build plugins in ai-dev-marketplace
cd ~/.claude/plugins/marketplaces/ai-dev-marketplace
/domain-plugin-builder:plugin-create ai-specific-plugin

# Build plugins in dev-lifecycle-marketplace
cd ~/.claude/plugins/marketplaces/dev-lifecycle-marketplace
/domain-plugin-builder:plugin-create lifecycle-plugin

# Build plugins in custom projects
cd ~/my-custom-project
/domain-plugin-builder:plugin-create custom-plugin
```

The domain-plugin-builder uses absolute paths, so it works from ANY directory!

## Updating

To update to the latest version:

```bash
cd ~/.claude/plugins/marketplaces/domain-plugin-builder
git pull origin master
```

## Uninstallation

To remove the domain-plugin-builder:

```bash
# Remove the marketplace
rm -rf ~/.claude/plugins/marketplaces/domain-plugin-builder

# Remove command registrations from ~/.claude/settings.json
# (Edit manually to remove SlashCommand(/domain-plugin-builder:*) entries)
```

## Support

- **Issues**: https://github.com/vanman2024/domain-plugin-builder/issues
- **Documentation**: See `/docs` directory in the repository
- **Examples**: See `skills/build-assistant/templates/` for examples

## Next Steps

After installation:
1. Read the main [README.md](README.md) for features overview
2. Check out [templates](plugins/domain-plugin-builder/skills/build-assistant/templates/) for examples
3. Try building your first plugin with `/domain-plugin-builder:plugin-create`
4. Explore the [documentation](plugins/domain-plugin-builder/docs/) for advanced usage

---

**Happy plugin building!** 🚀
