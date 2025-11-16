---
description: Create agent(s) using templates - supports parallel creation for 3+ agents
argument-hint: <agent-name> "<description>" [--marketplace] | <agent-1> "<desc-1>" <agent-2> "<desc-2>" ... [--marketplace]
allowed-tools: Task, Read, Write, Edit, Bash, Glob, Grep, TodoWrite
---

**Arguments**: $ARGUMENTS

**Security**: Follow @~/.claude/plugins/marketplaces/dev-lifecycle-marketplace/docs/security/SECURITY-RULES.md (never hardcode API keys)

**Framework**: Load @component-decision-framework.md and @dans-composition-pattern.md

**Goal**: Create properly structured agent file(s). For 3+ agents, use parallel execution.

**EXECUTE each phase immediately** using actual tools (Bash, Read, Write, Task, TodoWrite). Complete all phases in order.

Phase 0: Create Todo List

Create todo list for all phases below.

Phase 1: Parse Arguments, Determine Mode & Count Agents
Goal: Extract agent specifications, determine mode, and execution strategy

Actions:

Parse $ARGUMENTS to extract:
- Agent names and descriptions
- Plugin name (from context or pwd)
- Marketplace mode (check for --marketplace flag)

If plugin not specified:

!{bash basename $(pwd)}

Determine base path - check if already in a plugin directory:

!{bash test -f .claude-plugin/plugin.json && echo "." || (echo "$ARGUMENTS" | grep -q "\-\-marketplace" && echo "plugins/$(basename $(pwd))" || echo ".")}

Store as $BASE_PATH:
- If .claude-plugin/plugin.json exists: BASE_PATH="." (already in plugin directory)
- Else if --marketplace present: BASE_PATH="plugins/$PLUGIN_NAME"
- Else: BASE_PATH="." (standalone plugin mode)

All subsequent file operations use $BASE_PATH instead of hardcoded "plugins/$PLUGIN_NAME"

Use bash to parse $ARGUMENTS and count how many agents are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each agent specification:
- If count = 1: Single agent mode - extract <agent-name> and "<description>"
- If count = 2: Two agents mode - extract both <agent-N> "<desc-N>" sets
- If count >= 3: Multiple agents mode - extract all <agent-N> "<desc-N>" sets

All agents use Task tool - whether creating 1 or 10 agents.

**Note:** Agents inherit tools from parent - no need to specify tools field.

Phase 2: Load Templates
Goal: Study framework patterns

Actions:

Load agent template immediately:
!{Read @agent-with-phased-webfetch.md}

Determine plugin location from context (default: domain-plugin-builder)

Phase 3: Create Agent(s)
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

For each agent, create a Task() call with subagent_type="domain-plugin-builder:agents-builder" that includes:
- Agent name and description
- Instructions to load templates from build-assistant/templates/agents/
- File path: $BASE_PATH/agents/{agent-name}.md
- Frontmatter: name, description, model: inherit, color (from agent-color-decision.md)
- **NO tools field** - agents inherit from parent
- Available Tools & Resources section (MCP servers, skills, slash commands)
- Progressive WebFetch for docs
- Keep under 300 lines
- Validate with validation script

**Send ALL Task() calls together in ONE message - they will execute in parallel!**

Only proceed to Phase 4 after all Task() calls complete.

Phase 4: Validation and Registration

**Validate all created agents:**

For each agent:
!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh $BASE_PATH/agents/$AGENT_NAME.md}

If validation fails, read errors and fix issues.

**Note:** Agents don't need settings.json registration (only commands do).

Phase 5: Git Commit and Push
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

Phase 6: Sync to Airtable
Goal: Sync created agent(s) to Airtable immediately

Actions:

**CRITICAL: Actually execute the sync command for each agent created!**

For each agent that was created, run the Bash tool to sync to Airtable.

**You MUST execute this for EVERY agent you created in Phase 3:**

Extract the list of agent names from Phase 1 parsing, then for each agent execute:

Bash: python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py --type=agent --name={agent-name} --plugin={plugin-name} --marketplace=domain-plugin-builder

Wait for each sync to complete before proceeding to next agent.

**DO NOT skip this phase!** Airtable sync is critical for marketplace integration.

Phase 7: Self-Validation

Run validation script to verify all work completed:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh $BASE_PATH/agents/*.md}

Mark all todos complete if validation passes.

Phase 8: Summary
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
