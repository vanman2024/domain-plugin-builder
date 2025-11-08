# Airtable Sync Guarantee

This document explains how the domain-plugin-builder ensures that all components are always synced to Airtable.

## Overview

Every component (agent, command, skill, hook) created by the builder commands is automatically synced to Airtable for tracking and discovery. This provides a **guarantee** that the filesystem and Airtable database stay in sync.

## Automatic Sync in Builder Commands

All builder commands automatically sync components to Airtable:

### 1. Agents (`/domain-plugin-builder:agents-create`)

**Sync Phase**: Added after agent creation, before summary

```bash
python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py \
  --type=agent \
  --name=<agent-name> \
  --plugin=<plugin-name> \
  --marketplace=<marketplace-name>
```

**Location in workflow**: Phase 5 (after creation, before validation)

### 2. Commands (`/domain-plugin-builder:slash-commands-create`)

**Sync Phase**: Added after command creation, before summary

```bash
python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py \
  --type=command \
  --name=<command-name> \
  --plugin=<plugin-name> \
  --marketplace=<marketplace-name>
```

**Location in workflow**: Phase 5 (after creation, before validation)

### 3. Skills (`/domain-plugin-builder:skills-create`)

**Sync Phase**: Added after skill creation, before summary

```bash
python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py \
  --type=skill \
  --name=<skill-name> \
  --plugin=<plugin-name> \
  --marketplace=<marketplace-name>
```

**Location in workflow**: Phase 5 (after creation, before validation)

### 4. Hooks (`/domain-plugin-builder:hooks-create`)

**Sync Phase**: Added after hook creation, before summary (Phase 5.5)

```bash
python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py \
  --type=hook \
  --name=<hook-name> \
  --plugin=<plugin-name> \
  --marketplace=<marketplace-name> \
  --event-type=<event-type> \
  --script-path=<script-path>
```

**Location in workflow**: Phase 5.5 (after creation, before summary)

## Validation & Monitoring

### Running Validation

Check sync status across all marketplaces:

```bash
python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-validator.py
```

Check specific marketplace:

```bash
python scripts/sync-validator.py --marketplace=ai-dev-marketplace
```

### Understanding the Report

The validator provides three metrics:

1. **✅ Synced**: Components that exist in both filesystem and Airtable
2. **⚠️  Missing**: Components in filesystem but NOT in Airtable (need sync)
3. **🗑️  Orphaned**: Components in Airtable but NOT in filesystem (should be removed)

Example report:

```
================================================================================
📊 AIRTABLE SYNC VALIDATION REPORT
================================================================================

✅ Synced:   146 components
⚠️  Missing:  148 components (in filesystem but not Airtable)
🗑️  Orphaned: 310 components (in Airtable but not filesystem)

================================================================================
⚠️  MISSING IN AIRTABLE (need to sync)
================================================================================

AGENTS:
  - nextjs-frontend/component-builder-agent

COMMANDS:
  - nextjs-frontend/scaffold-app
  - nextjs-frontend/add-page
  ...
```

### Auto-Sync Missing Components

Automatically sync all missing components:

```bash
python scripts/sync-validator.py --auto-sync
```

This will:
1. Identify all components missing from Airtable
2. Run `sync-component.py` for each missing component
3. Create Airtable records with proper linkage to plugins

### Handling Orphaned Records

Components marked as "Orphaned" exist in Airtable but not in the filesystem. This happens when:
- Files are deleted without updating Airtable
- Components are renamed
- Plugins are moved between marketplaces

To clean up orphaned records:

```bash
python scripts/sync-validator.py --fix-orphans
```

**Warning**: This will DELETE records from Airtable. Review the list carefully before using this option.

## Sync Guarantee Mechanism

### How It Works

1. **Component Creation**:
   - Builder command creates component file(s)
   - Validates component structure
   - Immediately syncs to Airtable

2. **Airtable Record Creation**:
   - Checks if plugin exists (creates if missing)
   - Checks if component already exists
   - Creates new record OR updates existing record
   - Returns success confirmation

3. **Error Handling**:
   - If sync fails, command reports failure
   - Component is still created on filesystem
   - Can be manually synced later with `sync-component.py`

### Environment Variables

The sync scripts support both token formats:

- `AIRTABLE_TOKEN` - Standard Airtable API token
- `MCP_AIRTABLE_TOKEN` - MCP server token format

One of these must be set in your environment.

### Airtable Schema

Components are stored in these tables:

**Plugins Table**:
- Name (text)
- Marketplace Link (linked record - auto-created)

**Agents Table**:
- Agent Name (text)
- Plugin (linked record to Plugins)
- Additional fields auto-populated from frontmatter

**Commands Table**:
- Name (text)
- Command Name (text, e.g., `/plugin:command`)
- Plugin (linked record to Plugins)
- Description (text)
- Argument Hint (text)

**Skills Table**:
- Skill Name (text)
- Plugin (linked record to Plugins)
- Description (text)

**Hooks Table**:
- Hook Name (text)
- Event Type (text: PreToolUse, PostToolUse, etc.)
- Plugin (linked record to Plugins)

## Best Practices

### 1. Always Run Validation After Bulk Changes

After creating multiple components:

```bash
python scripts/sync-validator.py
```

### 2. Sync Before Major Releases

Before tagging releases or deploying:

```bash
python scripts/sync-validator.py --auto-sync
```

Ensures all components are discoverable in Airtable.

### 3. Regular Audits

Run validation weekly or monthly:

```bash
# Check status
python scripts/sync-validator.py

# Fix if needed
python scripts/sync-validator.py --auto-sync
```

### 4. CI/CD Integration

Add to GitHub Actions:

```yaml
- name: Validate Airtable Sync
  run: |
    python scripts/sync-validator.py
  env:
    AIRTABLE_TOKEN: ${{ secrets.AIRTABLE_TOKEN }}
```

Fails CI if components are out of sync.

## Troubleshooting

### "AIRTABLE_TOKEN environment variable not set"

**Solution**: Export token in your shell:

```bash
export AIRTABLE_TOKEN=your_token_here
# OR
export MCP_AIRTABLE_TOKEN=your_token_here
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

### "Plugin 'xyz' not found in Airtable"

**Solution**: The plugin record is auto-created on first sync. If this fails:

1. Check token permissions
2. Verify BASE_ID is correct in scripts
3. Manually create plugin in Airtable UI

### Components Missing After Bulk Creation

**Solution**: Run auto-sync:

```bash
python scripts/sync-validator.py --auto-sync
```

### "Unknown field name" Errors

**Solution**: Airtable schema changed. Update `sync-component.py` to match current field names in Airtable base.

## Manual Sync

To manually sync a single component:

**Agent**:
```bash
python scripts/sync-component.py \
  --type=agent \
  --name=my-agent \
  --plugin=my-plugin \
  --marketplace=ai-dev-marketplace
```

**Command**:
```bash
python scripts/sync-component.py \
  --type=command \
  --name=my-command \
  --plugin=my-plugin \
  --marketplace=ai-dev-marketplace
```

**Skill**:
```bash
python scripts/sync-component.py \
  --type=skill \
  --name=my-skill \
  --plugin=my-plugin \
  --marketplace=ai-dev-marketplace
```

**Hook**:
```bash
python scripts/sync-component.py \
  --type=hook \
  --name=my-hook \
  --plugin=my-plugin \
  --marketplace=ai-dev-marketplace \
  --event-type=PreToolUse \
  --script-path=/path/to/hook.sh
```

## Summary

The domain-plugin-builder provides a **guarantee** that all components stay synced through:

1. ✅ **Automatic sync** in every builder command
2. ✅ **Validation tools** for audit and verification
3. ✅ **Auto-sync capability** for bulk fixes
4. ✅ **Manual sync** for edge cases
5. ✅ **Clear reporting** on sync status

This ensures the Airtable database is always an accurate reflection of components in the filesystem.
