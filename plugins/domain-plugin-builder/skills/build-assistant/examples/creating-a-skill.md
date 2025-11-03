# Example: Creating a Skill

This example demonstrates how to create a skill that manages multiple related operations.

## Scenario

Creating a `deployment-manager` skill that handles deployment operations (deploy, rollback, validate, monitor).

## Important: Skill vs Command Decision

**Use a SKILL when:**
- Managing a DOMAIN with multiple related operations (3+)
- Agent should automatically invoke it
- Needs scripts, templates, and examples
- Reusable knowledge base

**Use a COMMAND when:**
- One-off task (single operation)
- User explicitly triggers it
- Simple orchestration

**For deployment:**
- ❌ One command `/deploy` → Too simple for a skill
- ✅ Skill that manages: deploy, rollback, validate, monitor → Correct!

## Command

```bash
/domain-plugin-builder:skills-create deployment-manager "Manage deployment operations including deploy, rollback, validation, and monitoring across multiple platforms"
```

## What Happens

### Phase 1: Command Creates Directory Structure
```
skills/deployment-manager/
├── SKILL.md              # Main skill documentation
├── scripts/              # Helper scripts
│   ├── deploy.sh
│   ├── rollback.sh
│   ├── validate.sh
│   └── monitor.sh
├── templates/            # Configuration templates
│   ├── vercel-config/
│   ├── railway-config/
│   └── docker-config/
└── examples/             # Usage examples
    ├── deploying-nextjs.md
    ├── rolling-back.md
    └── monitoring-health.md
```

### Phase 2: Command Generates SKILL.md

**Location**: `skills/deployment-manager/SKILL.md`

```markdown
---
name: Deployment-Manager
description: Manage deployment operations including deploy, rollback, validation, and monitoring across multiple platforms. Use when deploying applications, handling rollbacks, validating deployments, or monitoring production health.
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# Deployment Manager

This skill provides comprehensive deployment management including deployment, rollback, validation, and monitoring capabilities for Vercel, Railway, DigitalOcean, and Docker platforms.

## Instructions

### When Deploying an Application

1. **Detect platform:**
   - Run: `scripts/detect-platform.sh`
   - Identifies: Vercel (Next.js), Railway (Python/Node), DigitalOcean, or Docker

2. **Load platform template:**
   - Read: `templates/<platform>-config/`
   - Get deployment configuration patterns

3. **Validate pre-deployment:**
   - Run: `scripts/validate.sh`
   - Check: Tests pass, build succeeds, env vars set

4. **Execute deployment:**
   - Run: `scripts/deploy.sh <platform>`
   - Uses platform-specific deployment commands

5. **Monitor health:**
   - Run: `scripts/monitor.sh <deployment-url>`
   - Verify: Health endpoints, response times, error rates

### When Rolling Back a Deployment

1. **Identify deployment:**
   - List recent deployments: `scripts/list-deployments.sh`
   - Get deployment ID or version to rollback to

2. **Execute rollback:**
   - Run: `scripts/rollback.sh <deployment-id>`
   - Platform handles rollback (Vercel instant, others vary)

3. **Validate rollback:**
   - Run: `scripts/validate.sh`
   - Ensure previous version is live and healthy

### When Validating Deployment Health

1. **Run health checks:**
   - Execute: `scripts/monitor.sh <url>`
   - Check: HTTP status, response time, SSL cert

2. **Verify endpoints:**
   - Test critical API endpoints
   - Validate authentication works
   - Check database connectivity

3. **Monitor metrics:**
   - Load WebFetch for platform monitoring docs
   - Review: Error rates, latency, throughput

## Available Resources

### Scripts

- `scripts/detect-platform.sh` - Identify deployment platform from project structure
- `scripts/deploy.sh` - Platform-agnostic deployment orchestrator
- `scripts/rollback.sh` - Handle deployment rollbacks
- `scripts/validate.sh` - Pre/post deployment validation
- `scripts/monitor.sh` - Health check and monitoring

### Templates

- `templates/vercel-config/` - Vercel deployment configuration
- `templates/railway-config/` - Railway deployment setup
- `templates/docker-config/` - Docker containerization

### Examples

- `examples/deploying-nextjs.md` - Deploy Next.js app to Vercel
- `examples/rolling-back.md` - Rollback failed deployment
- `examples/monitoring-health.md` - Monitor production health

## Requirements

- Platform CLI tools installed (vercel, railway, doctl, docker)
- Environment variables configured
- Valid deployment credentials
- Network access to platform APIs

## Best Practices

1. **Always validate** before deployment
2. **Test rollback** procedure in staging first
3. **Monitor health** immediately after deployment
4. **Document changes** in changelog
5. **Use blue-green** deployments when possible

---

**Purpose**: Centralize deployment knowledge and automation
**Load when**: Deploying, rolling back, or monitoring applications
**Platforms**: Vercel, Railway, DigitalOcean, Docker
```

### Phase 3: Command Creates Scripts

**Example**: `scripts/deploy.sh`

```bash
#!/bin/bash
set -euo pipefail

PLATFORM="${1:-auto}"
PROJECT_DIR="${2:-$(pwd)}"

# Auto-detect platform if not specified
if [ "$PLATFORM" = "auto" ]; then
  PLATFORM=$(bash "$(dirname "$0")/detect-platform.sh" "$PROJECT_DIR")
fi

echo "🚀 Deploying to $PLATFORM..."

case "$PLATFORM" in
  vercel)
    cd "$PROJECT_DIR" && vercel --prod
    ;;
  railway)
    cd "$PROJECT_DIR" && railway up
    ;;
  digitalocean)
    cd "$PROJECT_DIR" && doctl apps create-deployment
    ;;
  docker)
    cd "$PROJECT_DIR" && docker-compose up -d
    ;;
  *)
    echo "❌ Unknown platform: $PLATFORM"
    exit 1
    ;;
esac

echo "✅ Deployment complete!"
```

### Phase 4: Command Creates Templates

**Example**: `templates/vercel-config/vercel.json`

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next",
  "env": {
    "DATABASE_URL": "@database-url",
    "API_KEY": "@api-key"
  }
}
```

### Phase 5: Command Creates Examples

**Example**: `examples/deploying-nextjs.md`

```markdown
# Example: Deploying Next.js to Vercel

## Scenario
Deploy a Next.js application to Vercel with proper environment variables and monitoring.

## Steps

1. Invoke the skill:
   ```markdown
   !{skill deployment-manager}
   ```

2. Agent automatically:
   - Detects platform (Vercel for Next.js)
   - Loads Vercel template configuration
   - Runs pre-deployment validation
   - Executes deployment
   - Monitors health post-deployment

## Result
- Application deployed to Vercel
- Environment variables configured
- Health checks passing
- Deployment URL provided
```

## Validation

After creation, the command runs:

```bash
bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-skill.sh plugins/deployment/skills/deployment-manager
```

### Validation Checks:
- ✅ SKILL.md exists with proper frontmatter
- ✅ Description includes "Use when" trigger context
- ✅ scripts/ directory has 3+ scripts
- ✅ templates/ directory has 2+ templates per subdirectory
- ✅ examples/ directory has 3+ examples

## Best Practices Demonstrated

1. **Domain Management** - Skill manages entire deployment domain (not just one operation)
2. **Multiple Operations** - Handles deploy, rollback, validate, monitor
3. **Scripts for Automation** - Executable scripts for common tasks
4. **Templates for Configuration** - Reusable config patterns
5. **Examples for Learning** - Show how to use the skill

## Dan's Principle Applied

**Skills are compositional managers:**

The skill DOESN'T do the work itself. Instead:
- Scripts contain the actual deployment logic
- Templates provide configuration patterns
- Examples show usage patterns

**Commands invoke this skill:**

```markdown
/deploy → Invokes deployment-manager skill → Uses scripts/templates
/rollback → Invokes deployment-manager skill → Uses rollback script
/validate-deployment → Invokes deployment-manager skill → Uses validation script
```

## When to Use This Pattern

Create a skill when managing a DOMAIN with:
- 3+ related operations (deploy, rollback, validate, monitor)
- Reusable scripts and templates
- Multiple platforms or variations
- Knowledge that agents should auto-discover

**Don't create a skill for:**
- Single one-off operations → Use a command instead
- Simple orchestration → Use a command that delegates to agents

---

**Related Examples:**
- [Creating an Agent](./creating-an-agent.md)
- [Creating a Command](./creating-a-command.md)
- [Skills vs Commands Decision Guide](../../../docs/frameworks/claude/component-decision-framework.md)
