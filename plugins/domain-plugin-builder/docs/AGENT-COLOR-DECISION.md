# Agent Color Decision Framework

**Purpose:** Automatic color assignment based on agent's primary action

**When building an agent, the agent determines its own color using this decision tree.**

---

## Decision Tree

Ask these questions IN ORDER:

### 1. Does it CREATE/BUILD/GENERATE new files?
**→ BLUE**

Examples:
- Creates agent files → blue
- Generates components → blue
- Builds endpoints → blue
- Scaffolds projects → blue

### 2. Does it VALIDATE/CHECK/VERIFY correctness?
**→ YELLOW**

Examples:
- Validates schemas → yellow
- Checks compliance → yellow
- Audits security → yellow
- Verifies structure → yellow

### 3. Does it INTEGRATE/INSTALL/CONNECT external services?
**→ GREEN**

Examples:
- Integrates Supabase → green
- Installs packages → green
- Connects APIs → green
- Sets up services → green

### 4. Does it DESIGN/ARCHITECT/PLAN systems?
**→ PURPLE**

Examples:
- Designs schemas → purple
- Plans architecture → purple
- Creates specs → purple
- Architects systems → purple

### 5. Does it DEPLOY/PUBLISH/RELEASE to production?
**→ ORANGE**

Examples:
- Deploys apps → orange
- Publishes packages → orange
- Releases versions → orange
- Uploads to CDN → orange

### 6. Does it FIX/REFACTOR/ADJUST existing code?
**→ RED**

Examples:
- Fixes bugs → red
- Refactors code → red
- Adjusts implementations → red
- Optimizes performance → red

### 7. Does it TEST/RUN validations?
**→ PINK**

Examples:
- Runs tests → pink
- Executes test suites → pink
- Generates tests → pink
- Validates through testing → pink

### 8. Does it ANALYZE/SCAN/EXAMINE code?
**→ CYAN**

Examples:
- Analyzes performance → cyan
- Scans for issues → cyan
- Examines code → cyan
- Gathers metrics → cyan

---

## Primary Action Verbs

Use the **primary verb** in the agent's description to determine color:

| Primary Verb | Color |
|--------------|-------|
| create, build, generate, scaffold | BLUE |
| validate, verify, check, audit | YELLOW |
| integrate, install, connect, setup | GREEN |
| design, architect, plan, specify | PURPLE |
| deploy, publish, release, upload | ORANGE |
| fix, refactor, adjust, optimize | RED |
| test, run, execute | PINK |
| analyze, scan, examine, assess | CYAN |

---

## Example Decision Process

**Agent:** `database-optimizer`

**Question 1:** Does it CREATE new files?
→ No, it optimizes existing queries

**Question 6:** Does it FIX/OPTIMIZE existing code?
→ YES! It optimizes database queries

**Color:** RED ✅

---

**Agent:** `supabase-integrator`

**Question 1:** Does it CREATE new files?
→ It creates config files, but primary action is integration

**Question 3:** Does it INTEGRATE external services?
→ YES! Primary action is integrating Supabase

**Color:** GREEN ✅

---

**Agent:** `plugin-validator`

**Question 2:** Does it VALIDATE/CHECK?
→ YES! It validates plugin structure

**Color:** YELLOW ✅

---

## When Building Agents

**In agents-builder.md, use this logic:**

```markdown
Phase: Determine Color

Based on the agent's primary action:

Extract the main verb from description:
- "Use this agent to [VERB]..."

Match verb to color table:
- create/build/generate → blue
- validate/verify/check → yellow
- integrate/install/setup → green
- design/architect/plan → purple
- deploy/publish/release → orange
- fix/refactor/optimize → red
- test/run/execute → pink
- analyze/scan/examine → cyan

Assign color to frontmatter:
color: [determined-color]
```

---

## Special Cases

### Multi-Purpose Agents
If an agent does MULTIPLE things:
- Use the **PRIMARY** action (what it spends most time doing)
- If 50/50 split, prefer in this priority order:
  1. Deploy/Publish (orange) - most critical
  2. Validate/Check (yellow) - prevents issues
  3. Build/Create (blue) - core work
  4. Others

### Orchestrator Agents
If agent orchestrates OTHER agents:
- Look at what those sub-agents DO
- Use the color of the PRIMARY delegated task

---

## Validation

**plugin-validator checks:**
- Color matches agent's primary action verb
- Color is one of: blue, yellow, green, purple, orange, red, pink, cyan
- Color is not "auto" (must be explicit)

---

**Last Updated:** November 2, 2025
**Purpose:** Automatic color determination for visual consistency
**Scope:** ALL agents in ALL plugins
