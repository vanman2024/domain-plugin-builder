# Dan's Composition Pattern

**Source:** [Tactical Agentic Coding - Skills Are Compositional](https://www.youtube.com/watch?v=skills-composition)

**Author:** Dan (Tactical Agentic Coding YouTube Channel)

**Purpose:** Clarify when to use skills vs commands vs sub-agents, and how they compose together

---

## The Fundamental Truth

> "Everything is a prompt in the end. Tokens in, tokens out. The prompt is the fundamental unit of knowledge work."

**The Core 4:**
1. Context
2. Model
3. Prompt
4. Tools

Master these fundamentals → Master composition → Master features → Master tools

---

## The Composition Hierarchy

```
USER
  ↓
SLASH COMMAND (The Primitive)
  ↓
SKILL (Compositional Manager)
  ↓
SUB-AGENT (Parallel Execution)
  ↓
MCP SERVER (External Integration)
```

### Why This Order?

- **Slash Commands** = Closest to bare metal prompts (the primitive)
- **Skills** = Group multiple commands together (compositional)
- **Sub-agents** = Isolate and parallelize (specialized execution)
- **MCP Servers** = External data/tools (lowest level integration)

---

## Critical Rule #1: Slash Commands Are The Primitive

**Always start with a slash command.**

- If you can do the job with a command, DON'T create a skill
- Commands are reusable, testable, composable
- Commands ARE prompts (just with structure)

### Example

```bash
# Start here:
/create-worktree branch-name

# NOT here:
Skill: create-worktree  # ❌ Wrong! This is one operation
```

---

## Critical Rule #2: Skills Are Managers, Not Workers

> "If you can do the job with a sub-agent or custom slash command and it's a one-off job, DO NOT USE A SKILL. This is not what skills are for."

**Use a skill ONLY when:**
- Managing a DOMAIN (3+ related operations)
- Agents should automatically discover it
- Need reusable scripts, templates, examples

**Don't use a skill when:**
- It's a one-off task → Use a command instead
- It's a single operation → Use a command instead

### ❌ Wrong: Skill for One Operation

```
Skill: create-git-worktree
Purpose: Create a git worktree

Problem: This is ONE operation!
Should be: /create-worktree command
```

### ✅ Correct: Skill as Domain Manager

```
Skill: worktree-manager
Purpose: Manage git worktrees

Operations it handles:
  - Create worktree (via /create-worktree)
  - List worktrees (via /list-worktrees)
  - Remove worktree (via /remove-worktree)
  - Merge worktree (via /merge-worktree)
  - Stop worktree server (via /stop-worktree)

The skill MANAGES the domain, commands do the work.
```

---

## Critical Rule #3: Skills Compose Slash Commands

Dan's complaint:

> "Where's my /commands directory inside my skill?"

**Skills should invoke commands, not replace them!**

### How Skills Are Invoked (Two Ways)

**1. Agents Auto-Discover Skills:**
```markdown
# Agent automatically loads skill for context
!{skill worktree-manager}

# Skill provides knowledge, scripts, templates
# Agent uses that knowledge to accomplish task
```

**2. Slash Commands Load Skills:**
```markdown
# In /manage-worktrees command

## Load Skills

!{skill worktree-manager}

# Command now has access to worktree knowledge
```

### How Skills Invoke Commands

Once a skill is loaded, it can orchestrate slash commands:

```markdown
# In SKILL.md for worktree-manager

## When Creating a Worktree

Use the SlashCommand tool to invoke the creation command:

SlashCommand(/create-worktree branch-name)

## When Listing Worktrees

Use the SlashCommand tool:

SlashCommand(/list-worktrees)

## When Removing a Worktree

Use the SlashCommand tool:

SlashCommand(/remove-worktree worktree-name)
```

**The Flow:**
```
Agent or Command
  ↓ (invokes skill)
!{skill worktree-manager}
  ↓ (skill provides knowledge + orchestrates)
SlashCommand(/create-worktree)
  ↓ (command does actual work)
Creates worktree
```

**Skills orchestrate commands. Commands do the actual work.**

---

## Critical Rule #4: One Command → Many Skills (Reuse)

Example from real projects:

- `spec-management` skill → Used by 8 different planning commands
- `project-detection` skill → Used by 7 different foundation commands
- Skills provide knowledge, multiple commands use that knowledge

---

## When to Use Each Component

| Component | Use When | Don't Use When |
|-----------|----------|----------------|
| **Slash Command** | One-off task, user triggers explicitly, simple orchestration | Managing entire domain with multiple operations |
| **Skill** | Managing domain (3+ operations), repeat solutions, agent auto-discovers | Single operation, one-off task |
| **Sub-agent** | Parallelization needed, isolated context acceptable | Single sequential task, need to keep context |
| **MCP Server** | External API/service integration, third-party tools | Internal logic, domain management |

---

## The Progressive Approach

Dan's recommended evolution:

```
1. START: Build a slash command
   ↓
   Test it. Does it work? Is it useful?
   ↓
2. IF one-off task: KEEP as slash command ✅
   ↓
3. IF need parallelization: Move to sub-agent
   ↓
4. IF managing domain (3+ operations): Create skill that composes commands
```

### Example Evolution

**Phase 1:** Create `/create-worktree` command
```bash
/create-worktree feature-branch
```

**Phase 2:** Realize you also need:
- `/list-worktrees`
- `/remove-worktree`
- `/merge-worktree`

**Phase 3:** Create `worktree-manager` skill that:
- Provides knowledge about worktrees
- Has scripts for common operations
- Invokes the slash commands via SlashCommand tool
- Agents can auto-discover it

---

## Real-World Examples

### Example 1: Deployment

**❌ WRONG:**
```
Skill: deploy-to-vercel
Purpose: Deploy to Vercel

Problem: One operation!
```

**✅ CORRECT:**
```
Command: /deploy platform
Purpose: Deploy to any platform

AND

Skill: deployment-manager
Purpose: Manage deployments across platforms
Operations:
  - Deploy (via /deploy)
  - Rollback (via /rollback)
  - Validate (via /validate-deployment)
  - Monitor (via /monitor-health)
```

### Example 2: Database Schema

**❌ WRONG:**
```
Skill: create-schema
Purpose: Create database schema

Problem: One operation!
```

**✅ CORRECT:**
```
Command: /supabase:create-schema
Purpose: Create schema from spec

AND

Skill: schema-patterns
Purpose: Database schema knowledge
Provides:
  - Schema templates
  - Migration patterns
  - RLS policy examples
  - Validation rules

Commands like /create-schema, /validate-schema, /migrate-schema
all use the schema-patterns skill for knowledge.
```

---

## Common Mistakes to Avoid

### Mistake 1: Creating Skill for One-Off Task

```
❌ Skill: send-email
❌ Skill: create-file
❌ Skill: run-tests

✅ Command: /send-email
✅ Command: /create-file
✅ Command: /run-tests
```

### Mistake 2: Commands That Don't Compose

```
❌ Command only calls one agent, doesn't use skills

✅ Command loads skill knowledge, then delegates to agent:
   - Load skill for patterns
   - Delegate to agent for execution
   - Agent uses skill knowledge
```

### Mistake 3: Too Many Skills

If you have 20 skills but only 5 commands, something's wrong!

**Good ratio:** More commands than skills
- Example: 16 commands, 7 skills (Supabase plugin)
- Skills provide deep knowledge, commands use that knowledge

---

## Key Quotes from Dan

> "Skills offer a dedicated solution, right? An opinionated structure on how to solve repeat problems in an agent first way."

> "This is the foundation. If you master the fundamentals [prompts/commands], you'll master the compositional units, you'll master the features, and then you'll master the tools."

> "Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming."

> "Always lead with a custom slash command. When you're starting out, I always recommend you just build a prompt. Don't build a skill. Don't build a sub agent. Keep it simple."

---

## Decision Flowchart

```
Building something new?
│
├─ Is it ONE operation?
│  └─ ✅ CREATE A SLASH COMMAND
│     Test it. Ship it. Done.
│
├─ Is it 2 related operations?
│  └─ ✅ CREATE 2 SLASH COMMANDS
│     Don't make a skill yet.
│
├─ Is it 3+ related operations managing a domain?
│  └─ ✅ CREATE A SKILL + SLASH COMMANDS
│     - Commands do the work
│     - Skill provides knowledge/patterns
│     - Skill may invoke commands via SlashCommand tool
│
├─ Need to run tasks in parallel?
│  └─ ✅ USE SUB-AGENTS
│     Commands can launch sub-agents via Task tool
│
└─ Integrating external API?
   └─ ✅ CREATE MCP SERVER
      Skills/commands can use MCP tools
```

---

## Summary

**The Dan Pattern:**

1. **Commands first** - They're the primitive
2. **Skills for domains** - Only when managing 3+ operations
3. **Skills compose commands** - Not replace them
4. **Master prompts** - Everything else builds on this

**Remember:**
- Prompts/Commands = Primitive
- Skills = Compositional (group commands)
- Sub-agents = Parallelization
- MCP = External integration

**Start simple. Add complexity only when needed.**

---

## See Also

- [Component Decision Framework](./component-decision-framework.md) - Full decision guide
- [Agent Skills Architecture](./agent-skills-architecture.md) - Deep dive on skills
- [Official Claude Code Skills Docs](https://docs.claude.com/en/docs/claude-code/skills)

---

**Last Updated:** November 2, 2025
**Source:** Tactical Agentic Coding YouTube - "Skills Are Compositional"
**Purpose:** Architectural guidance for building plugins correctly
