---
description: Create hook(s) following standardized structure - supports parallel creation for 3+ hooks
argument-hint: <hook-name> <event-type> "<action>" [--plugin=name] | <hook-1> <event-1> ... [--plugin=name]
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---

**Arguments**: $ARGUMENTS

Goal: Create properly structured hooks. For 3+ hooks, creates them in parallel for faster execution.

Phase 1: Parse Arguments and Determine Plugin

Parse $ARGUMENTS to extract:
- Hook names and event types
- Plugin name (from --plugin=name or detect from pwd)

If plugin not specified:

!{bash basename $(pwd)}

Store plugin name for Phase 2.

Phase 2: Load Hooks Documentation

WebFetch: https://docs.claude.com/en/docs/claude-code/hooks-guide

This provides context on:
- Available event types and when they trigger
- Hook configuration structure
- Script patterns and best practices

Phase 3: Count Hooks and Choose Execution Mode

Count how many hooks were requested.

Execution modes:
- 1 hook: Direct creation
- 2 hooks: Sequential creation
- 3+ hooks: Parallel creation (invoke multiple hooks-builder agents)

Phase 4: Create Hooks

**Mode 1: Single Hook (1 hook)**

Task(description="Create hook", subagent_type="domain-plugin-builder:hooks-builder", prompt="You are the hooks-builder agent. Create a complete hook.

Hook name: <name-from-args>
Event type: <event-from-args>
Action: <action-from-args>
Plugin: <plugin-name>

Create hook configuration and script:
- Executable script in plugins/<plugin-name>/scripts/
- Hook entry in plugins/<plugin-name>/hooks/hooks.json
- Documentation in plugins/<plugin-name>/docs/hooks.md
- Use ${CLAUDE_PLUGIN_ROOT} for paths
- Validate hook structure

Deliverable: Complete hook with script, config, and documentation")

**Mode 2: Sequential (2 hooks)**

For each hook sequentially:
Task(description="Create hook N", subagent_type="domain-plugin-builder:hooks-builder", prompt="<same structure>")

Wait for completion, then create next hook.

**Mode 3: Parallel (3+ hooks)**

Create TODO list:

TodoWrite with list of all hooks to create.

Launch ALL hooks-builder agents IN PARALLEL (all at once):

Task(description="Create <hook-1-name>", subagent_type="domain-plugin-builder:hooks-builder", prompt="You are the hooks-builder agent. Create a complete hook.

Hook name: <hook-1-name>
Event type: <hook-1-event>
Action: <hook-1-action>
Plugin: <plugin-name>

Create:
- Script: plugins/<plugin-name>/scripts/<hook-1-name>.sh
- Config: Update plugins/<plugin-name>/hooks/hooks.json
- Docs: Update plugins/<plugin-name>/docs/hooks.md
- Use ${CLAUDE_PLUGIN_ROOT} for all paths

Deliverable: Complete hook")

Task(description="Create <hook-2-name>", subagent_type="domain-plugin-builder:hooks-builder", prompt="You are the hooks-builder agent. Create a complete hook.

Hook name: <hook-2-name>
Event type: <hook-2-event>
Action: <hook-2-action>
Plugin: <plugin-name>

Create:
- Script: plugins/<plugin-name>/scripts/<hook-2-name>.sh
- Config: Update plugins/<plugin-name>/hooks/hooks.json
- Docs: Update plugins/<plugin-name>/docs/hooks.md

Deliverable: Complete hook")

Continue for all hooks (hook-3, hook-4, etc.)

Wait for ALL agents to complete before proceeding.

Update TodoWrite as each completes.

Phase 5: Summary

Display results:

**Hooks Created:** <count>
**Plugin:** <plugin-name>
**Location:** plugins/<plugin-name>/hooks/

**Hooks:**
- <hook-1-name> (Event: <event-1>) - <action-1>
- <hook-2-name> (Event: <event-2>) - <action-2>
- etc.

**Next Steps:**
- Test hooks by triggering events
- Review scripts for correctness
- Commit to git
