---
allowed-tools: Task, Read, Write, Bash, Skill
description: Create agent(s) using templates - supports parallel creation for 3+ agents
argument-hint: <agent-name> "<description>" "<tools>" | <agent-1> "<desc-1>" "<tools-1>" <agent-2> "<desc-2>" "<tools-2>" ...
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

Phase 1: Parse Arguments & Count Agents
Goal: Extract agent specifications and determine execution mode

Actions:

Use bash to parse $ARGUMENTS and count how many agents are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each agent specification:
- If count = 1: Single agent mode - extract <agent-name>, "<description>", and "<tools>"
- If count = 2: Two agents mode - extract both <agent-N> "<desc-N>" "<tools-N>" sets
- If count >= 3: Multiple agents mode - extract all <agent-N> "<desc-N>" "<tools-N>" sets

All agents use Task tool - whether creating 1 or 10 agents.

Phase 2: Load Templates
Goal: Study framework patterns

Actions:
- Load agent template:
  - @agent-with-phased-webfetch.md
- Determine plugin location from context (default: domain-plugin-builder)

Phase 3: Create Agent(s)
Goal: Generate agent file(s) using Task() calls - works for 1 or multiple agents

Actions:

**For Single Agent:**

Task(description="Create agent", subagent_type="domain-plugin-builder:agents-builder", prompt="You are the agents-builder agent. Create a complete agent following framework templates.

Agent name: $AGENT_NAME
Description: $DESCRIPTION
Tools: $TOOLS

Load templates:
- Read: plugins/domain-plugin-builder/skills/build-assistant/templates/agents/agent-with-phased-webfetch.md

Create agent file at: plugins/$PLUGIN_NAME/agents/$AGENT_NAME.md
- Frontmatter with name, description, model: inherit, color (determine from description), tools
- Include progressive WebFetch for documentation
- Keep under 300 lines
- Validate with validation script

Deliverable: Complete validated agent file")

**For Multiple Agents (2+):**

**CRITICAL: Send ALL Task() calls in a SINGLE MESSAGE for parallel execution!**

Example for 3 agents - send all at once:

```
Task(description="Create agent 1", subagent_type="domain-plugin-builder:agents-builder", prompt="You are the agents-builder agent. Create a complete agent following framework templates.

Agent name: $AGENT_1_NAME
Description: $AGENT_1_DESC
Tools: $AGENT_1_TOOLS

Load templates:
- Read: plugins/domain-plugin-builder/skills/build-assistant/templates/agents/agent-with-phased-webfetch.md

Create agent file at: plugins/$PLUGIN_NAME/agents/$AGENT_1_NAME.md
- Frontmatter with name, description, model: inherit, color (determine from description), tools
- Include progressive WebFetch for documentation
- Keep under 300 lines
- Validate with validation script

Deliverable: Complete validated agent file")

Task(description="Create agent 2", subagent_type="domain-plugin-builder:agents-builder", prompt="[Same structure with $AGENT_2_NAME, $AGENT_2_DESC, $AGENT_2_TOOLS]")

Task(description="Create agent 3", subagent_type="domain-plugin-builder:agents-builder", prompt="[Same structure with $AGENT_3_NAME, $AGENT_3_DESC, $AGENT_3_TOOLS]")

[Continue for all N agents from $ARGUMENTS]
```

**DO NOT wait between Task() calls - send them ALL together in one response!**

The agents will run in parallel automatically. Only proceed to Phase 4 after all Task() calls complete.

Phase 4: Git Commit and Push
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

Phase 5: Summary
Goal: Report results

Actions:
- Display results for all agents (names, locations, line counts, validation status)
- Show git status (committed and pushed)
- Show next steps for using the agents
- If multiple agents created, list all successfully created agents
