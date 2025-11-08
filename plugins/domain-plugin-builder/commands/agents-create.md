---
allowed-tools: Task, Read, Write, Bash, Skill
description: Create agent(s) using templates - supports parallel creation for 3+ agents
argument-hint: <agent-name> "<description>" | <agent-1> "<desc-1>" <agent-2> "<desc-2>" ...
---

## Security Requirements

**CRITICAL:** All generated files must follow security rules:

@docs/security/SECURITY-RULES.md

**Key requirements:**
- Never hardcode API keys or secrets
- Use placeholders: `your_service_key_here`
- Protect `.env` files with `.gitignore`
- Create `.env.example` with placeholders only
- Document key acquisition for users

**Arguments**: $ARGUMENTS

Goal: Create properly structured agent file(s) following framework templates. For 3+ agents, creates them in parallel for faster execution.

Core Principles:
- Study templates before generating
- Keep agents concise using WebFetch (not embedding docs)
- Match complexity to task (simple vs complex)
- Validate line count and structure
- Use parallel execution for 3+ agents

Phase 1: Load Architectural Framework

Actions:
- Load component decision guidance:
  @docs/frameworks/claude/reference/component-decision-framework.md
- Load composition patterns:
  @docs/frameworks/claude/reference/dans-composition-pattern.md
- These provide critical understanding of:
  - Agents are for complex multi-step workflows with decision-making
  - When to use agents vs commands vs skills
  - Agent boundaries and responsibilities
  - How agents use skills and commands
  - Anti-patterns to avoid

Phase 2: Parse Arguments & Count Agents
Goal: Extract agent specifications and determine execution mode

Actions:

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
!{Write plugins/$PLUGIN_NAME/agents/$AGENT_NAME.md}

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
!{Bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh plugins/$PLUGIN_NAME/agents/$AGENT_NAME.md}

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

Create agent file at: plugins/$PLUGIN_NAME/agents/$AGENT_1_NAME.md
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
!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh plugins/$PLUGIN_NAME/agents/$AGENT_NAME.md}

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

Phase 8: Summary
Goal: Report results

Actions:
- Display results for all agents (names, locations, line counts, validation status)
- Show git status (committed and pushed)
- Show next steps for using the agents
- If multiple agents created, list all successfully created agents
