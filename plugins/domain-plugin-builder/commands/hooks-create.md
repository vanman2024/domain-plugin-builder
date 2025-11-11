---
description: Create hook(s) following standardized structure - supports parallel creation for 3+ hooks
argument-hint: <hook-name> <event-type> "<action>" [--plugin=name] [--marketplace] | <hook-1> <event-1> ... [--plugin=name] [--marketplace]
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

Goal: Create properly structured hooks. For 3+ hooks, creates them in parallel for faster execution.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite, Task)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Phase 0: Create Todo List

!{TodoWrite [
  {"content": "Load architectural framework", "status": "pending", "activeForm": "Loading architectural framework"},
  {"content": "Parse arguments and determine plugin", "status": "pending", "activeForm": "Parsing arguments and determining plugin"},
  {"content": "Load hooks documentation", "status": "pending", "activeForm": "Loading hooks documentation"},
  {"content": "Parse arguments and determine mode", "status": "pending", "activeForm": "Parsing arguments and determining mode"},
  {"content": "Create hook files", "status": "pending", "activeForm": "Creating hook files"},
  {"content": "Commit and push to git", "status": "pending", "activeForm": "Committing and pushing to git"},
  {"content": "Sync to Airtable", "status": "pending", "activeForm": "Syncing to Airtable"},
  {"content": "Run self-validation checks", "status": "pending", "activeForm": "Running self-validation checks"},
  {"content": "Display summary", "status": "pending", "activeForm": "Displaying summary"}
]}

Mark first task as in_progress before proceeding.

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  @docs/frameworks/claude/reference/component-decision-framework.md
- Load composition patterns:
  @docs/frameworks/claude/reference/dans-composition-pattern.md
- These provide critical understanding of:
  - Hooks are for event-driven automation
  - When to use hooks vs commands
  - Hook boundaries and responsibilities
  - How hooks integrate with plugin ecosystem
  - Anti-patterns to avoid

Phase 2: Parse Arguments and Determine Plugin & Mode

Parse $ARGUMENTS to extract:
- Hook names and event types
- Plugin name (from --plugin=name or detect from pwd)
- Marketplace mode (check for --marketplace flag)

If plugin not specified:

!{bash basename $(pwd)}

Determine base path based on --marketplace flag:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "plugins/$(basename $(pwd))" || echo "."}

Store as $BASE_PATH:
- If --marketplace present: BASE_PATH="plugins/$PLUGIN_NAME"
- If --marketplace absent: BASE_PATH="." (standalone plugin mode)

All subsequent file operations use $BASE_PATH instead of hardcoded "plugins/$PLUGIN_NAME"

Phase 3: Load Hooks Documentation

WebFetch: https://docs.claude.com/en/docs/claude-code/hooks-guide

This provides context on:
- Available event types and when they trigger
- Hook configuration structure
- Script patterns and best practices

Phase 4: Parse Arguments & Determine Mode

Actions:

Use bash to parse $ARGUMENTS and count how many hooks are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each hook specification:
- If count = 1: Single hook mode - extract <hook-name>, <event-type>, and "<action>"
- If count = 2: Two hooks mode - extract both sets
- If count >= 3: Multiple hooks mode - extract all sets

Execution modes:
- 1 hook: Direct creation
- 2 hooks: Sequential creation
- 3+ hooks: Parallel creation (invoke multiple hooks-builder agents)

Phase 5: Create Hooks

**Mode 1: Single Hook (1 hook)**

Task(description="Create hook", subagent_type="domain-plugin-builder:hooks-builder", prompt="You are the hooks-builder agent. Create a complete hook.

Hook name: <name-from-args>
Event type: <event-from-args>
Action: <action-from-args>
Plugin: <plugin-name>

Create hook configuration and script:
- Executable script in $BASE_PATH/scripts/
- Hook entry in $BASE_PATH/hooks/hooks.json
- Documentation in $BASE_PATH/docs/hooks.md
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

Task(description="Create hook 1", subagent_type="domain-plugin-builder:hooks-builder", prompt="You are the hooks-builder agent. Create a complete hook.

Hook name: $HOOK_1
Event type: $EVENT_1
Action: $ACTION_1
Plugin: $PLUGIN_NAME

Create:
- Script: $BASE_PATH/scripts/$HOOK_1.sh
- Config: Update $BASE_PATH/hooks/hooks.json
- Docs: Update $BASE_PATH/docs/hooks.md
- Use ${CLAUDE_PLUGIN_ROOT} for all paths

Deliverable: Complete hook")

Task(description="Create hook 2", subagent_type="domain-plugin-builder:hooks-builder", prompt="Create hook: $HOOK_2 - Event: $EVENT_2 [same prompt structure as hook 1 above]")

Task(description="Create hook 3", subagent_type="domain-plugin-builder:hooks-builder", prompt="Create hook: $HOOK_3 - Event: $EVENT_3 [same prompt structure as hook 1 above]")

[Continue for all N hooks requested]

Each Task() call happens in parallel. Parse $ARGUMENTS to determine how many Task() calls to make.

Wait for ALL agents to complete before proceeding.

Update TodoWrite as each completes.

Phase 5.5: Git Commit and Push
Goal: Save work immediately

Actions:
- Add all hook files to git:
  !{bash git add $BASE_PATH/hooks/ $BASE_PATH/scripts/ $BASE_PATH/docs/hooks.md}
- Commit with message:
  !{bash git commit -m "$(cat <<'EOF'
feat: Add hook(s) - HOOK_NAMES

Complete hook structure with scripts, config, and documentation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"}
- Push to GitHub: !{bash git push origin master}

Phase 5.6: Sync to Airtable
Goal: Sync created hook(s) to Airtable immediately

Actions:
- Determine marketplace name from current directory:
  !{bash pwd | grep -oE '(dev-lifecycle-marketplace|ai-dev-marketplace|mcp-servers-marketplace|domain-plugin-builder)' | head -1}
- For each created hook, sync to Airtable:
  !{bash python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py --type=hook --name=<hook-name> --plugin=<plugin-name> --marketplace=<marketplace-name> --event-type=<event-type> --script-path=<full-path-to-script>}

**Environment Requirement:**
- Requires AIRTABLE_TOKEN environment variable
- If not set, displays error message with instructions
- Sync will fail gracefully without blocking hook creation

**Note:** If multiple hooks created, sync each one sequentially.

Phase 6: Self-Validation Checklist

**CRITICAL: Verify ALL work was completed before finishing!**

Check each item and report status:

1. **Files Created:**
   Count hook scripts:
   !{bash ls -1 $BASE_PATH/scripts/*.sh 2>/dev/null | wc -l}
   Expected: <count from Phase 4>

2. **Files Exist:**
   For each hook, verify files exist:
   !{bash test -f $BASE_PATH/scripts/$HOOK_NAME.sh && echo "✅ $HOOK_NAME.sh exists" || echo "❌ $HOOK_NAME.sh MISSING"}
   !{bash test -f $BASE_PATH/hooks/hooks.json && echo "✅ hooks.json exists" || echo "❌ hooks.json MISSING"}
   !{bash test -f $BASE_PATH/docs/hooks.md && echo "✅ hooks.md exists" || echo "❌ hooks.md MISSING"}

3. **Script Executable:**
   Verify scripts are executable:
   !{bash test -x $BASE_PATH/scripts/$HOOK_NAME.sh && echo "✅ $HOOK_NAME.sh executable" || echo "❌ $HOOK_NAME.sh NOT EXECUTABLE"}

4. **Hook Configuration:**
   Verify hook is registered in hooks.json:
   !{bash grep "$HOOK_NAME" $BASE_PATH/hooks/hooks.json && echo "✅ Hook configured" || echo "❌ Hook NOT CONFIGURED"}

5. **Git Committed:**
   Verify files are committed:
   !{bash git log -1 --name-only | grep -E "(hooks/|scripts/)" && echo "✅ Committed" || echo "❌ NOT COMMITTED"}

6. **Git Pushed:**
   Verify push succeeded:
   !{bash git status | grep "up to date" && echo "✅ Pushed" || echo "❌ NOT PUSHED"}

7. **Airtable Sync:**
   Check sync was attempted for each hook

8. **Todo List Complete:**
   Mark all todos as completed:
   !{TodoWrite [all todos with status: "completed"]}

**If ANY check fails:**
- Stop immediately
- Report what's missing
- Fix the issue before proceeding
- Re-run this validation phase

**Only proceed to Phase 7 if ALL checks pass!**

Phase 7: Summary
Goal: Report results

Actions:
- Display results:

**Hooks Created:** <count>
**Plugin:** <plugin-name>
**Mode:** $BASE_PATH (marketplace mode if "plugins/", standalone if ".")
**Location:** $BASE_PATH/hooks/

**Hooks:**
- <hook-1-name> (Event: <event-1>) - <action-1> ✅
- <hook-2-name> (Event: <event-2>) - <action-2> ✅
- etc.

**Validation:** All passed ✅
**Git Status:** Committed and pushed ✅
**Airtable Sync:** Attempted ✅

**Next Steps:**
- Test hooks by triggering events
- Review scripts for correctness
- Monitor hook execution in logs
