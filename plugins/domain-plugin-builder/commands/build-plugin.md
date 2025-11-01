---
description: Build complete plugin with all components and validation
argument-hint: <plugin-name>
allowed-tools: SlashCommand, Task, Read, Write, Edit, Bash, Glob, AskUserQuestion, TodoWrite
---

**Arguments**: $ARGUMENTS

Goal: Build a complete, production-ready Claude Code plugin by orchestrating all builder commands and running comprehensive validation.

Core Principles:
- Orchestrate all sub-commands sequentially
- Track progress with TodoWrite
- Validate at each phase
- Ensure marketplace/settings integration
- Commit and push to GitHub

Phase 1: Initialize Todo List and Verify Location

Create todo list:

TodoWrite with tasks:
- Create plugin scaffold
- Build commands
- Build agents
- Build skills
- Build hooks
- Run validation
- Update marketplace.json
- Update settings.json
- Git commit and push
- Display summary

Verify location:

!{bash pwd}

Expected: domain-plugin-builder directory

Phase 2: Create Plugin Scaffold

Run /domain-plugin-builder:plugin-create $ARGUMENTS
(Wait for completion)

This creates:
- Directory structure
- plugin.json manifest
- README.md

Update TodoWrite: Mark "Create plugin scaffold" as completed

Phase 3: Build Commands

Ask user how many commands and what they should do.

Collect ALL command specifications, then invoke slash-commands-create ONCE with all of them:

Run /domain-plugin-builder:slash-commands-create <cmd-1> "<desc-1>" <cmd-2> "<desc-2>" <cmd-3> "<desc-3>" ... <cmd-N> "<desc-N>"

**CRITICAL:** Pass ALL commands in a SINGLE invocation. Do NOT call the command multiple times.

Examples:
- 1 command: /domain-plugin-builder:slash-commands-create deploy "Deploy application to production"
- 3 commands: /domain-plugin-builder:slash-commands-create init "Initialize project" build "Build the application" deploy "Deploy to production"
- 5 commands: /domain-plugin-builder:slash-commands-create cmd1 "desc1" cmd2 "desc2" cmd3 "desc3" cmd4 "desc4" cmd5 "desc5"

(Wait for completion - the slash-commands-create will handle parallel execution internally)

Update TodoWrite: Mark "Build commands" as completed

Phase 4: Build Agents

Ask user how many agents and what they should do.

Collect ALL agent specifications, then invoke agents-create ONCE with all of them:

Run /domain-plugin-builder:agents-create <agent-1> "<desc-1>" "<tools-1>" <agent-2> "<desc-2>" "<tools-2>" ... <agent-N> "<desc-N>" "<tools-N>"

**CRITICAL:** Pass ALL agents in a SINGLE invocation. Do NOT call the command multiple times.

Examples:
- 1 agent: /domain-plugin-builder:agents-create validator "Validate plugin structure" "Bash, Read, Grep, Glob"
- 3 agents: /domain-plugin-builder:agents-create scanner "Scan code" "Read, Grep" tester "Run tests" "Bash, Read" deployer "Deploy app" "Bash, Read, Write"

(Wait for completion - the agents-create will handle parallel execution internally)

Update TodoWrite: Mark "Build agents" as completed

Phase 5: Build Skills

Ask user how many skills needed.

Collect ALL skill specifications, then invoke skills-create ONCE with all of them:

Run /domain-plugin-builder:skills-create <skill-1> "<desc-1>" <skill-2> "<desc-2>" ... <skill-N> "<desc-N>"

**CRITICAL:** Pass ALL skills in a SINGLE invocation. Do NOT call the command multiple times.

(Wait for completion - the skills-create will handle parallel execution internally)

Update TodoWrite: Mark "Build skills" as completed

Phase 6: Build Hooks

Ask user how many hooks needed (optional - can skip).

Collect ALL hook specifications, then invoke hooks-create ONCE with all of them:

Run /domain-plugin-builder:hooks-create <hook-1> <event-1> "<action-1>" <hook-2> <event-2> "<action-2>" ... <hook-N> <event-N> "<action-N>"

**CRITICAL:** Pass ALL hooks in a SINGLE invocation. Do NOT call the command multiple times.

Example:
- 3 hooks: /domain-plugin-builder:hooks-create pre-validation PreToolUse "Validate inputs" post-logging PostToolUse "Log tool usage" session-init SessionStart "Initialize session"

(Wait for completion - the hooks-create will handle parallel execution internally)

Update TodoWrite: Mark "Build hooks" as completed

Phase 7: Update Marketplace Configuration

Run marketplace sync script:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/sync-marketplace.sh}

This registers the plugin in marketplace.json

Update TodoWrite: Mark "Update marketplace.json" as completed

Phase 8: Register in Settings

Read current settings and add plugin commands:

@~/.claude/settings.local.json

List plugin commands:

!{bash ls plugins/$ARGUMENTS/commands/*.md 2>/dev/null | sed 's|plugins/||; s|/commands/|:|; s|.md||'}

Add to settings.local.json permissions.allow array:
- "SlashCommand(/$ARGUMENTS:*)"

Use Edit tool to insert after last plugin entry.

Update TodoWrite: Mark "Update settings.json" as completed

Phase 9: Run Comprehensive Validation

Run /domain-plugin-builder:validate $ARGUMENTS
(Wait for validation to complete)

The validate command will:
- Invoke plugin-validator agent
- Run all validation scripts
- Check marketplace.json registration
- Check settings.json registration
- Verify git status
- Provide comprehensive report

If validation fails:
- Review errors
- Fix issues
- Re-run validation

Update TodoWrite: Mark "Run validation" as completed

Phase 10: Git Commit and Push

Stage all plugin files:

!{bash git add plugins/$ARGUMENTS .claude/marketplace.json ~/.claude/settings.local.json}

Commit:

!{bash git commit -m "$(cat <<'EOF'
feat: Build complete $ARGUMENTS plugin

Complete plugin with commands, agents, skills, and validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"}

Push to GitHub:

!{bash git push origin master}

Update TodoWrite: Mark "Git commit and push" as completed

Phase 11: Display Summary

Count components:

!{bash ls plugins/$ARGUMENTS/commands/ 2>/dev/null | wc -l}
!{bash ls plugins/$ARGUMENTS/agents/ 2>/dev/null | wc -l}
!{bash ls -d plugins/$ARGUMENTS/skills/*/ 2>/dev/null | wc -l}

Display:

**Plugin Built:** $ARGUMENTS
**Location:** plugins/$ARGUMENTS

**Components:**
- Commands: X
- Agents: Y
- Skills: Z

**Integration:**
- ✅ Registered in marketplace.json
- ✅ Registered in settings.json
- ✅ All validations passed
- ✅ Committed to git
- ✅ Pushed to GitHub

**Next Steps:**
- Test commands: /$ARGUMENTS:<command-name>
- Deploy to marketplace
- Build additional features

Update TodoWrite: Mark "Display summary" as completed
