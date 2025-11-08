# Airtable Sync Failsafe Mechanism

This document explains the **dual-layer sync guarantee** that ensures components are ALWAYS synced to Airtable, even if agents skip steps.

## The Problem

**Original approach (command-based sync only):**
- Agents execute bash commands to sync: `!{bash python sync-component.py ...}`
- If agent skips this step → component NOT synced
- Relies on perfect agent execution
- **No guarantee of sync**

## The Solution: Dual-Layer Sync

### Layer 1: Command-Based Sync (Best Effort)

All builder commands include explicit sync steps:
- `/domain-plugin-builder:agents-create` - Phase 5
- `/domain-plugin-builder:slash-commands-create` - Phase 5
- `/domain-plugin-builder:skills-create` - Phase 4
- `/domain-plugin-builder:hooks-create` - Phase 5.5

**When it works**: Agent follows all phases → immediate sync
**When it fails**: Agent skips sync phase → Layer 2 catches it

### Layer 2: PostToolUse Hook (Failsafe)

**Hook configuration** (`hooks/hooks.json`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/auto-sync-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**How it works**:

1. **Trigger**: Every time Write or Edit tool is used
2. **Detection**: Hook analyzes file path:
   - Is it in `/plugins/<plugin>/agents/`?
   - Is it in `/plugins/<plugin>/commands/`?
   - Is it in `/plugins/<plugin>/skills/`?
3. **Auto-sync**: If yes, automatically syncs to Airtable
4. **Background**: Runs in background (non-blocking)
5. **Logging**: Records success/failure to `~/.claude/auto-sync.log`

## Hook Implementation

### File: `scripts/auto-sync-hook.sh`

```bash
#!/bin/bash
# Receives JSON via stdin with tool_input.file_path

# Extract info from JSON
TOOL_NAME=$(echo "$TOOL_EVENT" | jq -r '.tool_name')
FILE_PATH=$(echo "$TOOL_EVENT" | jq -r '.tool_input.file_path')

# Check if component file
if [[ "$FILE_PATH" =~ /plugins/([^/]+)/(agents|commands|skills)/ ]]; then
  # Extract plugin, type, name, marketplace
  # Run sync in background
  python sync-component.py --type=... --name=... --plugin=... --marketplace=...
fi
```

### What Gets Synced

**Agents**: Any `.md` file in `plugins/*/agents/`
**Commands**: Any `.md` file in `plugins/*/commands/`
**Skills**: Any `SKILL.md` file in `plugins/*/skills/*/`
**Hooks**: Not auto-synced (require event-type parameter)

## How It Guarantees Sync

### Scenario 1: Agent Follows All Steps
1. Agent creates component file (Write tool)
2. Hook triggers → detects component → syncs
3. Agent runs explicit sync command → updates existing record
4. **Result**: Component synced (idempotent)

### Scenario 2: Agent Skips Sync Step
1. Agent creates component file (Write tool)
2. Hook triggers → detects component → syncs
3. Agent skips sync command (forgot/error)
4. **Result**: Component STILL synced (failsafe caught it)

### Scenario 3: Agent Edits Component
1. Agent edits component file (Edit tool)
2. Hook triggers → detects component → syncs
3. **Result**: Airtable record updated

## Monitoring

### Auto-Sync Log

All hook executions are logged:

```bash
tail -f ~/.claude/auto-sync.log
```

Example output:
```
[2025-01-08 10:23:45] ✅ Auto-synced agent: nextjs-frontend/app-scaffolding-agent
[2025-01-08 10:24:12] ✅ Auto-synced command: planning/add-feature
[2025-01-08 10:25:03] ❌ Auto-sync failed for skill: quality/security-scan
```

### Detailed Logs

Each sync creates a detailed log:

```bash
cat /tmp/auto-sync-agent-app-scaffolding-agent.log
```

Shows full sync output, errors, Airtable responses.

## Validation

### Check Sync Status

Run validator to see current state:

```bash
python scripts/sync-validator.py
```

If hook is working properly:
- New components automatically show as "Synced"
- Missing components are only old ones (pre-hook)

### Test the Hook

1. Create a test component:
   ```bash
   echo "test" > plugins/test-plugin/agents/test-agent.md
   ```

2. Wait 3 seconds (hook runs in background)

3. Check log:
   ```bash
   tail ~/.claude/auto-sync.log
   ```

4. Should see: `✅ Auto-synced agent: test-plugin/test-agent`

## Best Practices

### 1. Keep Both Layers

**Don't remove command-based sync** just because hook exists:
- Command sync is immediate (no 2-second delay)
- Provides confirmation in command output
- Hook is backup, not replacement

### 2. Monitor the Log

Check auto-sync log weekly:

```bash
grep "❌" ~/.claude/auto-sync.log
```

Investigate any failures.

### 3. Run Validation

Monthly validation ensures everything synced:

```bash
python scripts/sync-validator.py --auto-sync
```

Catches any edge cases hook might miss.

### 4. Hook Maintenance

If hook stops working:

1. Check if hooks.json is valid:
   ```bash
   jq . plugins/domain-plugin-builder/hooks/hooks.json
   ```

2. Check script permissions:
   ```bash
   ls -la plugins/domain-plugin-builder/scripts/auto-sync-hook.sh
   ```

3. Test manually:
   ```bash
   echo '{"tool_name":"Write","tool_input":{"file_path":"plugins/test/agents/test.md"}}' | \
     bash plugins/domain-plugin-builder/scripts/auto-sync-hook.sh
   ```

## Limitations

### What Hook Cannot Sync

**Hooks** (require event-type parameter):
- Can't determine event type from file path alone
- Must use command-based sync: `/domain-plugin-builder:hooks-create`

**Files Outside Pattern**:
- Random .md files not in agents/commands/skills/
- Files in wrong directory structure

### Performance

- Hook adds ~2 second delay (background process)
- Minimal impact on agent execution
- Sync happens asynchronously

## Summary

**Dual-layer guarantee:**

| Layer | Method | When | Purpose |
|-------|--------|------|---------|
| 1 | Command-based | Phase 5 in builder commands | Immediate sync with confirmation |
| 2 | PostToolUse hook | Every Write/Edit of component | Failsafe backup sync |

**Result**: Components sync even if agents are imperfect ✅

**Validation**: `sync-validator.py` ensures nothing slips through

**Monitoring**: `~/.claude/auto-sync.log` tracks all hook executions

This provides a **guarantee** that components stay synced to Airtable regardless of agent behavior.
