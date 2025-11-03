---
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, TodoWrite, Skill
description: Create slash command(s) following standardized structure - supports parallel creation for 3+ commands
argument-hint: <command-name> "<description>" [--plugin=name] | <cmd-1> "<desc-1>" <cmd-2> "<desc-2>" ... [--plugin=name]
---

## Security Requirements

**CRITICAL:** All generated files must follow security rules:

@docs/security/SECURITY-RULES.md

**Key requirements:**
- Never hardcode API keys or secrets
- Use placeholders: `your_service_key_here`
- Protect `.env` files with `.gitignore`
- Create `.env.example` with placeholders only
- Document key acquisition for users

**Arguments**: $ARGUMENTS

Goal: Create properly structured slash command(s). For 3+ commands, creates them in parallel for faster execution.

Phase 1: Parse Arguments and Determine Plugin

Parse $ARGUMENTS to extract:
- Command names and descriptions
- Plugin name (from --plugin=name or detect from pwd)

If plugin not specified:

!{bash basename $(pwd)}

Store plugin name for Phase 2.

Phase 2: Load Templates

Load command template for reference:

@template-command-patterns.md

Phase 3: Parse Arguments & Determine Mode

Actions:

Use bash to parse $ARGUMENTS and count how many commands are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each command specification:
- If count = 1: Single command mode - extract <command-name> and "<description>"
- If count = 2: Two commands mode - extract both <cmd-N> "<desc-N>" pairs
- If count >= 3: Multiple commands mode - extract all <cmd-N> "<desc-N>" pairs

Phase 4: Create Commands

Actions:

**ALWAYS use Task() calls - whether creating 1 or 10 commands**

**For Single Command:**

Task(description="Create command", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: $CMD_NAME
Description: $DESCRIPTION
Plugin: $PLUGIN_NAME

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/$PLUGIN_NAME/commands/$CMD_NAME.md

Follow framework structure:
- Frontmatter with description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS for all argument references
- Validate with validation script

Deliverable: Complete validated command file")

**For Multiple Commands (2+):**

**CRITICAL: Send ALL Task() calls in a SINGLE MESSAGE for parallel execution!**

Example for 3 commands - send all at once:

```
Task(description="Create command 1", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: $CMD_1_NAME
Description: $CMD_1_DESC
Plugin: $PLUGIN_NAME

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/$PLUGIN_NAME/commands/$CMD_1_NAME.md

Follow framework structure:
- Frontmatter with description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS for all argument references
- Validate with validation script

Deliverable: Complete validated command file")

Task(description="Create command 2", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="[Same structure with $CMD_2_NAME, $CMD_2_DESC]")

Task(description="Create command 3", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="[Same structure with $CMD_3_NAME, $CMD_3_DESC]")

[Continue for all N commands from $ARGUMENTS]
```

**DO NOT wait between Task() calls - send them ALL together in one response!**

The agents will run in parallel automatically. Only proceed to Phase 5 after all Task() calls complete.

Phase 5: Validation

For each created command:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/$PLUGIN_NAME/commands/$CMD_NAME.md}

If validation fails, read errors and fix issues.

Phase 6: Summary

Display results:

**Commands Created:** <count>
**Plugin:** $PLUGIN_NAME
**Location:** plugins/$PLUGIN_NAME/commands/

**Files:**
- $CMD_1.md - $DESC_1
- $CMD_2.md - $DESC_2
- etc.

**Validation:** All passed ✅

**Next Steps:**
- Test commands: /$PLUGIN_NAME:$CMD_NAME
- Add to build workflow
- Commit to git
