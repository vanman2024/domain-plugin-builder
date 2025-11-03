# Migration from ai-dev-marketplace

## Overview

The `domain-plugin-builder` has been extracted from `ai-dev-marketplace` into its own standalone marketplace. This migration enables the plugin builder to work across **ALL codebases and marketplaces**, not just ai-dev-marketplace.

## Why the Migration?

### The Problem

Previously, `domain-plugin-builder` was located in:
```
~/.claude/plugins/marketplaces/ai-dev-marketplace/plugins/domain-plugin-builder/
```

All commands used **relative paths**:
```markdown
@plugins/domain-plugin-builder/skills/build-assistant/templates/...
bash plugins/domain-plugin-builder/skills/build-assistant/scripts/...
```

**This only worked when `pwd` was in `ai-dev-marketplace`**, breaking the entire purpose of being a universal plugin builder.

### The Solution

Now `domain-plugin-builder` is its own marketplace:
```
~/.claude/plugins/marketplaces/domain-plugin-builder/
```

All commands use **absolute paths**:
```markdown
@~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/...
bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/...
```

**This works from ANY directory** in ANY codebase!

## What Changed

### Repository Structure

**Before**:
```
ai-dev-marketplace/
└── plugins/
    └── domain-plugin-builder/
        ├── commands/
        ├── agents/
        ├── skills/
        └── docs/
```

**After**:
```
domain-plugin-builder/              # Standalone repository
├── .claude-plugin/
│   └── marketplace.json
└── plugins/domain-plugin-builder/
    ├── commands/
    ├── agents/
    ├── skills/
    └── docs/
```

### Path References

**Before** (Relative - BROKEN):
```markdown
Run: `bash plugins/domain-plugin-builder/skills/build-assistant/scripts/list-agents.sh`
Load: @plugins/domain-plugin-builder/docs/frameworks/claude/component-decision-framework.md
```

**After** (Absolute - WORKS EVERYWHERE):
```markdown
Run: `bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/list-agents.sh`
Load: @~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/component-decision-framework.md`
```

### Command Registration

**Before**: Commands registered in `ai-dev-marketplace` settings

**After**: Commands registered globally, work from ANY marketplace

## Migration Steps for Users

### 1. Install New Marketplace

```bash
cd ~/.claude/plugins/marketplaces
git clone https://github.com/vanman2024/domain-plugin-builder.git
```

### 2. Update Settings

Add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "SlashCommand(/domain-plugin-builder:*)"
    ]
  }
}
```

### 3. Remove Old Installation (Optional)

If you previously had domain-plugin-builder in ai-dev-marketplace:

```bash
# Remove old plugin (keep the marketplace)
cd ~/.claude/plugins/marketplaces/ai-dev-marketplace
rm -rf plugins/domain-plugin-builder

# Update ai-dev-marketplace's marketplace.json to remove domain-plugin-builder entry
```

### 4. Verify Installation

```bash
# Test from any directory
cd ~
# Commands should work from anywhere
```

## Breaking Changes

### None for End Users

If you were using the plugin builder commands, they work exactly the same way:

```bash
# Before and After - Same commands
/domain-plugin-builder:plugin-create my-plugin
/domain-plugin-builder:slash-commands-create my-command "Description"
```

### For Plugin Developers

If you have plugins that **reference domain-plugin-builder resources**:

**Before**:
```markdown
@plugins/domain-plugin-builder/docs/sdks/my-sdk-documentation.md
```

**After**:
```markdown
@~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/sdks/my-sdk-documentation.md
```

## Benefits of Migration

### ✅ Universal Compatibility

Works in **ANY** codebase:
- ✅ ai-dev-marketplace
- ✅ dev-lifecycle-marketplace
- ✅ mcp-servers-marketplace
- ✅ Custom projects
- ✅ Client codebases
- ✅ Non-marketplace directories

### ✅ Independent Lifecycle

- Version domain-plugin-builder independently
- Update without affecting other marketplaces
- Fork and customize easily

### ✅ Clean Separation

- Meta-tool separated from domain plugins
- Clearer architectural boundaries
- Easier to maintain

### ✅ True Portability

- One installation works everywhere
- No need to install per marketplace
- Consistent behavior across environments

## Technical Details

### Path Resolution

The absolute paths use `~/.claude/plugins/marketplaces/domain-plugin-builder/` which:
- ✅ Resolves from any directory
- ✅ Works in bash scripts
- ✅ Works with @ file loading syntax
- ✅ Compatible with Docker/CI (with proper $HOME)

### Script Compatibility

All validation scripts updated:
- `validate-command.sh`
- `validate-agent.sh`
- `validate-plugin.sh`
- `validate-skill.sh`
- `sync-marketplace.sh`

All use absolute paths to domain-plugin-builder installation.

## Rollback Plan

If issues arise, you can temporarily rollback:

```bash
# Restore old installation
cd ~/.claude/plugins/marketplaces/ai-dev-marketplace/plugins
git checkout <previous-commit> domain-plugin-builder/

# Remove new installation
rm -rf ~/.claude/plugins/marketplaces/domain-plugin-builder
```

However, this returns to the broken state where it only works in ai-dev-marketplace.

## Timeline

- **Before**: domain-plugin-builder in ai-dev-marketplace (broken for cross-repo use)
- **Now**: domain-plugin-builder as standalone marketplace (works everywhere)
- **Future**: Potential to package as npm/pip module for even easier distribution

## FAQ

### Q: Do I need to reinstall in each marketplace?

**A**: No! Install once in `~/.claude/plugins/marketplaces/domain-plugin-builder/` and use from anywhere.

### Q: Will my existing plugins break?

**A**: No. Plugins you created with the old version work fine. Only the builder itself has moved.

### Q: Can I use both old and new versions?

**A**: Not recommended. Use the new standalone version exclusively for consistent behavior.

### Q: What about plugins I'm currently building?

**A**: Complete them with the old version, then switch to the new one for future plugins.

### Q: How do I update the builder?

**A**:
```bash
cd ~/.claude/plugins/marketplaces/domain-plugin-builder
git pull origin master
```

## Support

- **Repository**: https://github.com/vanman2024/domain-plugin-builder
- **Issues**: https://github.com/vanman2024/domain-plugin-builder/issues
- **Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)

## Conclusion

This migration transforms domain-plugin-builder from a marketplace-specific tool to a **true universal plugin builder** that works everywhere. The architectural change is significant, but the user experience remains identical while gaining massive portability benefits.

**Recommendation**: Migrate to the standalone version immediately for maximum flexibility.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
