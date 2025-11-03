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
