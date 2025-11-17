---
description: Create slash command(s) following standardized structure - supports parallel creation for 3+ commands
argument-hint: <command-name> "<description>" [--plugin=name] | <cmd-1> "<desc-1>" <cmd-2> "<desc-2>" ... [--plugin=name]
---

## Security Requirements

**CRITICAL:** All generated files must follow security rules:

@~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/docs/security/SECURITY-RULES.md

**Key requirements:**
- Never hardcode API keys or secrets
- Use placeholders: `your_service_key_here`
- Protect `.env` files with `.gitignore`
- Create `.env.example` with placeholders only
- Document key acquisition for users

**Arguments**: $ARGUMENTS

Goal: Create properly structured slash command(s). For 3+ commands, creates them in parallel for faster execution.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Phase 0: Create Todo List

Create todo list for all phases below.

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- Load composition patterns:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/dans-composition-pattern.md}
- These provide critical understanding of:
  - Commands are the primitive (start here!)
  - When to use commands vs skills vs agents vs hooks
  - Skills compose commands (not vice versa)
  - Composition hierarchies and patterns
  - Anti-patterns to avoid

Phase 2: Parse Arguments and Determine Plugin

Parse $ARGUMENTS to extract:
- Command names and descriptions
- Plugin name (from --plugin=name or detect from pwd)

If plugin not specified:

!{bash basename $(pwd)}

Store plugin name for Phase 3.

Phase 3: Load Templates

Load command template for reference:

!{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md}

Phase 4: Parse Arguments & Determine Mode

Actions:

Use bash to parse $ARGUMENTS and count how many commands are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each command specification:
- If count = 1: Single command mode - extract <command-name> and "<description>"
- If count = 2: Two commands mode - extract both <cmd-N> "<desc-N>" pairs
- If count >= 3: Multiple commands mode - extract all <cmd-N> "<desc-N>" pairs

Phase 5: Create Commands

Actions:

**Decision: 1-2 commands = build directly, 3+ commands = use Task() for parallel**

**For 1-2 Commands:**

Build directly - execute these steps immediately:

1. **List existing agents (to use correct names in Task() calls):**
!{ls plugins/$PLUGIN_NAME/agents/*.md 2>/dev/null}

2. Load template:
!{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md}

3. For each command, create the file:
!{Write plugins/$PLUGIN_NAME/commands/$CMD_NAME.md}

Include:
- Frontmatter with description, argument-hint, allowed-tools
- Use Goal → Actions → Phase pattern
- Keep under 150 lines
- **CRITICAL:** If command invokes agents via Task(), use ACTUAL agent names from step 1!
  - Format: subagent_type="$PLUGIN_NAME:agent-name"
  - Example: If agents/security-scanner.md exists, use subagent_type="my-plugin:security-scanner"
  - NEVER use placeholder names - use REAL agent file names!

4. Validate:
!{Bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/$PLUGIN_NAME/commands/$CMD_NAME.md}

No need for Task() overhead when building 1-2 commands

**For 3+ Commands:**

**CRITICAL: Send ALL Task() calls in a SINGLE MESSAGE for parallel execution!**

Example for 3 commands - send all at once:

```
Task(description="Create command 1", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: $CMD_1_NAME
Description: $CMD_1_DESC
Plugin: $PLUGIN_NAME

**CRITICAL: Use ACTUAL Agent Names**
BEFORE creating the command, list existing agents:
!{ls plugins/$PLUGIN_NAME/agents/*.md 2>/dev/null}

If the command needs to invoke an agent via Task(), use the ACTUAL agent names from the list above!
- Format: subagent_type=\"$PLUGIN_NAME:agent-name\"
- Example: If agents/security-scanner.md exists, use subagent_type=\"$PLUGIN_NAME:security-scanner\"
- NEVER use placeholder names like \"agent1\" or \"scanner\" - use the REAL agent file names!

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/$PLUGIN_NAME/commands/$CMD_1_NAME.md

Follow framework structure:
- Frontmatter with description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS for all argument references
- Use ACTUAL agent names in Task() calls (subagent_type field)
- Validate with validation script

Deliverable: Complete validated command file with correct agent references")

Task(description="Create command 2", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="[Same structure with $CMD_2_NAME, $CMD_2_DESC]")

Task(description="Create command 3", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="[Same structure with $CMD_3_NAME, $CMD_3_DESC]")

[Continue for all N commands from $ARGUMENTS]
```

**DO NOT wait between Task() calls - send them ALL together in one response!**

The agents will run in parallel automatically. Only proceed to Phase 6 after all Task() calls complete.

Phase 6: Validation

For each created command:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/$PLUGIN_NAME/commands/$CMD_NAME.md}

If validation fails, read errors and fix issues.

Phase 7: Sync to Airtable

**Use bulk sync script for efficiency:**

Bash: python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/bulk-sync-airtable.py --plugin={plugin-name} --marketplace={marketplace-name} --type=commands

This syncs ALL commands in parallel instead of one at a time.

**Environment Requirement:**
- Requires AIRTABLE_TOKEN environment variable
- If not set, displays error message with instructions

Phase 8: Register in Settings

**CRITICAL: Commands must be registered to be usable!**

Run registration script to add all created commands to ~/.claude/settings.json:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/register-commands-in-settings.sh $PLUGIN_NAME}

This registers entries like:
- SlashCommand(/$PLUGIN_NAME:$CMD_1)
- SlashCommand(/$PLUGIN_NAME:$CMD_2)
- etc.

Verify registration by checking settings.json contains the new commands.

Phase 9: Self-Validation

Run validation script to verify all work completed:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/$PLUGIN_NAME/commands/*.md}

Mark all todos complete if validation passes.

Phase 10: Summary

Display results:

**Commands Created:** <count>
**Plugin:** $PLUGIN_NAME
**Location:** plugins/$PLUGIN_NAME/commands/

**Files:**
- $CMD_1.md - $DESC_1 ✅
- $CMD_2.md - $DESC_2 ✅
- etc.

**Validation:** All passed ✅
**Registration:** Complete ✅
**Airtable Sync:** Attempted ✅

**Next Steps:**
- Test commands: /$PLUGIN_NAME:$CMD_NAME
- Add to build workflow
- Commit to git
