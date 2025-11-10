---
description: Create new skill(s) using skills-builder agent - analyzes plugin structure or accepts direct specifications (supports parallel creation)
argument-hint: [--analyze <plugin-name>] | [<skill-name> "<description>"] | [<skill-1> "<desc-1>" <skill-2> "<desc-2>" ...]
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

Goal: Create properly structured skill(s) by launching the skills-builder agent

Phase 0: Create Todo List

!{TodoWrite [
  {"content": "Load architecture decision framework", "status": "pending", "activeForm": "Loading architecture decision framework"},
  {"content": "Parse arguments and determine mode", "status": "pending", "activeForm": "Parsing arguments and determining mode"},
  {"content": "Launch skills-builder agent", "status": "pending", "activeForm": "Launching skills-builder agent"},
  {"content": "Validate created skills", "status": "pending", "activeForm": "Validating created skills"},
  {"content": "Sync to Airtable", "status": "pending", "activeForm": "Syncing to Airtable"},
  {"content": "Display summary", "status": "pending", "activeForm": "Displaying summary"}
]}

Mark first task as in_progress before proceeding.

Phase 1: Discovery & Architecture Decision Framework
Goal: Load comprehensive component decision framework to understand WHEN to use skills vs commands vs agents vs hooks vs MCP

Actions:
- Load the complete component decision framework:
  @component-decision-framework.md
- This provides critical understanding of:
  - 🚨 START WITH COMMANDS FIRST (not skills!)
  - Commands are the primitive (closest to prompts)
  - Skills are for MANAGING multiple related commands
  - The "One-Off vs Management" test
  - When NOT to create a skill
  - Real composition hierarchy (skills use commands, not vice versa)
  - Complete decision tree with real examples
  - Anti-patterns to avoid
- This architectural decision-making context will be passed to the skills-builder agent
- Agent will understand when the requested functionality should be a COMMAND instead of a skill

Phase 2: Parse Arguments & Determine Mode

Actions:

Use bash to parse $ARGUMENTS and count how many skills are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each skill specification:
- If count = 0 and --analyze present: Set mode to "analyze", extract plugin name
- If count = 1: Single skill mode - extract <skill-name> and "<description>"
- If count >= 2: Multiple skills mode - extract all <skill-N> "<desc-N>" pairs

Phase 3: Launch Skills Builder Agent(s)

Actions:

**For --analyze mode:**

Task(description="Analyze plugin for needed skills", subagent_type="domain-plugin-builder:skills-builder", prompt="You are the skills-builder agent. Analyze the plugin structure at plugins/$PLUGIN_NAME to determine what skills are needed.

Architectural context from component-decision-framework.md:
@~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/component-decision-framework.md

Tasks:
1. Read detailed skills documentation via WebFetch:
   - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart
   - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
   - https://docs.claude.com/en/docs/claude-code/skills
   - https://docs.claude.com/en/docs/claude-code/slash-commands#skills-vs-slash-commands
   - https://github.com/anthropics/claude-cookbooks/tree/main/skills
   - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
2. Analyze plugin commands and agents
3. Identify what reusable capabilities are needed
4. Report recommended skills to create

Plugin: plugins/$PLUGIN_NAME
Deliverable: List of recommended skills with descriptions")

**Decision: 1-2 skills = build directly, 3+ skills = use Task() for parallel**

**For 1-2 Skills:**

Build directly - execute these steps immediately:

1. Load decision framework:
!{Read @component-decision-framework.md}

2. Load skill template:
!{Read @SKILL.md.template}

3. For each skill:
!{Bash mkdir -p plugins/$PLUGIN_NAME/skills/$SKILL_NAME/{scripts,templates,examples}}

!{Write plugins/$PLUGIN_NAME/skills/$SKILL_NAME/SKILL.md}

Create scripts, templates, and examples as needed.

4. Validate:
!{Bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh plugins/$PLUGIN_NAME/skills/$SKILL_NAME}

No need for Task() overhead when building 1-2 skills

**For 3+ Skills:**

Launch multiple skills-builder agents IN PARALLEL (all at once) using multiple Task() calls in ONE response:

Task(description="Create skill 1", subagent_type="domain-plugin-builder:skills-builder", prompt="Create skill: $SKILL_1 - $DESC_1 [same prompt structure as single skill above]")

Task(description="Create skill 2", subagent_type="domain-plugin-builder:skills-builder", prompt="Create skill: $SKILL_2 - $DESC_2 [same prompt structure as single skill above]")

Task(description="Create skill 3", subagent_type="domain-plugin-builder:skills-builder", prompt="Create skill: $SKILL_3 - $DESC_3 [same prompt structure as single skill above]")

[Continue for all N skills requested]

Each Task() call happens in parallel. Parse $ARGUMENTS to determine how many Task() calls to make.

Wait for ALL agents to complete before proceeding to Phase 4.

Phase 4: Validation

**Validate all created skills:**

For each skill:
!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh plugins/$PLUGIN_NAME/skills/$SKILL_NAME}

If validation fails, read errors and fix issues.

Phase 5: Sync to Airtable

**CRITICAL: Sync each skill to Airtable as source of truth!**

Actions:

Determine marketplace name from current directory:

!{bash pwd | grep -oE '(dev-lifecycle-marketplace|ai-dev-marketplace|mcp-servers-marketplace|domain-plugin-builder)' | head -1}

For each created skill, sync to Airtable:

!{bash python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py --type=skill --name=$SKILL_NAME --plugin=$PLUGIN_NAME --marketplace=$MARKETPLACE_NAME}

This:
- Extracts frontmatter from SKILL.md (name, description)
- Finds or creates Skill record in Airtable
- Links to Plugin record
- Updates Directory Path field
- Updates Has SKILL.md, Has Scripts, Has Templates, Has Examples checkboxes

**Environment Requirement:**
- Requires AIRTABLE_TOKEN environment variable
- If not set, displays error message with instructions
- Sync will fail gracefully without blocking skill creation

Phase 6: Register Skills in Settings

**CRITICAL: Skills must be registered to be usable!**

Register all created skills in ~/.claude/settings.json:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/register-skills-in-settings.sh $PLUGIN_NAME}

This registers entries like:
- Skill($PLUGIN_NAME:$SKILL_1)
- Skill($PLUGIN_NAME:$SKILL_2)
- etc.

Verify skills are accessible with Skill tool.

Phase 7: Git Commit and Push

Actions:
- Add all created skill directories to git:
  !{bash git add plugins/*/skills/*}
- Commit with descriptive message:
  !{bash git commit -m "$(cat <<'EOF'
feat: Add skill(s) - SKILL_NAMES

Complete skill structure with scripts, templates, and examples.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"}
- Push to GitHub: !{bash git push origin master}

Phase 8: Summary

Actions:
- Display results from all agents (skill names, locations, validation status)
- Show git status (committed and pushed)
- Confirm skills registered in settings.json
- Show how to invoke skills: !{skill plugin:skill-name}
- If multiple skills created, list all successfully created skills
