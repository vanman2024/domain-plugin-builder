---
description: Create basic plugin directory structure and manifest
argument-hint: <plugin-name> [--marketplace]
---

---
🚨 **EXECUTION NOTICE FOR CLAUDE**

When you invoke this command via `SlashCommand(/domain-plugin-builder:plugin-create ...)`, the system returns THESE INSTRUCTIONS below.

**YOU are the executor. This is NOT an autonomous subprocess.**

- ✅ The phases below are YOUR execution checklist
- ✅ YOU must run each phase immediately using tools (Bash, Read, Write, Edit, TodoWrite)
- ✅ Complete ALL phases before considering this command done
- ❌ DON'T wait for "the command to complete" - YOU complete it by executing the phases
- ❌ DON'T treat this as status output - it IS your instruction set

**Immediately after SlashCommand returns, start executing Phase 0, then Phase 1, etc.**

See `@CLAUDE.md` section "SlashCommand Execution - YOU Are The Executor" for detailed explanation.

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

Goal: Create the basic directory structure and plugin.json manifest for a new Claude Code plugin.

This is a simple command focused on creating the scaffold. Use /domain-plugin-builder:build-plugin for complete orchestration.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite, AskUserQuestion)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Phase 0: Create Todo List using TodoWrite tool

Create todo list for all phases below.

Phase 1: Parse Arguments and Setup Structure

Parse $ARGUMENTS to extract plugin name:

!{bash echo "$ARGUMENTS" | sed 's/--marketplace//g' | xargs}

Store as $PLUGIN_NAME.

**CRITICAL: Always create marketplace structure**

Structure to create:
```
$PLUGIN_NAME/
├── .claude-plugin/
│   └── marketplace.json    ← Marketplace manifest
└── plugins/
    └── $PLUGIN_NAME/
        ├── .claude-plugin/
        │   └── plugin.json  ← Plugin manifest
        ├── commands/
        ├── agents/
        ├── skills/
        └── ...
```

This matches domain-plugin-builder's structure exactly.

Phase 2: Gather Basic Info

Use AskUserQuestion to get:
- Plugin description (one sentence)
- Plugin type (SDK, Framework, Custom)
- Author name (default: "Plugin Developer")
- Author email (default: "noreply@example.com")
- License (default: "MIT")
- Repository URL (default: "https://github.com/username/{{PLUGIN_NAME}}")
- Homepage URL (default: "https://github.com/username/{{PLUGIN_NAME}}")

Store these values for Phase 4.

Phase 3: Create Marketplace and Plugin Directory Structure

Create marketplace root structure:

!{bash mkdir -p $PLUGIN_NAME/.claude-plugin}

Create plugin subdirectory structure:

!{bash mkdir -p $PLUGIN_NAME/plugins/$PLUGIN_NAME/.claude-plugin $PLUGIN_NAME/plugins/$PLUGIN_NAME/commands $PLUGIN_NAME/plugins/$PLUGIN_NAME/agents $PLUGIN_NAME/plugins/$PLUGIN_NAME/skills $PLUGIN_NAME/plugins/$PLUGIN_NAME/hooks $PLUGIN_NAME/plugins/$PLUGIN_NAME/scripts $PLUGIN_NAME/plugins/$PLUGIN_NAME/docs}

Result:
- Marketplace root: `$PLUGIN_NAME/.claude-plugin/`
- Plugin: `$PLUGIN_NAME/plugins/$PLUGIN_NAME/`

Phase 4: Create Marketplace and Plugin Files from Templates

Set template variables:
- PLUGIN_NAME=<from Phase 1>
- DESCRIPTION=<from Phase 2>
- AUTHOR_NAME=<from Phase 2>
- AUTHOR_EMAIL=<from Phase 2>
- LICENSE=<from Phase 2>
- REPOSITORY_URL=<from Phase 2>
- HOMEPAGE_URL=<from Phase 2>
- VERSION="1.0.0"
- KEYWORDS='["plugin", "claude-code"]'
- DATE=$(date +%Y-%m-%d)

**Create marketplace.json at root:**

!{bash sed "s/{{PLUGIN_NAME}}/$PLUGIN_NAME/g; s/{{DESCRIPTION}}/$DESCRIPTION/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/marketplace.json.template > $PLUGIN_NAME/.claude-plugin/marketplace.json}

**Create plugin.json in plugins subdirectory:**

Replace ALL template variables in plugin.json:

!{bash sed "s/{{PLUGIN_NAME}}/$PLUGIN_NAME/g; s/{{VERSION}}/$VERSION/g; s/{{DESCRIPTION}}/$DESCRIPTION/g; s/{{AUTHOR_NAME}}/$AUTHOR_NAME/g; s/{{AUTHOR_EMAIL}}/$AUTHOR_EMAIL/g; s/{{HOMEPAGE_URL}}/$HOMEPAGE_URL/g; s/{{REPOSITORY_URL}}/$REPOSITORY_URL/g; s/{{LICENSE}}/$LICENSE/g; s/{{KEYWORDS}}/$KEYWORDS/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/plugin.json.template > $PLUGIN_NAME/plugins/$PLUGIN_NAME/.claude-plugin/plugin.json}

**Create plugin files:**

!{bash sed "s/{{PLUGIN_NAME}}/$PLUGIN_NAME/g; s/{{DESCRIPTION}}/$DESCRIPTION/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/README.md.template > $PLUGIN_NAME/plugins/$PLUGIN_NAME/README.md}

!{bash sed "s/{{DATE}}/$DATE/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/CHANGELOG.md.template > $PLUGIN_NAME/plugins/$PLUGIN_NAME/CHANGELOG.md}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/hooks.json.template $PLUGIN_NAME/plugins/$PLUGIN_NAME/hooks/hooks.json}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/.gitignore.template $PLUGIN_NAME/plugins/$PLUGIN_NAME/.gitignore}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/mcp.json.template $PLUGIN_NAME/plugins/$PLUGIN_NAME/.mcp.json}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/LICENSE.template $PLUGIN_NAME/plugins/$PLUGIN_NAME/LICENSE}

Phase 5: Self-Validation

Run validation script to verify all work completed:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-plugin.sh $BASE_PATH}

Mark all todos complete if validation passes.

Phase 6: Summary

Display:
- Plugin created: $PLUGIN_NAME ✅
- Mode: $BASE_PATH (marketplace mode if "plugins/", standalone if ".")
- Location: $BASE_PATH
- Files created:
  - .claude-plugin/plugin.json ✅
  - hooks/hooks.json ✅
  - .gitignore ✅
  - .mcp.json ✅
  - LICENSE ✅
  - CHANGELOG.md ✅
  - README.md ✅
- Directory structure: Complete ✅
- Validation: Passed ✅
- Next steps:
  - Build components in this order:
    1. Agents first: /domain-plugin-builder:agents-create <agent-name> "description"
    2. Commands second: /domain-plugin-builder:slash-commands-create <cmd-name> "description"
    3. Skills third: /domain-plugin-builder:skills-create <skill-name> "description"
    4. Hooks last: /domain-plugin-builder:hooks-create <hook-name> <event> "action"
  - Why agents first? Commands often invoke agents, so agents must exist first
  - Validate when done: /domain-plugin-builder:validate $PLUGIN_NAME
