---
description: Build complete plugin with all components and validation
argument-hint: <plugin-name> [--marketplace]
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

Goal: Build a complete, production-ready Claude Code plugin by orchestrating all builder commands and running comprehensive validation.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, TodoWrite, SlashCommand, Task)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Core Principles:
- Orchestrate all sub-commands sequentially
- Track progress with TodoWrite
- Validate at each phase
- Ensure marketplace/settings integration
- Commit and push to GitHub

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- Load composition patterns:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/dans-composition-pattern.md}
- These guide all component creation decisions throughout the build process

Phase 2: Initialize Todo List and Verify Location

Create todo list:

TodoWrite with tasks:
- Parse arguments and determine mode
- Create plugin scaffold
- Build agents (FIRST - so commands can reference them!)
- Build commands (AFTER agents - can reference agent names correctly)
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

Mark first task as in_progress before proceeding.

Phase 2.5: Parse Arguments and Determine Mode

Parse $ARGUMENTS to extract:
- Plugin name
- Marketplace mode (check for --marketplace flag)

Extract plugin name from $ARGUMENTS (first argument before any flags).

Determine base path based on --marketplace flag:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "plugins/$(echo "$ARGUMENTS" | awk '{print $1}')" || echo "."}

Store as $BASE_PATH:
- If --marketplace present: BASE_PATH="plugins/$PLUGIN_NAME"
- If --marketplace absent: BASE_PATH="." (standalone plugin mode)

All subsequent file operations use $BASE_PATH instead of hardcoded "plugins/$PLUGIN_NAME"

Update TodoWrite: Mark "Parse arguments and determine mode" as completed

Phase 3: Create Plugin Scaffold

**Use SlashCommand tool to invoke the command:**

Determine if marketplace flag should be passed:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "--marketplace" || echo ""}

Store marketplace flag result and pass to plugin-create:

SlashCommand(/domain-plugin-builder:plugin-create $ARGUMENTS)

This creates:
- Directory structure
- plugin.json manifest
- README.md

Wait for the command to complete, then update TodoWrite: Mark "Create plugin scaffold" as completed

Phase 4: Build Agents

Ask user how many agents and what they should do.

Collect ALL agent specifications, then use SlashCommand tool to invoke agents-create ONCE with all of them:

**Use SlashCommand tool:**

Build the command with marketplace flag if present:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "/domain-plugin-builder:agents-create <agent-1> \"<desc-1>\" <agent-2> \"<desc-2>\" ... <agent-N> \"<desc-N>\" --marketplace" || echo "/domain-plugin-builder:agents-create <agent-1> \"<desc-1>\" <agent-2> \"<desc-2>\" ... <agent-N> \"<desc-N>\""}

SlashCommand with appropriate flags based on marketplace mode.

**CRITICAL:** Pass ALL agents in a SINGLE SlashCommand invocation. Do NOT call multiple times.

**Note:** Agents inherit tools from parent - no need to specify tools parameter.

Examples:
- 1 agent: SlashCommand(/domain-plugin-builder:agents-create validator "Validate plugin structure")
- 3 agents: SlashCommand(/domain-plugin-builder:agents-create scanner "Scan code" tester "Run tests" deployer "Deploy app")

Wait for the command to complete (agents-create handles parallel execution internally)

Update TodoWrite: Mark "Build agents" as completed

Phase 5: Build Commands

**IMPORTANT:** Agents are now created, so commands can reference them correctly!

Ask user how many commands and what they should do.

Collect ALL command specifications, then use SlashCommand tool to invoke slash-commands-create ONCE with all of them:

**Use SlashCommand tool:**

Build the command with marketplace flag if present:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "/domain-plugin-builder:slash-commands-create <cmd-1> \"<desc-1>\" <cmd-2> \"<desc-2>\" <cmd-3> \"<desc-3>\" ... <cmd-N> \"<desc-N>\" --marketplace" || echo "/domain-plugin-builder:slash-commands-create <cmd-1> \"<desc-1>\" <cmd-2> \"<desc-2>\" <cmd-3> \"<desc-3>\" ... <cmd-N> \"<desc-N>\""}

SlashCommand with appropriate flags based on marketplace mode.

**CRITICAL:** Pass ALL commands in a SINGLE SlashCommand invocation. Do NOT call multiple times.

Examples:
- 1 command: SlashCommand(/domain-plugin-builder:slash-commands-create deploy "Deploy application to production")
- 3 commands: SlashCommand(/domain-plugin-builder:slash-commands-create init "Initialize project" build "Build the application" deploy "Deploy to production")

Wait for the command to complete (slash-commands-create handles parallel execution internally)

Update TodoWrite: Mark "Build commands" as completed

Phase 6: Build Skills

Ask user how many skills needed.

Collect ALL skill specifications, then use SlashCommand tool to invoke skills-create ONCE with all of them:

**Use SlashCommand tool:**

Build the command with marketplace flag if present:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "/domain-plugin-builder:skills-create <skill-1> \"<desc-1>\" <skill-2> \"<desc-2>\" ... <skill-N> \"<desc-N>\" --marketplace" || echo "/domain-plugin-builder:skills-create <skill-1> \"<desc-1>\" <skill-2> \"<desc-2>\" ... <skill-N> \"<desc-N>\""}

SlashCommand with appropriate flags based on marketplace mode.

**CRITICAL:** Pass ALL skills in a SINGLE SlashCommand invocation. Do NOT call multiple times.

Wait for the command to complete (skills-create handles parallel execution internally)

Update TodoWrite: Mark "Build skills" as completed

Phase 7: Build Hooks

**IMPORTANT: Most plugins DON'T need hooks! Only ask if the plugin needs system-level automation.**

**Skip hooks if the plugin provides:**
- Features (commands, agents, skills for user tasks)
- Development tools
- Integrations
- Workflow orchestration

**Include hooks ONLY if the plugin needs:**
- **Auto-formatting**: Run formatters automatically after edits (PostToolUse)
- **Security/Compliance**: Block sensitive file modifications (PreToolUse)
- **Logging/Auditing**: Track all tool executions for compliance (PostToolUse)
- **Custom Notifications**: Modify notification behavior (Notification hook)
- **Session Management**: Initialize/cleanup on session start/end (SessionStart/SessionEnd)

**Decision:**
Ask user: "Does this plugin need system-level automation (auto-formatting, security blocking, logging, notifications)?"

**If NO (most plugins):**
- Create empty hooks directory and hooks.json:
  !{bash mkdir -p $BASE_PATH/hooks}
  !{Write $BASE_PATH/hooks/hooks.json}
  Content:
  ```json
  {
    "hooks": {
      "PreToolUse": [], "PostToolUse": [], "UserPromptSubmit": [], "SessionStart": [], "SessionEnd": [], "PreCompact": []
    }
  }
  ```
- Update TodoWrite: Mark "Build hooks" as completed (skipped - not needed)

**If YES (rare):**
Ask what automations needed, then collect hook specifications.

Use SlashCommand tool to invoke hooks-create ONCE with all of them:

Build the command with marketplace flag if present:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "/domain-plugin-builder:hooks-create <hook-1> <event-1> \"<action-1>\" <hook-2> <event-2> \"<action-2>\" ... <hook-N> <event-N> \"<action-N>\" --marketplace" || echo "/domain-plugin-builder:hooks-create <hook-1> <event-1> \"<action-1>\" <hook-2> <event-2> \"<action-2>\" ... <hook-N> <event-N> \"<action-N>\""}

SlashCommand with appropriate flags based on marketplace mode.

**CRITICAL:** Pass ALL hooks in a SINGLE SlashCommand invocation. Do NOT call multiple times.

Example:
- 3 hooks: SlashCommand(/domain-plugin-builder:hooks-create pre-validation PreToolUse "Validate inputs" post-logging PostToolUse "Log tool usage" session-init SessionStart "Initialize session")

Wait for the command to complete (hooks-create handles parallel execution internally)

Update TodoWrite: Mark "Build hooks" as completed

Phase 8: Update Marketplace Configuration

Run marketplace sync script:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/sync-marketplace.sh}

This registers the plugin in marketplace.json

Update TodoWrite: Mark "Update marketplace.json" as completed

Phase 9: Register in Settings

Read current settings and add plugin commands:

@~/.claude/settings.local.json

List plugin commands:

!{bash ls $BASE_PATH/commands/*.md 2>/dev/null | sed 's|plugins/||; s|/commands/|:|; s|.md||'}

Add to settings.local.json permissions.allow array:
- "SlashCommand(/$ARGUMENTS:*)"

Use Edit tool to insert after last plugin entry.

Update TodoWrite: Mark "Update settings.json" as completed

Phase 10: Run Comprehensive Validation

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

Phase 11: Git Commit and Push

Stage all plugin files:

!{bash git add $BASE_PATH .claude/marketplace.json ~/.claude/settings.local.json}

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

Phase 12: Display Summary

Count components:

!{bash ls $BASE_PATH/commands/ 2>/dev/null | wc -l}
!{bash ls $BASE_PATH/agents/ 2>/dev/null | wc -l}
!{bash ls -d $BASE_PATH/skills/*/ 2>/dev/null | wc -l}

Display:

**Plugin Built:** $PLUGIN_NAME
**Mode:** $BASE_PATH (marketplace mode if "plugins/", standalone if ".")
**Location:** $BASE_PATH

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
