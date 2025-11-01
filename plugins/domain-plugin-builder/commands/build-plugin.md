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

For each command, run sequentially:

Run /domain-plugin-builder:slash-commands-create <command-name> "<description>"
(Wait for completion)

Update TodoWrite: Mark "Build commands" as completed

Phase 4: Build Agents

Ask user how many agents and what they should do.

For each agent, run sequentially:

Run /domain-plugin-builder:agents-create <agent-name> "<description>" "<tools>"
(Wait for completion)

Update TodoWrite: Mark "Build agents" as completed

Phase 5: Build Skills

Ask user how many skills needed.

For each skill, run sequentially:

Run /domain-plugin-builder:skills-create <skill-name> "<description>"
(Wait for completion)

Update TodoWrite: Mark "Build skills" as completed

Phase 6: Build Hooks

Ask user how many hooks needed (optional - can skip).

For each hook, run sequentially:

Run /domain-plugin-builder:hooks-create <hook-name> <event-type> "<action>"
(Wait for completion)

Update TodoWrite: Mark "Build hooks" as completed

Phase 7: Update Marketplace Configuration

Run marketplace sync script:

!{bash plugins/domain-plugin-builder/skills/build-assistant/scripts/sync-marketplace.sh}

This registers the plugin in marketplace.json

Update TodoWrite: Mark "Update marketplace.json" as completed

Phase 8: Register in Settings

Read current settings and add plugin commands:

@.claude/settings.local.json

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

!{bash git add plugins/$ARGUMENTS .claude/marketplace.json .claude/settings.local.json}

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
