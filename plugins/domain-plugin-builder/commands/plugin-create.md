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

!{TodoWrite [
  {"content": "Load architectural framework", "status": "pending", "activeForm": "Loading architectural framework"},
  {"content": "Verify location", "status": "pending", "activeForm": "Verifying location"},
  {"content": "Gather basic info", "status": "pending", "activeForm": "Gathering basic info"},
  {"content": "Create directory structure", "status": "pending", "activeForm": "Creating directory structure"},
  {"content": "Create plugin manifest", "status": "pending", "activeForm": "Creating plugin manifest"},
  {"content": "Create MCP config", "status": "pending", "activeForm": "Creating MCP config"},
  {"content": "Update marketplace registration", "status": "pending", "activeForm": "Updating marketplace registration"},
  {"content": "Register commands in settings", "status": "pending", "activeForm": "Registering commands in settings"},
  {"content": "Git commit and push", "status": "pending", "activeForm": "Committing and pushing to git"},
  {"content": "Display summary", "status": "pending", "activeForm": "Displaying summary"}
]}

Mark first task as in_progress before proceeding.

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  @docs/frameworks/claude/reference/component-decision-framework.md
- Load composition patterns:
  @docs/frameworks/claude/reference/dans-composition-pattern.md
- These inform the plugin structure and component organization

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

!{bash mkdir -p $BASE_PATH/.claude-plugin}
!{bash mkdir -p $BASE_PATH/commands}
!{bash mkdir -p $BASE_PATH/agents}
!{bash mkdir -p $BASE_PATH/skills}
!{bash mkdir -p $BASE_PATH/hooks}
!{bash mkdir -p $BASE_PATH/scripts}
!{bash mkdir -p $BASE_PATH/docs}

Phase 5: Create plugin.json Manifest

Write $BASE_PATH/.claude-plugin/plugin.json:

```json
{
  "name": "$ARGUMENTS", "version": "1.0.0", "description": "<from Phase 2>", "author": {
    "name": "Plugin Builder", "email": "builder@example.com"
  }, "license": "MIT", "keywords": []
}
```

Phase 6: Create Placeholder hooks.json

Write $BASE_PATH/hooks/hooks.json:

```json
{
  "PreToolUse": [], "PostToolUse": [], "UserPromptSubmit": [], "SessionStart": [], "SessionEnd": [], "PreCompact": []
}
```

This is a placeholder. Use /domain-plugin-builder:hooks-create to add hooks.

Phase 7: Create .gitignore

Write $BASE_PATH/.gitignore:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Node.js
node_modules/
npm-debug.log
yarn-error.log

# MCP
.mcp_cache/
```

Phase 8: Create .mcp.json

Write $BASE_PATH/.mcp.json:

```json
{
  "mcpServers": {}
}
```

This is a placeholder for MCP server configurations.

Phase 9: Create LICENSE

Write $BASE_PATH/LICENSE:

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

Phase 10: Create CHANGELOG.md

Write $BASE_PATH/CHANGELOG.md:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - $(date +%Y-%m-%d)

### Added
- Initial plugin scaffold
- Plugin directory structure
- Plugin manifest (plugin.json)
```

Phase 10: Create README.md

Write $BASE_PATH/README.md with basic plugin info.

Phase 11: Self-Validation Checklist

**CRITICAL: Verify ALL work was completed before finishing!**

Check each item and report status:

1. **Plugin Directory Created:**
   !{bash test -d $BASE_PATH && echo "✅ Directory exists" || echo "❌ Directory MISSING"}

2. **Directory Structure Complete:**
   !{bash test -d $BASE_PATH/.claude-plugin && echo "✅ .claude-plugin/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/commands && echo "✅ commands/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/agents && echo "✅ agents/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/skills && echo "✅ skills/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/hooks && echo "✅ hooks/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/scripts && echo "✅ scripts/" || echo "❌ MISSING"}
   !{bash test -d $BASE_PATH/docs && echo "✅ docs/" || echo "❌ MISSING"}

3. **Plugin Manifest Exists:**
   !{bash test -f $BASE_PATH/.claude-plugin/plugin.json && echo "✅ plugin.json exists" || echo "❌ plugin.json MISSING"}

4. **Plugin Manifest Valid:**
   !{bash python3 -m json.tool $BASE_PATH/.claude-plugin/plugin.json > /dev/null 2>&1 && echo "✅ Valid JSON" || echo "❌ INVALID JSON"}

5. **MCP Config Exists:**
   !{bash test -f $BASE_PATH/.mcp.json && echo "✅ .mcp.json exists" || echo "❌ .mcp.json MISSING"}

6. **MCP Config Valid:**
   !{bash python3 -m json.tool $BASE_PATH/.mcp.json > /dev/null 2>&1 && echo "✅ Valid JSON" || echo "❌ INVALID JSON"}

7. **Marketplace Registration:**
   !{bash grep -q "$PLUGIN_NAME" .claude-plugin/marketplace.json 2>/dev/null && echo "✅ Registered in marketplace.json" || echo "⚠️ Not registered (OK if handled by build-plugin)"}

8. **Git Status:**
   !{bash git status $BASE_PATH}
   Check if files are tracked or committed

9. **Git Commit:**
   !{bash git log -1 --name-only | grep "$BASE_PATH" && echo "✅ Committed" || echo "⚠️ Not committed (OK if handled by build-plugin)"}

10. **Git Push:**
    !{bash git status | grep "up to date" && echo "✅ Pushed" || echo "⚠️ Not pushed (OK if handled by build-plugin)"}

11. **Todo List Complete:**
    Mark all todos as completed:
    !{TodoWrite [
      {"content": "Load architectural framework", "status": "completed", "activeForm": "Loading architectural framework"},
      {"content": "Verify location", "status": "completed", "activeForm": "Verifying location"},
      {"content": "Gather basic info", "status": "completed", "activeForm": "Gathering basic info"},
      {"content": "Create directory structure", "status": "completed", "activeForm": "Creating directory structure"},
      {"content": "Create plugin manifest", "status": "completed", "activeForm": "Creating plugin manifest"},
      {"content": "Create MCP config", "status": "completed", "activeForm": "Creating MCP config"},
      {"content": "Update marketplace registration", "status": "completed", "activeForm": "Updating marketplace registration"},
      {"content": "Register commands in settings", "status": "completed", "activeForm": "Registering commands in settings"},
      {"content": "Git commit and push", "status": "completed", "activeForm": "Committing and pushing to git"},
      {"content": "Display summary", "status": "completed", "activeForm": "Displaying summary"}
    ]}

**If ANY critical check fails (items 1-6):**
- Stop immediately
- Report what's missing
- Fix the issue before proceeding
- Re-run this validation phase

**If git checks fail (items 8-10):**
- These may be OK if plugin-create is called from build-plugin
- build-plugin handles git workflow after all components added

**Only proceed to Phase 12 if ALL critical checks pass!**

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
