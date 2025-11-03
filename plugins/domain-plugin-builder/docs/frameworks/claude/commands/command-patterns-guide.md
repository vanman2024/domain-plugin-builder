# Command Patterns Guide

Complete guide to the 4 command patterns for building Claude Code slash commands.

## Overview

Commands follow 1 of 4 patterns based on complexity and execution model:

| Pattern | Use Case | Execution | Example |
|---------|----------|-----------|---------|
| **1. Simple** | Mechanical tasks, no AI | Direct bash/script | `/version`, `/git-setup` |
| **2. Single Agent** | One AI capability | Task() → 1 agent | `/detect`, `/init` |
| **3. Sequential** | Chain slash commands | SlashCommand() calls | `/build-full-stack` |
| **4. Parallel** | Independent validations | Multiple Task() at once | `/validate` |

---

## Pattern 1: Simple (No Agents)

**When to use:**
- Mechanical operations (version bumping, file operations)
- Configuration updates
- No AI decision-making needed

**Structure:**
```markdown
---
description: Short description
argument-hint: <args>
allowed-tools: Bash, Read, Write, Edit
---

Phase 1: Parse Arguments
!{bash echo "$ARGUMENTS"}

Phase 2: Execute Operation
!{bash some-command $ARGUMENTS}

Phase 3: Summary
Display results
```

**Example: Version Bump**
```markdown
Phase 1: Parse Version Type
Parse $ARGUMENTS for major/minor/patch

Phase 2: Update Version Files
!{bash sed -i 's/"version": ".*"/"version": "1.2.3"/' package.json}

Phase 3: Git Tag
!{bash git tag v1.2.3}
```

**Key Characteristics:**
- ✅ No Task() calls
- ✅ Direct bash commands
- ✅ Fast execution
- ✅ Deterministic output

---

## Pattern 2: Single Agent

**When to use:**
- One AI capability needed (analysis, generation, refactoring)
- Decision-making required
- Processing complex inputs

**Structure:**
```markdown
---
description: Short description
argument-hint: <args>
allowed-tools: Task, Read, Write, Bash
---

Phase 1: Parse Arguments
Extract parameters from $ARGUMENTS

Phase 2: Invoke Agent
Task(description="...", subagent_type="agent-name", prompt="...")

Phase 3: Validation
Validate agent output

Phase 4: Summary
Display results
```

**Example: Project Detection**
```markdown
Phase 1: Determine Project Path
PROJECT_PATH="${1:-$(pwd)}"

Phase 2: Launch Detection Agent
Task(description="Detect project stack", subagent_type="project-detector", prompt="
Analyze project at: $PROJECT_PATH
Detect:
- Framework (Next.js, FastAPI, etc.)
- Language (TypeScript, Python)
- Dependencies
Deliverable: Complete tech stack analysis
")

Phase 3: Write Results
Write detection results to .claude/project.json

Phase 4: Summary
Display detected stack
```

**Key Characteristics:**
- ✅ One Task() call
- ✅ AI-powered analysis/generation
- ✅ Clear agent responsibility
- ✅ Validation after agent completes

---

## Pattern 3: Sequential (Slash Command Chain)

**When to use:**
- Orchestrating multiple steps
- Each step is a reusable command
- Steps must run in order

**Structure:**
```markdown
---
description: Orchestrator description
argument-hint: <args>
allowed-tools: SlashCommand, TodoWrite, Bash, Read
---

Phase 1: Create Todo List
TodoWrite with all steps

Phase 2: Step 1
SlashCommand(/command-1 $ARGS)
Wait for completion
Update TodoWrite

Phase 3: Step 2
SlashCommand(/command-2 $ARGS)
Wait for completion
Update TodoWrite

Phase 4: Summary
Display results from all steps
```

**Example: Full Stack Build**
```markdown
Phase 1: Initialize
TodoWrite:
- Initialize Next.js
- Initialize FastAPI
- Setup Supabase
- Deploy

Phase 2: Frontend
SlashCommand(/nextjs-frontend:init $PROJECT_NAME)
Update TodoWrite: Mark "Initialize Next.js" as completed

Phase 3: Backend
SlashCommand(/fastapi-backend:init $PROJECT_NAME)
Update TodoWrite: Mark "Initialize FastAPI" as completed

Phase 4: Database
SlashCommand(/supabase:init-ai-app $PROJECT_NAME)
Update TodoWrite: Mark "Setup Supabase" as completed

Phase 5: Deploy
SlashCommand(/deployment:deploy $PROJECT_NAME)
Update TodoWrite: Mark "Deploy" as completed
```

**Key Characteristics:**
- ✅ Multiple SlashCommand() calls
- ✅ Sequential execution (MUST wait between each)
- ✅ TodoWrite for tracking
- ✅ Each command is independently useful

**CRITICAL RULES:**
1. **NEVER run slash commands in parallel** - they queue and don't execute
2. **ALWAYS wait for completion** before next SlashCommand()
3. **Use SlashCommand() tool**, not text

---

## Pattern 4: Parallel (Multiple Agents)

**When to use:**
- Independent validation tasks
- No dependencies between operations
- All can run simultaneously

**Structure:**
```markdown
---
description: Parallel operations
argument-hint: <args>
allowed-tools: Task, Read, Bash
---

Phase 1: Parse Arguments
Extract parameters

Phase 2: Launch Parallel Agents
**CRITICAL: Send ALL Task() calls in ONE message!**

Task(description="Task 1", subagent_type="agent-1", prompt="...")
Task(description="Task 2", subagent_type="agent-2", prompt="...")
Task(description="Task 3", subagent_type="agent-3", prompt="...")

Wait for ALL to complete

Phase 3: Aggregate Results
Collect results from all agents

Phase 4: Summary
Display combined results
```

**Example: Comprehensive Validation**
```markdown
Phase 1: Determine Plugin Path
PLUGIN_PATH="plugins/$ARGUMENTS"

Phase 2: Launch Validators (Parallel)
Send all Task() calls at once:

Task(description="Lint code", subagent_type="linter", prompt="
Lint all code in: $PLUGIN_PATH
Report style issues
")

Task(description="Run tests", subagent_type="test-runner", prompt="
Run test suite for: $PLUGIN_PATH
Report failures
")

Task(description="Security scan", subagent_type="security-scanner", prompt="
Scan for vulnerabilities in: $PLUGIN_PATH
Report security issues
")

All 3 agents run in parallel!

Phase 3: Collect Results
Aggregate results from all validators

Phase 4: Summary
Display:
- Lint: X issues
- Tests: Y failures
- Security: Z vulnerabilities
```

**Key Characteristics:**
- ✅ Multiple Task() calls in ONE message
- ✅ All agents run simultaneously
- ✅ No dependencies between agents
- ✅ Faster than sequential

**CRITICAL RULES:**
1. **ALL Task() calls in SINGLE message** - don't send separate messages
2. **No wait between Task()** - send them all together
3. **Independent agents only** - no dependencies

---

## Decision Flowchart

```
Need to build a command?
│
├─ No AI needed?
│  └─ Pattern 1: Simple
│     (bash commands, config updates)
│
├─ Need one AI capability?
│  └─ Pattern 2: Single Agent
│     (analysis, generation, refactoring)
│
├─ Orchestrating existing commands?
│  └─ Pattern 3: Sequential
│     (chain slash commands with SlashCommand())
│
└─ Independent validations/checks?
   └─ Pattern 4: Parallel
      (multiple Task() at once)
```

---

## Common Mistakes

### ❌ WRONG: Running slash commands in parallel
```markdown
SlashCommand(/command-1)
SlashCommand(/command-2)
SlashCommand(/command-3)
```
**Problem**: Commands queue up and don't execute

### ✅ CORRECT: Sequential execution
```markdown
SlashCommand(/command-1)
(Wait for completion)

SlashCommand(/command-2)
(Wait for completion)

SlashCommand(/command-3)
```

---

### ❌ WRONG: Using Task() for sequential operations
```markdown
Task(description="Step 1", ...)
(Wait)
Task(description="Step 2", ...)
```
**Problem**: Should use SlashCommand() for reusable commands

### ✅ CORRECT: Use SlashCommand for orchestration
```markdown
SlashCommand(/step-1)
SlashCommand(/step-2)
```

---

### ❌ WRONG: Waiting between parallel Task() calls
```markdown
Task(description="Agent 1", ...)
(Wait for completion)
Task(description="Agent 2", ...)
```
**Problem**: Breaks parallelism - runs sequentially

### ✅ CORRECT: All Task() in one message
```markdown
Task(description="Agent 1", ...)
Task(description="Agent 2", ...)
Task(description="Agent 3", ...)

(Now they all run in parallel!)
```

---

## Pattern Selection Matrix

| Criteria | Simple | Single Agent | Sequential | Parallel |
|----------|--------|--------------|------------|----------|
| **AI Required** | No | Yes | Yes | Yes |
| **# of Operations** | Any | 1 | 2+ | 2+ |
| **Dependencies** | N/A | N/A | Sequential | None |
| **Execution** | Immediate | Task() | SlashCommand() | Task() |
| **Speed** | Fastest | Fast | Slower | Fast |
| **Complexity** | Low | Medium | High | Medium |

---

## Examples by Use Case

### Configuration Management
→ **Pattern 1: Simple**
- Update config files
- Set environment variables
- Initialize directories

### Code Generation
→ **Pattern 2: Single Agent**
- Generate components
- Create boilerplate
- Scaffold structures

### Full Stack Setup
→ **Pattern 3: Sequential**
- Initialize frontend
- Initialize backend
- Setup database
- Deploy

### Quality Checks
→ **Pattern 4: Parallel**
- Lint code
- Run tests
- Security scan
- Performance check

---

## Tools by Pattern

### Pattern 1: Simple
```yaml
allowed-tools: Bash, Read, Write, Edit
```

### Pattern 2: Single Agent
```yaml
allowed-tools: Task, Read, Write, Edit, Bash
```

### Pattern 3: Sequential
```yaml
allowed-tools: SlashCommand, TodoWrite, Read, Bash
```

### Pattern 4: Parallel
```yaml
allowed-tools: Task, Read, Bash
```

---

## Best Practices

### 1. Keep Commands Focused
- One clear responsibility
- Composable with other commands
- Reusable across projects

### 2. Use TodoWrite for Tracking
- Show progress to user
- Mark completed steps
- Clear visual feedback

### 3. Validate After Operations
- Check file existence
- Verify configurations
- Run validation scripts

### 4. Provide Clear Summaries
- What was created
- Where files are located
- Next steps for user

### 5. Handle Errors Gracefully
- Check preconditions
- Provide helpful error messages
- Suggest fixes

---

## Anti-Patterns to Avoid

### ❌ Mixing Patterns
Don't combine sequential and parallel in confusing ways

### ❌ Over-orchestration
Don't chain 10+ commands - break into smaller orchestrators

### ❌ Hardcoded Paths
Always use `$ARGUMENTS` and dynamic paths

### ❌ Missing Validation
Always validate outputs before declaring success

### ❌ Poor Error Messages
Generic errors don't help - be specific about what failed

---

## Next Steps

- Read: **command-best-practices.md** for detailed best practices
- Read: **command-examples.md** for real-world examples
- See: **template-command-patterns.md** for implementation templates

---

**Last Updated**: 2025-01-02
**See Also**:
- Command Best Practices
- Command Examples
- Dan's Composition Pattern
