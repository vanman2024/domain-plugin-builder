---
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
description: Create slash command(s) following standardized structure - supports parallel creation for 3+ commands
argument-hint: <command-name> "<description>" [--plugin=name] | <cmd-1> "<desc-1>" <cmd-2> "<desc-2>" ... [--plugin=name]
---

**Arguments**: $ARGUMENTS

Goal: Create properly structured slash command(s). For 3+ commands, creates them in parallel for faster execution.

Core Principles:
- Follow template patterns (Simple, Single Agent, Sequential, Parallel)
- Use $ARGUMENTS for all argument references
- Keep commands under 150 lines
- Validate before committing

Phase 1: Parse Arguments & Count Commands
Goal: Determine execution mode

Actions:
- Parse $ARGUMENTS to count how many commands requested
- Extract each command specification (name, description, plugin)
- Determine mode:
  - 1-2 commands: Sequential
  - 3+ commands: Parallel (use Task tool)
- Load template: @~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Phase 2: Create Command(s)
Goal: Generate command files

Actions:

**For Single Command:**
- Use AskUserQuestion if info missing
- Select pattern from template (1: Simple, 2: Single Agent, 3: Sequential, 4: Parallel)
- Create command file following Goal → Actions → Phase structure
- Validate: !{bash bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh COMMAND_FILE}

**For 2 Commands (Sequential):**
- Create first command and validate
- Create second command and validate

**For 3+ Commands (Parallel):**

Launch multiple general-purpose agents IN PARALLEL:

Task(description="Create command 1", subagent_type="general-purpose", prompt="Create slash command: $CMD_1_NAME

Description: $CMD_1_DESC
Plugin: $PLUGIN_NAME

Load template: @~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create: plugins/$PLUGIN_NAME/commands/$CMD_1_NAME.md
- Frontmatter: description, argument-hint, allowed-tools
- Goal → Actions → Phase structure
- Select pattern based on needs
- Validate with validation script

Deliverable: Complete validated command")

Task(description="Create command 2", subagent_type="general-purpose", prompt="[Same for command 2]")

Task(description="Create command 3", subagent_type="general-purpose", prompt="[Same for command 3]")

Wait for ALL agents to complete.

Phase 3: Validation
Goal: Ensure all commands pass validation

Actions:
- Validate each command: !{bash bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh COMMAND_FILE}
- Fix any validation errors
- Re-validate until all pass

Phase 4: Git Commit and Push
Goal: Save work immediately

Actions:
- Add files: !{bash git add plugins/*/commands/*.md .claude-plugin/marketplace.json}
- Commit:
  !{bash git commit -m "$(cat <<'EOF'
feat: Add slash command(s) - COMMAND_NAMES

Complete command structure following framework patterns.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"}
- Push: !{bash git push origin master}

Phase 5: Summary
Goal: Report results

Actions:
- Display all created commands (names, locations, patterns, validation status)
- Show git status (committed and pushed)
- Show usage examples
