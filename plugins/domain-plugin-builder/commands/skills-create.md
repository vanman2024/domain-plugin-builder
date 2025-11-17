---
description: Create new skill(s) using skills-builder agent - analyzes plugin structure or accepts direct specifications (supports parallel creation)
argument-hint: [--analyze <plugin-name>] | [<skill-name> "<description>"] | [<skill-1> "<desc-1>" <skill-2> "<desc-2>" ...] [--marketplace]
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

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, Read, Write, Edit, TodoWrite, Task)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Phase 0: Create Todo List

Create todo list for all phases below.

Phase 1: Discovery & Architecture Decision Framework
Goal: Load comprehensive component decision framework to understand WHEN to use skills vs commands vs agents vs hooks vs MCP

Actions:
- Load the complete component decision framework:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
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

Parse $ARGUMENTS to extract:
- Skill names and descriptions
- Plugin name (from --plugin=name or detect from pwd)
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

Use bash to parse $ARGUMENTS and count how many skills are being requested:

!{bash echo "$ARGUMENTS" | grep -oE '<[^>]+>' | wc -l}

Store the count. Then extract each skill specification:
- If count = 0 and --analyze present: Set mode to "analyze", extract plugin name
- If count = 1: Single skill mode - extract <skill-name> and "<description>"
- If count >= 2: Multiple skills mode - extract all <skill-N> "<desc-N>" pairs

Phase 3: Launch Skills Builder Agent(s)

Actions:

**For --analyze mode:**

Task(description="Analyze plugin for needed skills", subagent_type="domain-plugin-builder:skills-builder", prompt="You are the skills-builder agent. Analyze the plugin structure at $BASE_PATH to determine what skills are needed.

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

Plugin: $BASE_PATH
Deliverable: List of recommended skills with descriptions")

**Decision: 1-2 skills = build directly, 3+ skills = use Task() for parallel**

**For 1-2 Skills:**

Build directly - execute these steps immediately:

1. Load decision framework:
!{Read @component-decision-framework.md}

2. Load skill template:
!{Read @SKILL.md.template}

3. For each skill:
!{Bash mkdir -p $BASE_PATH/skills/$SKILL_NAME/{scripts,templates,examples}}

!{Write $BASE_PATH/skills/$SKILL_NAME/SKILL.md}

Create scripts, templates, and examples as needed.

4. Validate:
!{Bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh $BASE_PATH/skills/$SKILL_NAME}

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
!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh $BASE_PATH/skills/$SKILL_NAME}

If validation fails, read errors and fix issues.

Phase 5: Sync to Airtable

**Use bulk sync script for efficiency:**

Bash: python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/bulk-sync-airtable.py --plugin={plugin-name} --marketplace={marketplace-name} --type=skills

This syncs ALL skills in parallel instead of one at a time.

**Environment Requirement:**
- Requires AIRTABLE_TOKEN environment variable
- If not set, displays error message with instructions

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

Phase 8: Self-Validation

Run validation script to verify all work completed:

!{bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh $BASE_PATH/skills/*}

Mark all todos complete if validation passes.

Phase 9: Summary

Display results:

**Skills Created:** <count>
**Plugin:** $PLUGIN_NAME
**Mode:** $BASE_PATH (marketplace mode if "plugins/", standalone if ".")
**Location:** $BASE_PATH/skills/

**Files:**
- $SKILL_1/ - $DESC_1 ✅
- $SKILL_2/ - $DESC_2 ✅
- etc.

**Validation:** All passed ✅
**Registration:** Complete ✅
**Airtable Sync:** Attempted ✅
**Git:** Committed and pushed ✅

**Next Steps:**
- Invoke skills: Skill($PLUGIN_NAME:$SKILL_NAME)
- Test skill functionality
- Update documentation
