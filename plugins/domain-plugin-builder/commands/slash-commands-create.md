---
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, TodoWrite
description: Create slash command(s) following standardized structure - supports parallel creation for 3+ commands
argument-hint: <command-name> "<description>" [--plugin=name] | <cmd-1> "<desc-1>" <cmd-2> "<desc-2>" ... [--plugin=name]
---

**Arguments**: $ARGUMENTS

Goal: Create properly structured slash command(s). For 3+ commands, creates them in parallel for faster execution.

Phase 1: Parse Arguments and Determine Plugin

Parse $ARGUMENTS to extract:
- Command names and descriptions
- Plugin name (from --plugin=name or detect from pwd)

If plugin not specified, detect from current directory:

!{bash basename $(pwd)}

Store plugin name for Phase 2.

Phase 2: Count Commands and Choose Execution Mode

Count how many commands were requested.

Load template for reference:

@plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Execution modes:
- 1 command: Direct creation
- 2 commands: Sequential creation
- 3+ commands: Parallel creation (invoke multiple slash-commands-builder agents)

Phase 3: Create Commands

**Mode 1: Single Command (1 command)**

Task(description="Create command", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: <name-from-args>
Description: <description-from-args>
Plugin: <plugin-name>

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/<plugin-name>/commands/<command-name>.md

Follow framework structure:
- Frontmatter with description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS for all argument references
- Validate with validation script

Deliverable: Complete validated command file at plugins/<plugin-name>/commands/<command-name>.md")

**Mode 2: Sequential (2 commands)**

For each command sequentially:

Task(description="Create command N", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="<same structure as Mode 1>")

Wait for completion, then create next command.

**Mode 3: Parallel (3+ commands)**

Create TODO list:

TodoWrite with list of all commands to create.

Launch ALL slash-commands-builder agents IN PARALLEL (all at once):

For command 1:
Task(description="Create <cmd-1-name>", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: <cmd-1-name>
Description: <cmd-1-desc>
Plugin: <plugin-name>

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/<plugin-name>/commands/<cmd-1-name>.md

Follow framework structure:
- Frontmatter: description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS not numbered args
- Validate with validation script

Deliverable: Complete validated command file")

For command 2:
Task(description="Create <cmd-2-name>", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: <cmd-2-name>
Description: <cmd-2-desc>
Plugin: <plugin-name>

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/<plugin-name>/commands/<cmd-2-name>.md

Follow framework structure:
- Frontmatter: description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS not numbered args
- Validate with validation script

Deliverable: Complete validated command file")

For command 3:
Task(description="Create <cmd-3-name>", subagent_type="domain-plugin-builder:slash-commands-builder", prompt="You are the slash-commands-builder agent. Create a complete slash command.

Command name: <cmd-3-name>
Description: <cmd-3-desc>
Plugin: <plugin-name>

Load template: plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md

Create command file at: plugins/<plugin-name>/commands/<cmd-3-name>.md

Follow framework structure:
- Frontmatter: description, argument-hint, allowed-tools
- Goal → Actions → Phase pattern
- Keep under 150 lines
- Use $ARGUMENTS not numbered args
- Validate with validation script

Deliverable: Complete validated command file")

Continue for all commands (cmd-4, cmd-5, etc.)

Wait for ALL agents to complete before proceeding.

Update TodoWrite as each completes.

Phase 4: Validate All Commands

For each created command:

!{bash plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/<plugin-name>/commands/<command-name>.md}

If validation fails, read errors and fix issues.

Phase 5: Summary

Display results:

**Commands Created:** <count>
**Plugin:** <plugin-name>
**Location:** plugins/<plugin-name>/commands/

**Files:**
- <command-1-name>.md - <description>
- <command-2-name>.md - <description>
- etc.

**Validation:** All passed ✅

**Next Steps:**
- Test commands: /<plugin-name>:<command-name>
- Add to build workflow
- Commit to git
