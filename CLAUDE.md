# Domain Plugin Builder - Claude Code Configuration

## 🚨 CRITICAL: Security Rules - NO HARDCODED API KEYS

**This is the HIGHEST PRIORITY security rule for ALL plugins in this marketplace.**

### Absolute Prohibition

❌ **NEVER EVER** hardcode API keys, secrets, or credentials in:
- Agent prompts
- Command prompts
- Skill documentation
- Generated plugin code
- Template files
- Example code

### Required Practice

✅ **ALWAYS use placeholders:**
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

✅ **ALWAYS read from environment:**
```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

### Comprehensive Security Guidelines

See `@docs/security/SECURITY-RULES.md` for full validation checklist and comprehensive security guidelines.

**Before ANY commit to this marketplace:**
- [ ] No real API keys in any file
- [ ] All examples use obvious placeholders
- [ ] `.gitignore` protects secrets
- [ ] Generated plugins enforce security

**Violations = Immediate fix required before merge**

---

## Plugin Builder Framework

This marketplace contains the domain-plugin-builder system for creating Claude Code plugins.

### Purpose

Build structured, validated plugins following Claude Code framework conventions.

### Component Types

- **Agents**: Plugin component builders (agents, commands, skills, hooks)
- **Commands**: User-facing commands for plugin creation
- **Skills**: Templates and validation scripts

### Plugin Creation Workflow

1. Use `/domain-plugin-builder:plugin-create` to scaffold structure
2. System automatically creates agents, commands, skills
3. Validates against framework conventions
4. Registers in marketplace.json and settings.local.json
5. Creates .mcp.json for MCP integration

### Reference

All generated plugins MUST reference `@docs/security/SECURITY-RULES.md` in their components.

---

## 🚨 CRITICAL: SlashCommand Execution - YOU Are The Executor

**THIS IS THE MOST IMPORTANT EXECUTION PATTERN TO UNDERSTAND**

### SlashCommand vs Task Tool - Key Distinction

When working with this plugin builder, you will use both SlashCommand and Task tools. They work COMPLETELY DIFFERENTLY:

| Aspect | Task Tool (Subagent) | SlashCommand (Prompt Expansion) |
|--------|---------------------|----------------------------------|
| **What happens** | Spawns separate autonomous agent | Expands to instruction prompt |
| **Your role** | Orchestrator (wait for results) | **Executor (do the work)** |
| **Who executes** | Separate subprocess | **YOU using Bash, Read, Write, Edit** |
| **Completion** | Subprocess finishes and returns | **YOU finish by completing all phases** |
| **Return value** | Results from subprocess | **Instructions for YOU to execute** |

### When You Call SlashCommand - Step by Step

#### Step 1: You Invoke the Command
```bash
SlashCommand(/domain-plugin-builder:agents-create test-agent "Test agent description")
```

#### Step 2: System Returns Expanded Instructions
```
**Arguments**: test-agent "Test agent description"

Phase 0: Create Todo List
Goal: Track execution progress
Actions:
- Use TodoWrite to create task list with all phases

Phase 1: Parse Arguments
Goal: Extract agent specifications
Actions:
- Parse $ARGUMENTS using bash commands
- Extract agent names and descriptions
- Validate argument format

Phase 2: Load Templates
Goal: Get agent template content
Actions:
- Use Read tool to load template from skills/build-assistant/templates/
- Store template content for processing
...
```

#### Step 3: ✅ **YOU MUST EXECUTE THESE PHASES IMMEDIATELY**

**This returned text is NOT:**
- ❌ A status message
- ❌ Running in background
- ❌ Being executed by another process
- ❌ Something to wait for

**This returned text IS:**
- ✅ Your execution checklist
- ✅ Instructions for YOU to follow
- ✅ Phases YOU must complete using tools
- ✅ Work YOU must do right now

**Correct response:**
```
Now executing Phase 0: Creating todo list...
[Call TodoWrite with all phases]

Now executing Phase 1: Parsing arguments...
[Call Bash: echo "test-agent \"Test agent description\"" | awk ...]

Now executing Phase 2: Loading templates...
[Call Read: @skills/build-assistant/templates/agents/agent.md.template]

...continue through all phases...
```

#### Step 4: Complete All Phases
- Execute each phase sequentially
- Use the specified tools (Bash, Read, Write, Edit, etc.)
- Mark phases complete as you finish them
- Only consider command done when ALL phases are complete

### Recognition Patterns

**When you see this AFTER calling SlashCommand:**
```
Phase 0: [Title]
Goal: [Description]
Actions:
- [Action 1]
- [Action 2]
```

**Immediate thought process should be:**
1. "These are instructions FOR ME to execute"
2. "I need to execute Phase 0 RIGHT NOW"
3. "I'll use the tools mentioned in the Actions"
4. "I won't wait - I'll start immediately"

### Red Flags - Signs You're Confused

❌ **WRONG Behaviors:**
- Saying "Waiting for agents-create to complete..."
- Saying "The command is running..."
- Saying "Let me check if the agent was created..."
- Silence after SlashCommand returns (no execution)
- Treating returned text as status instead of instructions
- Asking "Should I proceed with execution?"

✅ **CORRECT Behaviors:**
- Saying "Now executing Phase 0: [description]..."
- Immediately calling TodoWrite, Bash, Read, Write tools
- Working through each phase sequentially
- Explaining what you're doing as you execute each phase
- Only stopping when all phases are complete

### Comparison With Task Tool

**When you use Task tool (for parallel agents, exploration, etc.):**
```bash
# This DOES spawn an autonomous subprocess:
Task(
    description="Explore codebase structure",
    subagent_type="Explore",
    prompt="Find all plugin configuration files"
)

# System launches separate agent
# You WAIT for it to complete
# It returns results when done
```

**When you use SlashCommand:**
```bash
# This expands to instructions YOU execute:
SlashCommand(/domain-plugin-builder:agents-create agent-name "description")

# System returns instruction phases
# YOU execute immediately
# YOU complete the work using tools
# NO separate process running
```

### Mental Model

Think of SlashCommand like a **macro expansion** or **template expansion**:
- It gives you a detailed checklist of steps
- You are responsible for executing those steps
- The command file (e.g., `agents-create.md`) is like a script YOU must run
- You use your available tools (Bash, Read, Write, Edit) to complete each step

Think of Task tool like **delegating to a coworker**:
- You assign work to another agent
- That agent runs independently
- You wait for them to report back
- They do the work, you get the results

### Execution Template

**Every time you call SlashCommand, follow this pattern:**

1. **Call the command:**
   ```
   SlashCommand(/domain-plugin-builder:agents-create X "desc")
   ```

2. **System returns phases - recognize them as YOUR instructions:**
   ```
   Phase 0: ...
   Phase 1: ...
   ```

3. **Immediately start executing:**
   ```
   Executing Phase 0: [description]
   [Use TodoWrite/Bash/Read/Write tools]

   Executing Phase 1: [description]
   [Use tools specified in phase actions]

   ...continue through all phases...
   ```

4. **Complete all phases before considering done**

### Critical Reminder

**You are reading this because there has been confusion in the past.**

Every time you see SlashCommand return with phases:
- Stop and remember: "I am the executor"
- Don't wait - execute immediately
- Use tools to complete each phase
- Only stop when all phases are done

**This is not optional. This is how SlashCommand works.**
