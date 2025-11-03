# Agent Color Standard

**Purpose:** Standardize agent colors across ALL codebases for visual consistency and quick identification

**When building agents, use these colors based on agent type:**

---

## Color Scheme by Agent Type

### 🔵 Blue - Builders/Generators
**Purpose:** Create, generate, or build components

**Examples:**
- `agents-builder` - Creates agent files
- `slash-commands-builder` - Creates command files
- `skills-builder` - Creates skill directories
- `hooks-builder` - Creates hook configurations
- `component-builder` - Generates UI components
- `page-generator` - Creates Next.js pages
- `endpoint-generator` - Creates API endpoints

**Use blue when:** Agent generates/creates new files or components

---

### 🟡 Yellow - Validators/Checkers
**Purpose:** Validate, verify, check, audit

**Examples:**
- `plugin-validator` - Validates plugin structure
- `security-auditor` - Checks for vulnerabilities
- `schema-validator` - Validates database schemas
- `compliance-checker` - Audits code compliance
- `deployment-validator` - Verifies deployment readiness

**Use yellow when:** Agent checks/validates/verifies correctness

---

### 🟢 Green - Integrators/Installers
**Purpose:** Integrate services, install dependencies, connect systems

**Examples:**
- `supabase-integrator` - Integrates Supabase
- `vercel-ai-integrator` - Integrates Vercel AI SDK
- `mem0-integrator` - Integrates Mem0
- `package-installer` - Installs dependencies
- `mcp-integrator` - Integrates MCP servers

**Use green when:** Agent integrates external services or installs components

---

### 🟣 Purple - Architects/Designers
**Purpose:** Design architecture, plan systems, create specifications

**Examples:**
- `schema-architect` - Designs database schemas
- `api-architect` - Designs API structure
- `system-architect` - Plans system architecture
- `deployment-architect` - Plans deployment strategy
- `feature-analyzer` - Analyzes and designs features

**Use purple when:** Agent designs/plans/architects systems

---

### 🟠 Orange - Deployers/Publishers
**Purpose:** Deploy, publish, release to production

**Examples:**
- `deployment-deployer` - Deploys applications
- `fastmcp-deployer` - Deploys MCP servers
- `package-publisher` - Publishes packages
- `release-manager` - Manages releases
- `cdn-uploader` - Uploads to CDN

**Use orange when:** Agent deploys/publishes/releases to production

---

### 🔴 Red - Fixers/Adjusters
**Purpose:** Fix bugs, adjust code, refactor, troubleshoot

**Examples:**
- `code-refactorer` - Refactors code
- `implementation-adjuster` - Adjusts implementations
- `bug-fixer` - Fixes bugs
- `performance-optimizer` - Optimizes performance
- `migration-fixer` - Fixes migration issues

**Use red when:** Agent fixes/adjusts/refactors existing code

---

### 🩷 Pink - Testers/Runners
**Purpose:** Run tests, execute validations, perform checks

**Examples:**
- `test-generator` - Generates test suites
- `test-runner` - Executes tests
- `e2e-tester` - Runs end-to-end tests
- `api-tester` - Tests API endpoints
- `performance-tester` - Runs performance tests

**Use pink when:** Agent generates or runs tests

---

### 🔵 Cyan - Analyzers/Scanners
**Purpose:** Analyze code, scan for issues, gather metrics

**Examples:**
- `security-scanner` - Scans for security issues
- `performance-analyzer` - Analyzes performance
- `dependency-analyzer` - Analyzes dependencies
- `code-scanner` - Scans codebase
- `spec-analyzer` - Analyzes specifications

**Use cyan when:** Agent analyzes/scans/gathers information

---

## Quick Reference Table

| Color  | Agent Type           | Action Verbs                               |
|--------|----------------------|-------------------------------------------|
| Blue   | Builders/Generators  | create, generate, build, scaffold        |
| Yellow | Validators/Checkers  | validate, verify, check, audit            |
| Green  | Integrators/Install  | integrate, install, connect, setup        |
| Purple | Architects/Designers | design, architect, plan, specify          |
| Orange | Deployers/Publishers | deploy, publish, release, upload          |
| Red    | Fixers/Adjusters     | fix, refactor, adjust, optimize           |
| Pink   | Testers/Runners      | test, run, execute, validate              |
| Cyan   | Analyzers/Scanners   | analyze, scan, examine, assess            |

---

## Examples in Practice

### domain-plugin-builder
```markdown
agents-builder.md:
  color: blue        # Builds agent files

slash-commands-builder.md:
  color: blue        # Builds command files

skills-builder.md:
  color: blue        # Builds skill directories

plugin-validator.md:
  color: yellow      # Validates plugin structure
```

### supabase plugin
```markdown
supabase-architect.md:
  color: purple      # Designs database schemas

supabase-integrator.md:
  color: green       # Integrates Supabase

supabase-security-auditor.md:
  color: yellow      # Validates RLS policies

supabase-tester.md:
  color: pink        # Tests database operations
```

### deployment plugin
```markdown
deployment-detector.md:
  color: cyan        # Analyzes project for platform

deployment-deployer.md:
  color: orange      # Deploys to platforms

deployment-validator.md:
  color: yellow      # Validates deployment health
```

---

## Guidelines

1. **One color per agent** - Don't mix colors
2. **Consistent across all plugins** - Same type = same color everywhere
3. **Update this doc** - If new agent types emerge, add them here
4. **Use inherit for model** - `model: inherit` (don't specify models)
5. **Auto for most cases** - Only override when standardizing types

---

## When Building New Agents

**Ask yourself:**
- What does this agent DO? (action verb)
- Which category does that action fit?
- Use the corresponding color

**Example:**
```
Agent: database-optimizer
Action: Optimizes database queries
Category: Fixer/Adjuster
Color: Red ✅
```

---

**Last Updated:** November 2, 2025
**Purpose:** Visual consistency across all Claude Code plugins
**Scope:** ALL plugins in ALL marketplaces
