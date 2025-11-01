---
allowed-tools: Bash, Read, Write, AskUserQuestion
description: Create basic plugin directory structure and manifest
argument-hint: <plugin-name>
---

**Arguments**: $ARGUMENTS

Goal: Create the basic directory structure and plugin.json manifest for a new Claude Code plugin.

This is a simple command focused on creating the scaffold. Use /domain-plugin-builder:build-plugin for complete orchestration.

Phase 1: Verify Location

!{bash pwd}

Expected: domain-plugin-builder directory. If not correct, inform user.

Phase 2: Gather Basic Info

Use AskUserQuestion to get:
- Plugin description (one sentence)
- Plugin type (SDK, Framework, Custom)

Phase 3: Create Directory Structure

!{bash mkdir -p plugins/$ARGUMENTS/.claude-plugin}
!{bash mkdir -p plugins/$ARGUMENTS/commands}
!{bash mkdir -p plugins/$ARGUMENTS/agents}
!{bash mkdir -p plugins/$ARGUMENTS/skills}
!{bash mkdir -p plugins/$ARGUMENTS/hooks}
!{bash mkdir -p plugins/$ARGUMENTS/scripts}
!{bash mkdir -p plugins/$ARGUMENTS/docs}

Phase 4: Create plugin.json Manifest

Write plugins/$ARGUMENTS/.claude-plugin/plugin.json:

```json
{
  "name": "$ARGUMENTS",
  "version": "1.0.0",
  "description": "<from Phase 2>",
  "author": {
    "name": "Plugin Builder",
    "email": "builder@example.com"
  },
  "license": "MIT",
  "keywords": []
}
```

Phase 5: Create Placeholder hooks.json

Write plugins/$ARGUMENTS/hooks/hooks.json:

```json
{
  "PreToolUse": [],
  "PostToolUse": [],
  "UserPromptSubmit": [],
  "SessionStart": [],
  "SessionEnd": [],
  "PreCompact": []
}
```

This is a placeholder. Use /domain-plugin-builder:hooks-create to add hooks.

Phase 6: Create README.md

Write plugins/$ARGUMENTS/README.md with basic plugin info.

Phase 7: Summary

Display:
- Plugin created: $ARGUMENTS
- Location: plugins/$ARGUMENTS
- Next steps: Use /domain-plugin-builder:build-plugin $ARGUMENTS to add components
