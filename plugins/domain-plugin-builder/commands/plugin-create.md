---
description: Create basic plugin directory structure and manifest
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

Goal: Create the basic directory structure and plugin.json manifest for a new Claude Code plugin.

This is a simple command focused on creating the scaffold. Use /domain-plugin-builder:build-plugin for complete orchestration.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite, AskUserQuestion)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Phase 0: Create Todo List

Create todo list for all phases below.

Phase 1: Load Plugin Structure Documentation

Actions:
- Load official Claude Code plugin structure:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/plugins/claude-code-plugin-structure.md}

  **CRITICAL SECTIONS TO FOLLOW:**
  - "Plugin Structure" (lines 36-61) - Shows exact directory layout
  - "Critical: Directories are at plugin root, not inside .claude-plugin/" (line 59)

- Load marketplace structure differences:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/plugins/plugin-marketplaces.md}

  **KEY SECTION:**
  - "Plugin Installation Scoping" (lines 26-73) - Understand global vs project scoped

- Load component decision guidance:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- Load composition patterns:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/dans-composition-pattern.md}

**Understanding the Structure:**
- Standalone mode (no --marketplace): Creates structure at current directory (.)
- Marketplace mode (--marketplace): Creates structure at plugins/$PLUGIN_NAME/
- BOTH modes use IDENTICAL directory structure as defined in official docs

Phase 2: Verify Location and Parse Arguments

Parse $ARGUMENTS to extract plugin name and check for --marketplace flag:

!{bash echo "$ARGUMENTS" | sed 's/--marketplace//g' | xargs}

Store plugin name.

Determine base path based on --marketplace flag:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "plugins/$(echo "$ARGUMENTS" | sed 's/--marketplace//g' | xargs)" || echo "."}

Store as $BASE_PATH:
- If --marketplace present: BASE_PATH="plugins/$PLUGIN_NAME"
- If --marketplace absent: BASE_PATH="." (standalone plugin mode)

All subsequent file operations use $BASE_PATH instead of hardcoded "plugins/$PLUGIN_NAME"

!{bash pwd}

Expected: domain-plugin-builder directory (for marketplace mode) or project root (for standalone mode).

Phase 3: Gather Basic Info

Use AskUserQuestion to get:
- Plugin description (one sentence)
- Plugin type (SDK, Framework, Custom)

Phase 4: Create Directory Structure

Load official plugin structure to understand what to create:

!{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/plugins/claude-code-plugin-structure.md}

**Reference lines 40-56 which show the complete plugin layout:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Slash commands (optional)
├── agents/                   # Agent definitions (optional)
├── skills/                   # Agent Skills (optional)
├── hooks/                    # Hook configurations (optional)
├── .mcp.json                # MCP servers (optional)
├── scripts/                 # Utility scripts (optional)
└── README.md                # Plugin documentation
```

Create this exact structure at $BASE_PATH:

!{bash mkdir -p $BASE_PATH/.claude-plugin $BASE_PATH/commands $BASE_PATH/agents $BASE_PATH/skills $BASE_PATH/hooks $BASE_PATH/scripts $BASE_PATH/docs}

Phase 5: Create Plugin Files from Templates

Set template variables:
- PLUGIN_NAME=$ARGUMENTS
- DESCRIPTION=<from Phase 3>
- DATE=$(date +%Y-%m-%d)

Copy and customize templates:

!{bash sed "s/{{PLUGIN_NAME}}/$PLUGIN_NAME/g; s/{{DESCRIPTION}}/$DESCRIPTION/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/plugin.json.template > $BASE_PATH/.claude-plugin/plugin.json}

!{bash sed "s/{{PLUGIN_NAME}}/$PLUGIN_NAME/g; s/{{DESCRIPTION}}/$DESCRIPTION/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/README.md.template > $BASE_PATH/README.md}

!{bash sed "s/{{DATE}}/$DATE/g" ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/CHANGELOG.md.template > $BASE_PATH/CHANGELOG.md}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/hooks.json.template $BASE_PATH/hooks/hooks.json}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/.gitignore.template $BASE_PATH/.gitignore}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/mcp.json.template $BASE_PATH/.mcp.json}

!{bash cp ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/plugins/LICENSE.template $BASE_PATH/LICENSE}

Phase 6: Update Marketplace Registration

```
MIT License

Copyright (c) 2025 Plugin Builder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Phase 11: Self-Validation

Run validation script to verify all work completed:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-plugin.sh $BASE_PATH}

Mark all todos complete if validation passes.

Phase 12: Summary

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
  - Marketplace mode: Use /domain-plugin-builder:build-plugin $PLUGIN_NAME to add components
  - Standalone mode: Add components directly to current directory
