# Domain Plugin Builder

> **Meta-framework for building Claude Code plugins, agents, commands, and skills**

The Domain Plugin Builder is a universal toolkit for creating production-ready Claude Code plugins. It works across ALL codebases and marketplaces, enabling rapid development of domain-specific tools and AI agents.

## 🌟 Features

- **Universal Plugin Builder** - Create complete plugins with one command
- **Cross-Repository Support** - Works in ANY codebase, not tied to a specific marketplace
- **Component Builders** - Individual commands for agents, slash commands, and skills
- **Production-Ready** - Automatic validation, testing, and Git integration
- **Template-Based** - Comprehensive templates for all component types
- **Best Practices** - Built-in validation ensures standards compliance

## 🚀 Quick Start

### Installation

Add this marketplace to your Claude Code configuration:

```bash
# Add the domain-plugin-builder marketplace
# In your Claude Code interface, add marketplace:
https://github.com/anthropics/domain-plugin-builder
```

### Build Your First Plugin

```bash
# Create a complete plugin from scratch
/domain-plugin-builder:plugin-create my-awesome-plugin

# Or build individual components
/domain-plugin-builder:slash-commands-create my-command "Description"
/domain-plugin-builder:agents-create my-agent "Description" "Bash, Read, Write"
/domain-plugin-builder:skills-create my-skill "Description"
```

## 📦 What's Included

### Slash Commands

| Command | Description |
|---------|-------------|
| `/domain-plugin-builder:plugin-create` | Build complete plugin with all components |
| `/domain-plugin-builder:slash-commands-create` | Create new slash command with proper structure |
| `/domain-plugin-builder:agents-create` | Generate specialized agent with tool configuration |
| `/domain-plugin-builder:skills-create` | Build skill with scripts, templates, and examples |
| `/domain-plugin-builder:build-plugin` | Top-level orchestrator with validation and Git integration |

### Agents

| Agent | Purpose |
|-------|---------|
| `plugin-validator` | Comprehensive plugin compliance checking |
| `skills-builder` | Complex skill creation with proper structure |

### Skills

| Skill | Description |
|-------|-------------|
| `build-assistant` | Templates, scripts, and validation tools for plugin building |

## 🏗️ Architecture

The Domain Plugin Builder follows a clean separation of concerns:

```
domain-plugin-builder/
├── plugins/domain-plugin-builder/
│   ├── commands/              # Slash commands for building
│   │   ├── plugin-create.md
│   │   ├── slash-commands-create.md
│   │   ├── agents-create.md
│   │   ├── skills-create.md
│   │   └── build-plugin.md
│   ├── agents/                # Specialized builder agents
│   │   ├── plugin-validator.md
│   │   └── skills-builder.md
│   ├── skills/                # Templates and tools
│   │   └── build-assistant/
│   │       ├── templates/     # Component templates
│   │       ├── scripts/       # Validation and utility scripts
│   │       └── examples/      # Example implementations
│   └── docs/                  # Framework documentation
│       ├── frameworks/
│       └── sdks/
└── .claude-plugin/
    └── marketplace.json
```

## 🎯 Use Cases

### SDK Plugin Development

Build plugins for Python/TypeScript SDKs:

```bash
/domain-plugin-builder:plugin-create fastmcp
# Creates complete FastMCP plugin with SDK-specific commands
```

### Framework Integration

Create framework-specific tooling:

```bash
/domain-plugin-builder:plugin-create nextjs-frontend
# Builds Next.js-specific commands and agents
```

### Custom Domain Tools

Build specialized plugins for your domain:

```bash
/domain-plugin-builder:plugin-create deployment-automation
# Creates custom deployment tooling
```

## 📚 Documentation

### Core Principles

1. **Project-Agnostic** - Never hardcode frameworks, always detect
2. **Validation-First** - All components validated before commit
3. **Git Integration** - Automatic commit and push workflow
4. **Template-Based** - Consistent structure across all components
5. **Cross-Repository** - Works in ANY codebase

### Component Patterns

**Commands** (4 patterns):
- Pattern 1: Simple (no agents)
- Pattern 2: Single Agent
- Pattern 3: Sequential (multiple slash commands)
- Pattern 4: Parallel (multiple agents)

**Agents**:
- Specialized AI capabilities with tool access
- WebFetch-based documentation loading
- Under 300 lines for optimal performance

**Skills**:
- Scripts, templates, and examples
- Reusable across plugins
- Comprehensive validation

## 🔧 Development

### Building New Components

```bash
# Add a command to an existing plugin
/domain-plugin-builder:slash-commands-create deploy "Deploy to production" --plugin=deployment

# Add an agent
/domain-plugin-builder:agents-create code-analyzer "Analyze code quality" "Bash, Read, Grep, Glob"

# Add a skill
/domain-plugin-builder:skills-create api-testing "API testing utilities"
```

### Validation

All components are automatically validated:

```bash
# Validation happens automatically during creation
# Manual validation available:
bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-plugin.sh plugins/your-plugin
```

## 🌐 Cross-Repository Usage

Unlike marketplace-specific plugins, the Domain Plugin Builder is installed **globally** and can build plugins for **any marketplace**:

```
~/.claude/plugins/marketplaces/
├── ai-dev-marketplace/        # Your AI plugins
├── dev-lifecycle-marketplace/ # Your lifecycle plugins
├── mcp-servers-marketplace/   # Your MCP plugins
└── domain-plugin-builder/     # Builder toolkit (works everywhere)
```

**Key advantage**: Install once, use everywhere!

## 🤝 Contributing

The Domain Plugin Builder is designed to be extended:

1. Add new templates to `skills/build-assistant/templates/`
2. Create new validation scripts in `skills/build-assistant/scripts/`
3. Add framework documentation to `docs/frameworks/`
4. Contribute SDK patterns to `docs/sdks/`

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with [Claude Code](https://claude.com/claude-code) following best practices from extensive plugin development experience.

---

**Questions?** Check out the comprehensive documentation in `/docs` or examine the example templates in `/skills/build-assistant/templates`.

**Want to build plugins for your domain?** This framework makes it easy to create professional, production-ready tooling for any SDK, framework, or custom use case.
