---
description: Create agent(s) using templates - supports parallel creation for 3+ agents
argument-hint: <agent-name> "<description>" [--marketplace] | <agent-1> "<desc-1>" <agent-2> "<desc-2>" ... [--marketplace]
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

Goal: Create properly structured agent file(s) following framework templates. For 3+ agents, creates them in parallel for faster execution.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite, Task)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Core Principles:
- Study templates before generating
- Keep agents concise using WebFetch (not embedding docs)
- Match complexity to task (simple vs complex)
- Validate line count and structure
- Use parallel execution for 3+ agents

Phase 0: Create Todo List

!{TodoWrite [
  {"content": "Load architectural framework", "status": "pending", "activeForm": "Loading architectural framework"},
  {"content": "Parse arguments and count agents", "status": "pending", "activeForm": "Parsing arguments and counting agents"},
  {"content": "Determine execution mode", "status": "pending", "activeForm": "Determining execution mode"},
  {"content": "Load agent templates", "status": "pending", "activeForm": "Loading agent templates"},
  {"content": "Create agent files", "status": "pending", "activeForm": "Creating agent files"},
  {"content": "Validate all agents", "status": "pending", "activeForm": "Validating all agents"},
  {"content": "Sync to Airtable", "status": "pending", "activeForm": "Syncing to Airtable"},
  {"content": "Display summary", "status": "pending", "activeForm": "Displaying summary"}
]}

Mark first task as in_progress before proceeding.

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- Load composition patterns:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/dans-composition-pattern.md}
- These provide critical understanding of:
  - Agents are for complex multi-step workflows with decision-making
  - When to use agents vs commands vs skills
  - Agent boundaries and responsibilities
  - How agents use skills and commands
  - Anti-patterns to avoid

Phase 2: Parse Arguments, Determine Mode & Count Agents
Goal: Extract agent specifications, determine mode, and execution strategy

Actions:

Parse $ARGUMENTS to extract:
- Agent names and descriptions
- Plugin name (from context or pwd)
- Marketplace mode (check for --marketplace flag)

If plugin not specified:

!{bash basename $(pwd)}

Determine base path based on --marketplace flag:

!{bash echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "plugins/$(basename $(pwd))" || echo "."}

Store as $BASE_PATH:
- If --marketplace present: BASE_PATH="plugins/$PLUGIN_NAME"
- If --marketplace absent: BASE_PATH="." (standalone plugin mode)

All subsequent file operations use $BASE_PATH instead of hardcoded "plugins/$PLUGIN_NAME"

Use bash to parse $ARGUMENTS and count how many agents are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each agent specification:
- If count = 1: Single agent mode - extract <agent-name> and "<description>"
- If count = 2: Two agents mode - extract both <agent-N> "<desc-N>" sets
- If count >= 3: Multiple agents mode - extract all <agent-N> "<desc-N>" sets

All agents use Task tool - whether creating 1 or 10 agents.

**Note:** Agents inherit tools from parent - no need to specify tools field.

Phase 3: Load Templates
Goal: Study framework patterns

Actions:

Load agent template immediately:
!{Read @agent-with-phased-webfetch.md}

Determine plugin location from context (default: domain-plugin-builder)

Phase 4: Create Agent(s)
Goal: Generate agent file(s) efficiently

Actions:

**Decision: 1-2 agents = build directly, 3+ agents = use Task() for parallel**

**For 1-2 Agents:**

Build directly - execute these steps immediately:

1. Load template:
!{Read @agent-with-phased-webfetch.md}

2. Load color decision framework:
!{Read @agent-color-decision.md}

3. For each agent, create the file:
!{Write $BASE_PATH/agents/$AGENT_NAME.md}

Include:
- Frontmatter with name, description, model: inherit, color (from decision framework)
- **NO tools field** - agents inherit tools from parent
- "Available Tools & Resources" section specifying:
  - MCP servers (e.g., mcp__github, mcp__supabase)
  - Skills (e.g., Skill(plugin:skill-name))
  - Slash commands (e.g., SlashCommand(/plugin:command-name))
- Progressive WebFetch for documentation
- Keep under 300 lines

4. Validate:
!{Bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh $BASE_PATH/agents/$AGENT_NAME.md}

No need for Task() overhead when building 1-2 agents

**For 3+ Agents:**

**CRITICAL: Send ALL Task() calls in a SINGLE MESSAGE for parallel execution!**

Example for 3 agents - send all at once:

```
Task(description="Create agent 1", subagent_type="domain-plugin-builder:agents-builder", prompt="You are the agents-builder agent. Create a complete agent following framework templates.

Agent name: $AGENT_1_NAME
Description: $AGENT_1_DESC

Load templates:
- Read: plugins/domain-plugin-builder/skills/build-assistant/templates/agents/agent-with-phased-webfetch.md

Create agent file at: $BASE_PATH/agents/$AGENT_1_NAME.md
- Frontmatter with name, description, model: inherit, color (determine from description)
- **NO tools field** - agents inherit tools from parent
- Include 'Available Tools & Resources' section listing:
  - Specific MCP servers to use (e.g., mcp__github, mcp__supabase)
  - Specific skills to invoke (e.g., !{skill plugin:skill-name})
  - Specific slash commands (e.g., /plugin:command-name)
- Include progressive WebFetch for documentation
- Keep under 300 lines
- Validate with validation script

Deliverable: Complete validated agent file")

Task(description="Create agent 2", subagent_type="domain-plugin-builder:agents-builder", prompt="[Same structure with $AGENT_2_NAME, $AGENT_2_DESC]")

Task(description="Create agent 3", subagent_type="domain-plugin-builder:agents-builder", prompt="[Same structure with $AGENT_3_NAME, $AGENT_3_DESC]")

[Continue for all N agents from $ARGUMENTS]
```

**DO NOT wait between Task() calls - send them ALL together in one response!**

The agents will run in parallel automatically. Only proceed to Phase 5 after all Task() calls complete.

Phase 5: Validation and Registration

**Validate all created agents:**

For each agent:
!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh $BASE_PATH/agents/$AGENT_NAME.md}

If validation fails, read errors and fix issues.

**Note:** Agents don't need settings.json registration (only commands do).

Phase 6: Git Commit and Push
Goal: Save work immediately

Actions:
- Add all agent files to git: !{bash git add plugins/*/agents/*.md}
- Commit with message:
  !{bash git commit -m "$(cat <<'EOF'
feat: Add agent(s) - AGENT_NAMES

Complete agent structure with framework compliance.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"}
- Push to GitHub: !{bash git push origin master}

Phase 7: Sync to Airtable
Goal: Sync created agent(s) to Airtable immediately

Actions:
- For each created agent, sync to Airtable:
  !{bash python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py --type=agent --name=$AGENT_NAME --plugin=$PLUGIN_NAME --marketplace=$MARKETPLACE_NAME}

Phase 8: Self-Validation Checklist

**CRITICAL: Verify ALL work was completed before finishing!**

Check each item and report status:

1. **Files Created:**
   !{bash ls -1 $BASE_PATH/agents/*.md | wc -l}
   Expected: <count from Phase 2>

2. **Files Exist:**
   For each agent, verify file exists:
   !{bash test -f $BASE_PATH/agents/$AGENT_NAME.md && echo "✅ $AGENT_NAME.md exists" || echo "❌ $AGENT_NAME.md MISSING"}

3. **Validation Passed:**
   Re-run validation on each agent:
   !{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh $BASE_PATH/agents/$AGENT_NAME.md}
   Must show "✅ All checks passed"

4. **Git Committed:**
   Verify files are committed:
   !{bash git log -1 --name-only | grep "agents/" && echo "✅ Committed" || echo "❌ NOT COMMITTED"}

5. **Git Pushed:**
   Verify push succeeded:
   !{bash git status | grep "up to date" && echo "✅ Pushed" || echo "❌ NOT PUSHED"}

6. **Airtable Sync:**
   Check sync was attempted for each agent

7. **Todo List Complete:**
   Mark all todos as completed:
   !{TodoWrite [all todos with status: "completed"]}

**If ANY check fails:**
- Stop immediately
- Report what's missing
- Fix the issue before proceeding
- Re-run this validation phase

**Only proceed to Phase 9 if ALL checks pass!**

Phase 9: Summary
Goal: Report results

Actions:

Display results:

**Agents Created:** <count>
**Plugin:** $PLUGIN_NAME
**Mode:** $BASE_PATH (marketplace mode if "plugins/", standalone if ".")
**Location:** $BASE_PATH/agents/

**Files:**
- $AGENT_1.md - $DESC_1 ✅
- $AGENT_2.md - $DESC_2 ✅
- etc.

**Validation:** All passed ✅
**Git Status:** Committed and pushed ✅
**Airtable Sync:** Attempted ✅

**Next Steps:**
- Invoke agents via Task tool: Task(subagent_type="$PLUGIN_NAME:$AGENT_NAME")
- Use in commands and skills
- Test agent capabilities
