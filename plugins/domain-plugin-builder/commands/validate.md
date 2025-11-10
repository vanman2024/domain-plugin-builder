---
description: Validate plugin structure and compliance using plugin-validator agent
argument-hint: <plugin-name>
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

!{TodoWrite [
  {"content": "Verify plugin exists", "status": "pending", "activeForm": "Verifying plugin exists"},
  {"content": "Invoke plugin validator agent", "status": "pending", "activeForm": "Invoking plugin validator agent"},
  {"content": "Display validation results", "status": "pending", "activeForm": "Displaying validation results"}
]}

Mark first task as in_progress before proceeding.

Phase 1: Verify Plugin Exists

Check if plugin directory exists:

!{bash test -d "plugins/$ARGUMENTS" && echo "Found" || echo "Not found"}

If not found, display error:
- "Plugin 'plugins/$ARGUMENTS' not found"
- "Available plugins: !{bash ls -d plugins/*/ | sed 's|plugins/||; s|/||'}"

Phase 2: Invoke Plugin Validator Agent

Launch the plugin-validator agent to perform comprehensive validation:

Task(description="Validate plugin structure and compliance", subagent_type="domain-plugin-builder:plugin-validator", prompt="You are the plugin-validator agent. Perform comprehensive validation on plugins/$ARGUMENTS.

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
