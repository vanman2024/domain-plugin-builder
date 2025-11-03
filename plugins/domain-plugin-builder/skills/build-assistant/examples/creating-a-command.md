# Example: Creating a Slash Command

This example demonstrates how to create a slash command using the build-assistant skill.

## Scenario

Creating a `/deploy:validate` command that checks deployment readiness before pushing to production.

## Command

```bash
/domain-plugin-builder:slash-commands-create deploy:validate "Validate deployment readiness with comprehensive checks (tests, build, env vars, security)"
```

## What Happens

### Phase 1: Command Parses Arguments
The `/domain-plugin-builder:slash-commands-create` command:
1. Parses the command name: `deploy:validate`
2. Extracts description: "Validate deployment readiness..."
3. Determines plugin from context or `--plugin` flag

### Phase 2: Command Loads Template
```markdown
@~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/commands/template-command-patterns.md
```

### Phase 3: Command Creates File
For a single command, creates the file directly.

For 3+ commands, invokes `slash-commands-builder` agents in parallel.

## Generated Command File

**Location**: `plugins/deployment/commands/deploy-validate.md`

```markdown
---
allowed-tools: Task, Bash, Read, Grep, Glob, TodoWrite
description: Validate deployment readiness with comprehensive checks (tests, build, env vars, security)
argument-hint: [--skip-tests] [--skip-build]
---

**Arguments**: $ARGUMENTS

Goal: Ensure application is ready for production deployment through comprehensive validation.

## Phase 1: Create Validation Checklist

Create TodoWrite list to track all validation steps:
- Run test suite
- Verify build succeeds
- Check environment variables
- Validate security configs
- Review API endpoints

## Phase 2: Run Tests

**Skip if --skip-tests flag present**

Actions:
- Run: !{bash npm test}
- Verify all tests pass
- Check code coverage meets threshold (>80%)
- Mark todo as completed if successful

## Phase 3: Verify Build

**Skip if --skip-build flag present**

Actions:
- Run: !{bash npm run build}
- Ensure no build errors
- Verify output bundles created
- Check bundle sizes are acceptable
- Mark todo as completed if successful

## Phase 4: Environment Variable Check

Actions:
- Read .env.example
- Compare with .env
- Verify all required variables are set
- Check for placeholder values (your_key_here)
- Report any missing or incomplete variables

## Phase 5: Security Audit

Actions:
- Check for hardcoded secrets: !{bash grep -r "api_key\\|password\\|secret" src/}
- Verify HTTPS configuration
- Review CORS settings
- Check authentication implementation
- Scan dependencies for vulnerabilities: !{bash npm audit}

## Phase 6: API Endpoint Validation

Actions:
- List all API endpoints
- Verify authentication on protected routes
- Check rate limiting configuration
- Validate request/response schemas

## Success Criteria

All validation steps pass:
- ✅ Tests passing
- ✅ Build successful
- ✅ Environment variables complete
- ✅ No security issues found
- ✅ API endpoints validated

If any step fails, provide clear remediation steps.

## Notes

- Use --skip-tests for quick pre-commit checks
- Use --skip-build when only validating configuration
- Always run full validation before production deployment
```

## Validation

After creation, the command runs:

```bash
bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-command.sh plugins/deployment/commands/deploy-validate.md
```

### Validation Checks:
- ✅ Frontmatter contains: allowed-tools, description, argument-hint
- ✅ Uses TodoWrite for task tracking
- ✅ Has clear phases with actions
- ✅ Includes success criteria
- ✅ Tools are comma-separated (not JSON array)

## Best Practices Demonstrated

1. **TodoWrite for Tracking** - Command creates checklist of validation steps
2. **Phased Execution** - Clear phases with specific actions
3. **Argument Handling** - Supports optional flags (--skip-tests, --skip-build)
4. **Success Criteria** - Defines what "done" means
5. **Proper Tools** - Includes Task, Bash, Read, TodoWrite (not just Task!)

## Command Pattern Used

**Pattern 2: Single Agent** (if needed)

This command uses direct bash execution. If it needed AI analysis, it would use:

```markdown
Task(description="Analyze security issues",
     subagent_type="security-auditor",
     prompt="Review codebase for security vulnerabilities...")
```

## When to Use This Pattern

Use this pattern when creating commands that:
- Orchestrate multiple validation steps
- Need to track progress with TodoWrite
- Run deterministic checks (tests, builds, scans)
- Provide clear pass/fail criteria
- Support optional flags for flexibility

---

**Related Examples:**
- [Creating an Agent](./creating-an-agent.md)
- [Creating a Skill](./creating-a-skill.md)
- [Using Multiple Agents in Parallel](./parallel-agents-pattern.md)
