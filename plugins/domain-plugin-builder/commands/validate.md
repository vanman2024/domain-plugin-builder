---
description: Validate plugin structure and compliance using plugin-validator agent
argument-hint: <plugin-name>
---

---
🚨 **EXECUTION NOTICE FOR CLAUDE**

When you invoke this command via `SlashCommand(/domain-plugin-builder:validate ...)`, the system returns THESE INSTRUCTIONS below.

**YOU are the executor. This is NOT an autonomous subprocess.**

- ✅ The phases below are YOUR execution checklist
- ✅ YOU must run each phase immediately using tools (Bash, Read, Write, Edit, TodoWrite)
- ✅ Complete ALL phases before considering this command done
- ❌ DON'T wait for "the command to complete" - YOU complete it by executing the phases
- ❌ DON'T treat this as status output - it IS your instruction set

**Immediately after SlashCommand returns, start executing Phase 0, then Phase 1, etc.**

See `@CLAUDE.md` section "SlashCommand Execution - YOU Are The Executor" for detailed explanation.

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

Goal: Validate that a Claude Code plugin is properly structured, follows framework conventions, and is ready for deployment.

**CRITICAL EXECUTION INSTRUCTIONS:**
- DO NOT wait for phases to run automatically
- DO NOT just explain what the phases do
- EXECUTE each phase immediately using the actual tools (Bash, TodoWrite, Task)
- The `!{tool command}` syntax shows you WHAT to execute - use the real tool to DO IT
- Complete all phases in order before finishing

Core Principles:
- Invoke plugin-validator agent for comprehensive validation
- Agent runs all validation scripts internally
- Report validation results clearly

Phase 0: Create Todo List

Create todo list for all phases below.

Phase 1: Verify Plugin Exists and Determine Mode

Check if we're in a plugin directory or need to look in plugins/:

!{bash test -f .claude-plugin/plugin.json && echo "standalone" || (test -d "plugins/$ARGUMENTS" && echo "marketplace" || echo "not-found")}

Store mode:
- If "standalone": PLUGIN_PATH="." (current directory is the plugin)
- If "marketplace": PLUGIN_PATH="plugins/$ARGUMENTS"
- If "not-found": Display error and exit

If not found, display error:
- "Plugin not found. Either:"
- "  1. Run from inside plugin directory (with .claude-plugin/plugin.json)"
- "  2. Run from marketplace root with plugin name as argument"

Phase 2: Invoke Plugin Validator Agent

Launch the plugin-validator agent to perform comprehensive validation:

Task(description="Validate plugin structure and compliance", subagent_type="domain-plugin-builder:plugin-validator", prompt="You are the plugin-validator agent. Perform comprehensive validation on $PLUGIN_PATH.

Run all validation scripts:
- validate-plugin.sh for structure
- validate-command.sh for each command
- validate-agent.sh for each agent
- validate-plugin-manifest.sh for plugin.json

Verify:
- Directory structure compliance
- All agents follow framework conventions
- All commands follow pattern templates
- All skills have required directories
- Tool formatting (no JSON arrays, no wildcards)
- Line count limits (agents <300, commands <150)
- Plugin manifest correctness
- Documentation completeness

Deliverable: Complete validation report with pass/fail status, critical issues, warnings, and recommendations.")

Phase 3: Summary

Display validation completion message:

**Validation Complete for:** $ARGUMENTS

See detailed report above from plugin-validator agent.

If validation passed, next steps:
- Plugin is ready for use
- Commit changes if modifications were made
- Push to GitHub: !{bash git push origin master}

If validation failed:
- Review critical issues in report
- Fix issues identified
- Re-run validation: /domain-plugin-builder:validate $ARGUMENTS
